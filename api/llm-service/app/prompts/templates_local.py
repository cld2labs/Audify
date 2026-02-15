"""
Prompt templates specifically for local models (Ollama/Mistral/Llama)
Focuses on simpler, step-by-step instructions.
"""

# 1. ANALYZE/SUMMARIZE CHUNK
SUMMARIZE_CHUNK_SYSTEM = """You are a research assistant. Your job is to analyze text and extract key information.
Do NOT write a script. Only extract insights."""

SUMMARIZE_CHUNK_USER = """Analyze the following text section.
Extract:
1. Main themes or topics discussed.
2. Interesting facts or key takeaways.
3. Quotable moments or strong arguments.

Text to analyze:
{content}

Return the insights as a bulleted list. Keep it concise."""

# 2. CREATE OUTLINE
OUTLINE_SYSTEM = """You are a podcast producer. You plan the structure of episodes."""

OUTLINE_USER = """Based on the following research notes, create an outline for a podcast episode.
The host is {host_name} and the guest is {guest_name}.

Research Notes:
{insights}

Create a structured outline with:
1. Episode Title (Catchy)
2. Introduction (Brief)
3. 4-6 Conversational Segments (Topics to discuss in order)
4. Conclusion (Wrap up)

Format the output clearly."""

# 3. GENERATE SCRIPT SEGMENT
SCRIPT_SEGMENT_SYSTEM = """You are a scriptwriter for a podcast. Write natural, conversational dialogue.
The host is {host_name} and the guest is {guest_name}.
Tone: {tone}"""

SCRIPT_SEGMENT_USER = """Write the dialogue for this specific part of the podcast:
"{segment_topic}"

Context/Key Info to cover:
{segment_context}

Previous dialogue (for continuity):
{previous_dialogue}

Rules:
- Write ONLY the dialogue in JSON format: [{{"speaker": "{host_name}", "text": "..."}}, {{"speaker": "{guest_name}", "text": "..."}}]
- Make it sound natural (use "um", "you know", laughs).
- Host guides, Guest explains.
- Keep it focused on the topic."""

def get_local_summary_prompt(content: str) -> dict:
    return {
        "system": SUMMARIZE_CHUNK_SYSTEM,
        "user": SUMMARIZE_CHUNK_USER.format(content=content)
    }

def get_local_outline_prompt(insights: str, host_name: str, guest_name: str) -> dict:
    return {
        "system": OUTLINE_SYSTEM,
        "user": OUTLINE_USER.format(insights=insights, host_name=host_name, guest_name=guest_name)
    }

def get_local_script_prompt(
    segment_topic: str,
    segment_context: str,
    previous_dialogue: str,
    host_name: str,
    guest_name: str,
    tone: str
) -> dict:
    return {
        "system": SCRIPT_SEGMENT_SYSTEM.format(host_name=host_name, guest_name=guest_name, tone=tone),
        "user": SCRIPT_SEGMENT_USER.format(
            segment_topic=segment_topic,
            segment_context=segment_context,
            previous_dialogue=previous_dialogue,
            host_name=host_name,
            guest_name=guest_name
        )
    }
