from pathlib import Path

from core.image_generator import generate_image
from core.video_generator import generate_video
from core.voice_generator import generate_voice
from core.music_generator import generate_music


def create_content_package(
    prompt,
    style="Realistic",
    voice="English Female",
    music_style="Cinematic",
    music_duration=10,
):
    """
    Create a complete content package from one idea.

    The package contains:
        - Generated image
        - Generated video
        - Generated voice narration
        - Generated background music
    """

    if not prompt or not prompt.strip():
        raise ValueError("Please enter a content idea.")

    prompt = prompt.strip()

    # -------------------------------------------------
    # 1. IMAGE
    # -------------------------------------------------

    image_path = generate_image(
        f"{style}, {prompt}"
    )

    # -------------------------------------------------
    # 2. VIDEO
    # -------------------------------------------------

    video_path = generate_video(
        image_path
    )

    # -------------------------------------------------
    # 3. VOICE
    # -------------------------------------------------

    narration = (
        f"Welcome to Personal AI Studio. "
        f"{prompt}"
    )

    voice_path = generate_voice(
        narration,
        voice,
    )

    # -------------------------------------------------
    # 4. MUSIC
    # -------------------------------------------------

    music_path = generate_music(
        music_style,
        music_duration,
    )

    return {
        "image": image_path,
        "video": video_path,
        "voice": voice_path,
        "music": music_path,
    }