from core.ai_planner import create_production_plan
from core.image_generator import generate_image
from core.video_generator import generate_video
from core.voice_generator import generate_voice
from core.music_generator import generate_music


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
    Create a complete coordinated content package.

    The local AI planner first creates the creative production plan.
    The existing generators then create the individual assets.
    """

    if not prompt or not prompt.strip():
        raise ValueError(
            "Please enter a content idea."
        )

    # -------------------------------------------------
    # 1. AI PRODUCTION PLAN
    # -------------------------------------------------

    plan = create_production_plan(
        prompt=prompt,
        style=style,
        content_type=content_type,
        narration_tone=narration_tone,
        music_style=music_style,
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
        video_motion,
        video_duration,
    )

    # -------------------------------------------------
    # 4. VOICE
    # -------------------------------------------------

    voice_path = generate_voice(
        plan["narration_script"],
        voice,
    )

    # -------------------------------------------------
    # 5. MUSIC
    # -------------------------------------------------

    music_path = generate_music(
        music_style,
        music_duration,
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