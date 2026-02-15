import openai
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
import json
from typing import Dict, List, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class LLMClient:
    """
    Client for interacting with Ollama (primary) and OpenAI (fallback)
    """

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        default_model: str = "gpt-4-turbo-preview"
    ):
        """
        Initialize LLM client with Ollama and OpenAI
        """
        self.openai_api_key = openai_api_key
        # Default model for OpenAI fallback
        self.default_model = default_model
        
        self.openai_client = None
        self.ollama_client = None
        
        # Initialize Ollama Client (Primary)
        # Ollama supports OpenAI-compatible API
        try:
            logger.info(f"Initializing Ollama Client at {settings.OLLAMA_BASE_URL} with model {settings.OLLAMA_MODEL}")
            self.ollama_client = openai.OpenAI(
                base_url=settings.OLLAMA_BASE_URL,
                api_key="ollama"  # Required by library but unused by Ollama
            )
        except Exception as e:
            logger.error(f"Failed to initialize Ollama client structure: {str(e)}")

        # Initialize OpenAI Client (Fallback)
        if openai_api_key:
            try:
                self.openai_client = openai.OpenAI(api_key=openai_api_key)
                logger.info("OpenAI Client initialized (Fallback)")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
        else:
            logger.warning("OpenAI API key missing. Fallback will not be available.")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_with_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate text using Ollama (primary) or OpenAI (fallback)
        """
        # 1. Try Ollama (Primary)
        if self.ollama_client:
            try:
                # Use configured Ollama model
                ollama_model = settings.OLLAMA_MODEL
                logger.info(f"Attempting generation with Ollama model: {ollama_model}")
                
                # Note: Ollama might not support 'json_object' format for all models
                # We'll try without strict response_format first
                response = self.ollama_client.chat.completions.create(
                    model=ollama_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                content = response.choices[0].message.content
                if content:
                    logger.info(f"✓ Ollama generation successful ({len(content)} chars)")
                    return content
                else:
                    logger.warning("Ollama returned empty content")
                    
            except Exception as e:
                logger.warning(f"⚠ Ollama generation failed: {str(e)}. Falling back to OpenAI...")
        else:
            logger.warning("Ollama client not initialized. Falling back to OpenAI...")

        # 2. Fallback to OpenAI
        if not self.openai_client:
            error_msg = "OpenAI fallback unavailable: API key not configured"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            fallback_model = model or self.default_model
            logger.info(f"Generating with OpenAI fallback model: {fallback_model}")

            # Use JSON mode for reliable script formatting if using GPT-4 models
            response_format = {"type": "json_object"} if "gpt-4" in fallback_model else None

            response = self.openai_client.chat.completions.create(
                model=fallback_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format
            )

            content = response.choices[0].message.content
            logger.info(f"✓ OpenAI fallback generation successful ({len(content)} chars)")

            return content

        except Exception as e:
            logger.error(f"OpenAI generation failed: {str(e)}")
            raise

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        provider: str = "openai",
        **kwargs
    ) -> str:
        """
        Generate text wrapper
        """
        return await self.generate_with_openai(
            system_prompt,
            user_prompt,
            **kwargs
        )

    def count_tokens(self, text: str, model: str = "gpt-4") -> int:
        """
        Estimate token count
        """
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception:
            # Fallback
            return len(text) // 4

    def is_available(self, provider: str = "openai") -> bool:
        """
        Check if any LLM client is available
        """
        return (self.ollama_client is not None) or (self.openai_client is not None)
