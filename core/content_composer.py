from core.image_generator import generate_image
from core.video_generator import generate_video
from core.voice_generator import generate_voice
from core.music_generator import generate_music


def _build_content_plan(
    prompt,
    style,
    content_type,
    voice,
    narration_tone,
    music_style,
    music_duration,
    video_motion,
    video_duration,
):
    """
    Build a coordinated content plan from one user idea.
    """

    prompt = prompt.strip()

    content_type_instructions = {
        "Story": (
            "Create a strong visual story with a clear subject, "
            "setting, atmosphere, and sense of narrative."
        ),
        "Advertisement": (
            "Create a polished commercial-style composition "
            "that clearly presents the subject or product."
        ),
        "Social Media": (
            "Create an attention-grabbing social-media composition "
            "with a strong focal point and visually engaging details."
        ),
        "Explainer": (
            "Create a clear educational visual with an obvious "
            "subject and environment that supports explanation."
        ),
        "Cinematic": (
            "Create a dramatic cinematic composition with strong "
            "lighting, depth, atmosphere, and visual storytelling."
        ),
    }

    tone_instructions = {
        "Professional": (
            "Use a clear, polished and authoritative narration style."
        ),
        "Inspirational": (
            "Use an uplifting, motivating and encouraging narration style."
        ),
        "Dramatic": (
            "Use an emotional, dramatic and suspenseful narration style."
        ),
        "Friendly": (
            "Use a warm, conversational and approachable narration style."
        ),
    }

    image_prompt = (
        f"{style}, {prompt}. "
        f"{content_type_instructions.get(content_type, '')} "
        "Create a high-quality cinematic composition with "
        "clear subjects, natural lighting, realistic details, "
        "strong visual storytelling, and a consistent environment."
    )

    narration = (
        f"{tone_instructions.get(narration_tone, '')} "
        f"Today, we explore this story: {prompt}. "
        "Follow the visual story and imagine the scene unfolding "
        "naturally from beginning to end."
    )

    return {
        "original_prompt": prompt,
        "content_type": content_type,
        "image_prompt": image_prompt,
        "narration": narration,
        "voice": voice,
        "narration_tone": narration_tone,
        "video_motion": video_motion,
        "video_duration": video_duration,
        "music_style": music_style,
        "music_duration": music_duration,
    }


def create_content_package(
    prompt,
    style="Realistic",
    content_type="Story",
    voice="English Female",
    narration_tone="Friendly",
    music_style="Cinematic",
    music_duration=10,
    video_motion="Zoom In",
    video_duration=5,
):
    """
    Create a coordinated content package from one idea.

    The package contains:

        - Generated image
        - Generated video
        - Generated voice narration
        - Generated background music

    All assets are created from the same content plan.
    """

    if not prompt or not prompt.strip():
        raise ValueError(
            "Please enter a content idea."
        )

    plan = _build_content_plan(
        prompt=prompt,
        style=style,
        content_type=content_type,
        voice=voice,
        narration_tone=narration_tone,
        music_style=music_style,
        music_duration=music_duration,
        video_motion=video_motion,
        video_duration=video_duration,
    )

    # -------------------------------------------------
    # IMAGE
    # -------------------------------------------------

    image_path = generate_image(
        plan["image_prompt"]
    )

    # -------------------------------------------------
    # VIDEO
    # -------------------------------------------------

    video_path = generate_video(
        image_path,
        plan["video_motion"],
        plan["video_duration"],
    )

    # -------------------------------------------------
    # VOICE
    # -------------------------------------------------

    voice_path = generate_voice(
        plan["narration"],
        plan["voice"],
    )

    # -------------------------------------------------
    # MUSIC
    # -------------------------------------------------

    music_path = generate_music(
        plan["music_style"],
        plan["music_duration"],
    )

    return {
        "image": image_path,
        "video": video_path,
        "voice": voice_path,
        "music": music_path,
        "plan": plan,
    }