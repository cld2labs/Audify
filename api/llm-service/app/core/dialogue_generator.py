import logging
from typing import Dict, List, Optional
from app.core.llm_client import LLMClient
from app.core.prompt_builder import PromptBuilder
from app.core.script_formatter import ScriptFormatter

logger = logging.getLogger(__name__)

class DialogueGenerator:
    """
    Main orchestrator for podcast dialogue generation
    """

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        default_model: str = "gpt-4-turbo-preview"
    ):
        """
        Initialize dialogue generator

        Args:
            openai_api_key: OpenAI API key
            default_model: Default model to use
        """
        self.llm_client = LLMClient(
            openai_api_key=openai_api_key,
            default_model=default_model
        )
        self.prompt_builder = PromptBuilder()
        self.formatter = ScriptFormatter()

    async def generate_script(
        self,
        text: str,
        host_name: str = "Host",
        guest_name: str = "Guest",
        tone: str = "conversational",
        max_length: int = 2000,
        provider: str = "openai",
        target_audience: str = "general",
        **kwargs
    ) -> Dict:
        """
        Generate podcast script from text
        """
        # Dispatch to appropriate strategy
        if provider == "ollama":
            try:
                # Try the Blueprint Strategy for Local Models
                result = await self.generate_script_with_strategy(
                    text, host_name, guest_name, tone, max_length
                )
                
                # Standard post-processing (shared)
                return await self._process_generated_script(
                    result["script"], text, host_name, guest_name, tone
                )
                
            except Exception as e:
                logger.warning(f"Local strategy failed: {str(e)}. Fallback to standard generation.")
                # Fallback to standard method (likely will use OpenAI if configured, or fail if no fallback)
                # We switch provider to 'openai' to force the fallback path in standard generation if available
                return await self._generate_standard_script(
                    text, host_name, guest_name, tone, max_length, provider="openai", target_audience=target_audience, **kwargs
                )
        else:
            return await self._generate_standard_script(
                text, host_name, guest_name, tone, max_length, provider, target_audience=target_audience, **kwargs
            )

    async def _generate_standard_script(
        self,
        text: str,
        host_name: str,
        guest_name: str,
        tone: str,
        max_length: int,
        provider: str,
        target_audience: str = "general",
        **kwargs
    ) -> Dict:
        """Standard single-shot generation (Original Logic)"""
        try:
            logger.info(f"Generating script for {len(text)} chars of content (Standard)")

            # Validate input
            if not text or len(text.strip()) < 50:
                raise ValueError("Content too short for script generation")

            # Build prompts
            prompts = self.prompt_builder.build_generation_prompt(
                content=text,
                tone=tone,
                max_length=max_length,
                host_name=host_name,
                guest_name=guest_name,
                target_audience=target_audience
            )

            # Generate with LLM
            response = await self.llm_client.generate(
                system_prompt=prompts["system"],
                user_prompt=prompts["user"],
                provider=provider,
                temperature=0.7,
                max_tokens=4000
            )

            # Parse and validate response
            script = self.formatter.parse_llm_response(response)
            
            return await self._process_generated_script(
                script, text, host_name, guest_name, tone
            )

        except Exception as e:
            logger.error(f"Script generation failed: {str(e)}")
            raise

    async def _process_generated_script(
        self,
        script: List[Dict],
        original_text: str,
        host_name: str,
        guest_name: str,
        tone: str
    ) -> Dict:
        """Shared post-processing for scripts"""
        if not self.formatter.validate_script(script):
            raise ValueError("Generated script failed validation")

        # Post-process script
        script = self.formatter.merge_short_turns(script)
        script = self.formatter.truncate_script(script, max_turns=50)

        # Format for TTS
        tts_script = self.formatter.format_for_tts(script)

        # Calculate metadata
        metadata = self.formatter.calculate_metadata(tts_script)
        metadata["tone"] = tone
        metadata["host_name"] = host_name
        metadata["guest_name"] = guest_name
        metadata["source_length"] = len(original_text)

        logger.info(
            f"Generated script: {metadata['total_turns']} turns, "
            f"{metadata['estimated_duration_minutes']} min"
        )

        return {
            "script": tts_script,
            "metadata": metadata,
            "status": "success"
        }

    async def refine_script(
        self,
        script: List[Dict[str, str]],
        provider: str = "openai"
    ) -> Dict:
        """
        Refine an existing script

        Args:
            script: Current script
            provider: LLM provider

        Returns:
            Dict with refined script and metadata
        """
        try:
            logger.info(f"Refining script with {len(script)} turns")

            # Build refinement prompts
            prompts = self.prompt_builder.build_refinement_prompt(script)

            # Generate refinement
            response = await self.llm_client.generate(
                system_prompt=prompts["system"],
                user_prompt=prompts["user"],
                provider=provider,
                temperature=0.5,  # Lower temperature for refinement
                max_tokens=4000
            )

            # Parse response
            refined_script = self.formatter.parse_llm_response(response)

            if not self.formatter.validate_script(refined_script):
                logger.warning("Refined script invalid, returning original")
                return {
                    "script": script,
                    "metadata": self.formatter.calculate_metadata(script),
                    "status": "unchanged"
                }

            # Format and calculate metadata
            tts_script = self.formatter.format_for_tts(refined_script)
            metadata = self.formatter.calculate_metadata(tts_script)

            logger.info("Script refinement successful")

            return {
                "script": tts_script,
                "metadata": metadata,
                "status": "refined"
            }

        except Exception as e:
            logger.error(f"Script refinement failed: {str(e)}")
            # Return original script on failure
            return {
                "script": script,
                "metadata": self.formatter.calculate_metadata(script),
                "status": "error",
                "error": str(e)
            }

    async def generate_script_with_strategy(
        self,
        text: str,
        host_name: str,
        guest_name: str,
        tone: str,
        max_length: int
    ) -> Dict:
        """
        Generate script using the Blueprint Method (Map-Reduce-Expand)
        Optimized for local models.
        """
        logger.info("Executing Blueprint Strategy for Local Model")
        
        # 1. Map: Semantic Chunking & Summarization
        chunks = self._chunk_content(text)
        logger.info(f"Split content into {len(chunks)} chunks")
        
        import asyncio
        semaphore = asyncio.Semaphore(3)  # Limit concurrent local model requests

        async def summarize_chunk_safe(index, chunk):
            async with semaphore:
                logger.info(f"Analyzing chunk {index+1}/{len(chunks)}")
                summary_prompt = self.prompt_builder.build_local_summary_prompt(chunk)
                return await self.llm_client.generate(
                    system_prompt=summary_prompt["system"],
                    user_prompt=summary_prompt["user"],
                    provider="ollama",
                    temperature=0.3,
                    max_tokens=1000
                )

        tasks = [summarize_chunk_safe(i, chunk) for i, chunk in enumerate(chunks)]
        insights = await asyncio.gather(*tasks)
            
        combined_insights = "\n\n".join([f"Chunk {i+1}:\n{s}" for i, s in enumerate(insights)])
        
        # 2. Reduce: Create Outline
        logger.info("Generating episode outline...")
        outline_prompt = self.prompt_builder.build_local_outline_prompt(
            combined_insights, host_name, guest_name
        )
        outline = await self.llm_client.generate(
            system_prompt=outline_prompt["system"],
            user_prompt=outline_prompt["user"],
            provider="ollama",
            temperature=0.7,
            max_tokens=2000
        )
        
        # 3. Expand: Generate Script Segments
        logger.info("Generating script from outline...")
        
        # Simple parsing of outline into segments (heuristic)
        # We'll treat the outline as the "Map" for generation
        
        script_parts = []
        previous_dialogue = "None"
        
        # Generate in 2-3 passes if long, but for now let's try a guided generation
        # NOTE: For simplicity in this iteration, we feed the outline + context to generate
        # In a fully robust version, we'd parse the outline into distinct segments.
        # Here we will do a guided generation prompt.
        
        # Actually, let's stick to the plan: Segment by Segment.
        # We need to split the outline into segments.
        # Since strict parsing is hard, let's ask the LLM to write it section by section based on the outline.
        
        segments = ["Introduction", "Main Discussion", "Conclusion"] 
        
        full_script = []
        
        for segment in segments:
            logger.info(f"Generating segment: {segment}")
            script_prompt = self.prompt_builder.build_local_script_prompt(
                segment_topic=segment,
                segment_context=f"Follow this outline:\n{outline}\n\nKey Insights:\n{combined_insights}",
                previous_dialogue=previous_dialogue[-500:] if len(previous_dialogue) > 5 else "Start of episode",
                host_name=host_name,
                guest_name=guest_name,
                tone=tone
            )
            
            segment_text = await self.llm_client.generate(
                system_prompt=script_prompt["system"],
                user_prompt=script_prompt["user"],
                provider="ollama",
                temperature=0.7,
                max_tokens=3000
            )
            
            # Clean up JSON
            try:
                # Find JSON array
                start = segment_text.find('[')
                end = segment_text.rfind(']') + 1
                if start >= 0 and end > start:
                    json_str = segment_text[start:end]
                    import json
                    segment_json = json.loads(json_str)
                    full_script.extend(segment_json)
                    
                    # Update previous dialogue string for context
                    last_lines = "\n".join([f"{t['speaker']}: {t['text']}" for t in segment_json[-3:]])
                    previous_dialogue = last_lines
                else:
                    logger.warning(f"Could not parse JSON for segment {segment}")
            except Exception as e:
                logger.error(f"Error parsing segment {segment}: {e}")
                
        if not full_script:
            raise ValueError("Failed to generate any valid script segments")
            
        return {
            "script": full_script,
            "metadata": {}, # populated by caller
            "status": "success"
        }

    def _chunk_content(self, text: str, target_tokens: int = 4000) -> List[str]:
        """
        Semantically chunk content by paragraphs with overlap
        """
        # Split by double newlines to preserve paragraphs
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = []
        current_length = 0
        overlap_buffer = [] # Buffer for overlap
        
        for para in paragraphs:
            # Rough token estimate (4 chars per token)
            para_len = len(para) // 4
            
            if current_length + para_len > target_tokens and current_chunk:
                # Finalize current chunk
                # Add overlap from previous chunk if available
                chunk_text = "\n\n".join(overlap_buffer + current_chunk)
                chunks.append(chunk_text)
                
                # Start new chunk with overlap (last 2 paragraphs of previous)
                overlap_buffer = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk
                current_chunk = [para]
                current_length = para_len + sum(len(p)//4 for p in overlap_buffer)
            else:
                current_chunk.append(para)
                current_length += para_len
                
        # Add final chunk
        if current_chunk:
            chunk_text = "\n\n".join(overlap_buffer + current_chunk)
            chunks.append(chunk_text)
            
        return chunks

    def validate_content_length(self, text: str) -> Dict:
        """
        Validate if content is suitable for podcast generation
        
        Args:
            text: Content to validate
            
        Returns:
            Dict with validation results
        """
        word_count = len(text.split())
        char_count = len(text)

        # Check token count
        token_count = self.llm_client.count_tokens(text)

        issues = []
        recommendations = []

        # Too short
        if word_count < 100:
            issues.append("Content is very short")
            recommendations.append("Add more context or background information")

        # Too long
        if token_count > 8000:
            issues.append("Content may be too long for single request")
            recommendations.append("Consider breaking into multiple sections")

        # Very technical
        technical_indicators = ["algorithm", "theorem", "equation", "formula"]
        if any(word in text.lower() for word in technical_indicators):
            recommendations.append("Consider using 'educational' tone for technical content")

        return {
            "valid": len(issues) == 0,
            "word_count": word_count,
            "char_count": char_count,
            "token_count": token_count,
            "issues": issues,
            "recommendations": recommendations
        }

