import gradio as gr

from config import load_config
from core.content_composer import create_content_package


def create_content_composer_panel():

    config = load_config()

    video_provider = config.get(
        "video_provider",
        "local",
    )

    gr.Markdown("# 🎬 AI Content Composer")

    gr.Markdown(
        """
Turn one idea into a complete content package containing
an image, video, voice narration, and background music.
"""
    )

    if video_provider == "pollinations":

        gr.Markdown(
            """
🤖 **AI Motion Video Enabled**

The video will use Pollinations image-to-video.
This requires available Pollen balance.
"""
        )

    else:

        gr.Markdown(
            """
🆓 **Local Motion Video Enabled**

The video will use free cinematic camera movement.
For genuine subject movement, select Pollinations AI Motion
in Settings when you have available Pollen.
"""
        )

    prompt = gr.Textbox(
        label="Content Idea",
        placeholder=(
            "Example: A young entrepreneur building a successful "
            "business in Lagos..."
        ),
        lines=5,
    )

    style = gr.Dropdown(
        choices=[
            "Realistic",
            "Fantasy",
            "Anime",
            "Cartoon",
            "Oil Painting",
            "Watercolour",
        ],
        value="Realistic",
        label="Image Style",
    )

    voice = gr.Dropdown(
        choices=[
            "English Female",
            "English Male",
            "British Female",
            "British Male",
        ],
        value="English Female",
        label="Narration Voice",
    )

    music_style = gr.Dropdown(
        choices=[
            "Cinematic",
            "Calm",
            "Upbeat",
            "Ambient",
        ],
        value="Cinematic",
        label="Music Style",
    )

    music_duration = gr.Dropdown(
        choices=[
            5,
            10,
            15,
            20,
            30,
        ],
        value=10,
        label="Music Duration (seconds)",
    )

    generate_btn = gr.Button(
        "🚀 Create Complete Content",
        variant="primary",
    )

    status = gr.Markdown("🟢 Ready")

    gr.Markdown("## 🖼 Generated Image")

    image = gr.Image(
        label="Image",
        type="filepath",
        height=350,
    )

    gr.Markdown("## 🎬 Generated Video")

    video = gr.Video(
        label="Video",
        height=350,
    )

    gr.Markdown("## 🎙 Generated Voice")

    voice_audio = gr.Audio(
        label="Voice",
        type="filepath",
    )

    gr.Markdown("## 🎵 Generated Music")

    music_audio = gr.Audio(
        label="Music",
        type="filepath",
    )

    def run_composer(
        prompt_value,
        style_value,
        voice_value,
        music_style_value,
        duration_value,
    ):

        if not prompt_value or not prompt_value.strip():

            return (
                None,
                None,
                None,
                None,
                "❌ Please enter a content idea.",
            )

        try:

            package = create_content_package(
                prompt=prompt_value,
                style=style_value,
                voice=voice_value,
                music_style=music_style_value,
                music_duration=duration_value,
            )

            return (
                package["image"],
                package["video"],
                package["voice"],
                package["music"],
                "✅ Complete content package generated!",
            )

        except Exception as error:

            return (
                None,
                None,
                None,
                None,
                f"❌ {error}",
            )

    generate_btn.click(
        fn=run_composer,
        inputs=[
            prompt,
            style,
            voice,
            music_style,
            music_duration,
        ],
        outputs=[
            image,
            video,
            voice_audio,
            music_audio,
            status,
        ],
    )

    return (
        prompt,
        style,
        voice,
        music_style,
        music_duration,
        generate_btn,
        image,
        video,
        voice_audio,
        music_audio,
        status,
    )