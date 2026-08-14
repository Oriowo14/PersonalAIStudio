import json

import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:1.7b"


def create_production_plan(
    prompt,
    style="Realistic",
    content_type="Story",
    narration_tone="Friendly",
    music_style="Cinematic",
):
    """
    Create a structured production plan using
    the local Qwen model through Ollama.
    """

    if not prompt or not prompt.strip():
        raise ValueError(
            "Please enter a content idea."
        )

    system_prompt = """
You are the creative production planner for Personal AI Studio.

Turn the user's content idea into a practical production plan
for an AI-generated image, video, narration, and background music.

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{
    "title": "",
    "story_concept": "",
    "main_subject": "",
    "setting": "",
    "visual_direction": "",
    "image_prompt": "",
    "video_direction": "",
    "narration_script": "",
    "music_direction": ""
}

IMPORTANT RULES:

1. Never invent a person's name.
2. Never invent a company name.
3. Never invent specific facts that the user did not provide.
4. If the person has no name, describe them by their role,
   appearance, age range, or other information provided.
5. Keep the same main subject throughout the entire plan.
6. Keep the setting consistent.
7. The image prompt must describe the same subject and setting.
8. The video direction must describe movement that could naturally
   happen in the scene.
9. The narration must match the story.
10. The music direction must match the emotional tone.
11. Do not mention Personal AI Studio in the narration.
12. Do not add markdown.
13. Do not wrap the JSON in ```json or ```.

Keep the plan concise but useful.
"""

    user_prompt = f"""
CONTENT IDEA:
{prompt}

CONTENT TYPE:
{content_type}

IMAGE STYLE:
{style}

NARRATION TONE:
{narration_tone}

MUSIC STYLE:
{music_style}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "stream": False,
        "format": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                },
                "story_concept": {
                    "type": "string",
                },
                "main_subject": {
                    "type": "string",
                },
                "setting": {
                    "type": "string",
                },
                "visual_direction": {
                    "type": "string",
                },
                "image_prompt": {
                    "type": "string",
                },
                "video_direction": {
                    "type": "string",
                },
                "narration_script": {
                    "type": "string",
                },
                "music_direction": {
                    "type": "string",
                },
            },
            "required": [
                "title",
                "story_concept",
                "main_subject",
                "setting",
                "visual_direction",
                "image_prompt",
                "video_direction",
                "narration_script",
                "music_direction",
            ],
        },
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300,
        )

        response.raise_for_status()

    except requests.RequestException as error:

        raise RuntimeError(
            f"Could not connect to Ollama: {error}"
        )

    data = response.json()

    message = data.get(
        "message",
        {},
    )

    content = message.get(
        "content",
        "",
    ).strip()

    if not content:
        raise RuntimeError(
            "Ollama returned an empty response."
        )

    try:

        plan = json.loads(content)

    except json.JSONDecodeError as error:

        raise RuntimeError(
            f"Ollama returned invalid JSON: {error}"
        )

    required_fields = [
        "title",
        "story_concept",
        "main_subject",
        "setting",
        "visual_direction",
        "image_prompt",
        "video_direction",
        "narration_script",
        "music_direction",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in plan
    ]

    if missing_fields:

        raise RuntimeError(
            "Production plan is missing fields: "
            + ", ".join(missing_fields)
        )

    return plan