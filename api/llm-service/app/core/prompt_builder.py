import logging
from typing import Dict, Optional
from app.prompts.templates import (
    get_system_prompt,
    get_user_prompt,
    get_content_length_prompt
)
from app.prompts.templates_local import (
    get_local_summary_prompt,
    get_local_outline_prompt,
    get_local_script_prompt
)

logger = logging.getLogger(__name__)

class PromptBuilder:
    """
    Build prompts for podcast script generation
    """

    def __init__(self):
        self.system_prompt = get_system_prompt()

    def build_generation_prompt(
        self,
        content: str,
        tone: str = "conversational",
        max_length: int = 2000,
        host_name: str = "Host",
        guest_name: str = "Guest",
        target_audience: str = "general"
    ) -> Dict[str, str]:
        """
        Build prompts for script generation

        Args:
            content: Source content
            tone: Conversation tone
            max_length: Target word count
            host_name: Host name
            guest_name: Guest name
            target_audience: Target audience (general, beginner, expert)

        Returns:
            Dict with system and user prompts
        """
        # Calculate target number of dialogue turns
        # Rough estimate: 50-100 words per turn
        if tone == "quick_brief":
             # Shorter for specific style
             target_turns = max(5, min(15, max_length // 100))
        else:
             target_turns = max(10, min(30, max_length // 75))

        # Build user prompt
        user_prompt = get_user_prompt(
            content=content,
            tone=tone,
            target_audience=target_audience,
            target_turns=target_turns
        )

        # Add length-specific guidance
        content_length = len(content)
        length_prompt = get_content_length_prompt(content_length, target_turns)

        if length_prompt:
            user_prompt += f"\n\n{length_prompt}"

        # Add names if custom
        if host_name != "Host" or guest_name != "Guest":
            user_prompt += f"\n\nUse these names:\n- Host: {host_name}\n- Guest: {guest_name}"

        logger.info(f"Built prompt for {content_length} chars, targeting {target_turns} turns")

        return {
            "system": self.system_prompt,
            "user": user_prompt
        }

    def build_refinement_prompt(self, script: list) -> Dict[str, str]:
        """
        Build prompts for script refinement

        Args:
            script: Current script

        Returns:
            Dict with system and user prompts
        """
        from app.prompts.templates import SCRIPT_REFINEMENT_PROMPT

        user_prompt = SCRIPT_REFINEMENT_PROMPT.format(
            current_script=script
        )

        return {
            "system": self.system_prompt,
            "user": user_prompt
        }

    def build_local_summary_prompt(self, content: str) -> Dict[str, str]:
        """Build prompt for summarizing a chunk (Local Model)"""
        return get_local_summary_prompt(content)

    def build_local_outline_prompt(self, insights: str, host_name: str, guest_name: str) -> Dict[str, str]:
        """Build prompt for generating outline (Local Model)"""
        return get_local_outline_prompt(insights, host_name, guest_name)

    def build_local_script_prompt(
        self,
        segment_topic: str,
        segment_context: str,
        previous_dialogue: str,
        host_name: str,
        guest_name: str,
        tone: str
    ) -> Dict[str, str]:
        """Build prompt for generating script segment (Local Model)"""
        return get_local_script_prompt(
            segment_topic, segment_context, previous_dialogue, host_name, guest_name, tone
        )
