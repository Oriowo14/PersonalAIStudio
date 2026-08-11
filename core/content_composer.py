from core.image_generator import generate_image
from core.video_generator import generate_video
from core.voice_generator import generate_voice
from core.music_generator import generate_music


def _build_content_plan(
    prompt,
    style,
    voice,
    music_style,
    music_duration,
):
    """
    Build a coordinated content plan from one user idea.
    """

    prompt = prompt.strip()

    image_prompt = (
        f"{style}, {prompt}. "
        "Create a high-quality cinematic composition with "
        "clear subjects, natural lighting, realistic details, "
        "strong visual storytelling, and a consistent environment."
    )

    narration = (
        f"Welcome to Personal AI Studio. "
        f"Today, we explore this story: {prompt}. "
        "Follow the visual story and imagine the scene unfolding "
        "naturally from beginning to end."
    )

    video_motion = "Zoom In"

    return {
        "original_prompt": prompt,
        "image_prompt": image_prompt,
        "narration": narration,
        "voice": voice,
        "video_motion": video_motion,
        "music_style": music_style,
        "music_duration": music_duration,
    }


def create_content_package(
    prompt,
    style="Realistic",
    voice="English Female",
    music_style="Cinematic",
    music_duration=10,
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

    # -------------------------------------------------
    # 1. BUILD CONTENT PLAN
    # -------------------------------------------------

    plan = _build_content_plan(
        prompt=prompt,
        style=style,
        voice=voice,
        music_style=music_style,
        music_duration=music_duration,
    )

    # -------------------------------------------------
    # 2. IMAGE
    # -------------------------------------------------

    image_path = generate_image(
        plan["image_prompt"]
    )

    # -------------------------------------------------
    # 3. VIDEO
    # -------------------------------------------------

    video_path = generate_video(
        image_path,
        plan["video_motion"],
        5,
    )

    # -------------------------------------------------
    # 4. VOICE
    # -------------------------------------------------

    voice_path = generate_voice(
        plan["narration"],
        plan["voice"],
    )

    # -------------------------------------------------
    # 5. MUSIC
    # -------------------------------------------------

    music_path = generate_music(
        plan["music_style"],
        plan["music_duration"],
    )

    # -------------------------------------------------
    # 6. RETURN COMPLETE PACKAGE
    # -------------------------------------------------

    return {
        "image": image_path,
        "video": video_path,
        "voice": voice_path,
        "music": music_path,
        "plan": plan,
    }