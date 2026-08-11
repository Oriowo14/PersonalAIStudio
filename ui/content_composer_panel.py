import gradio as gr

from config import load_config
from core.content_composer import create_content_package


def create_content_composer_panel():

    config = load_config()

    video_provider = config.get(
        "video_provider",
        "local",
    )

    gr.Markdown("# 🚀 AI Content Composer")

    gr.Markdown(
        """
Turn one idea into a coordinated content package.

Personal AI Studio will use your idea to create:
**Image → Video → Voice → Music**
"""
    )

    # -------------------------------------------------
    # VIDEO PROVIDER STATUS
    # -------------------------------------------------

    if video_provider == "pollinations":

        gr.Markdown(
            """
### 🤖 AI Motion Video

Pollinations AI Motion is selected.

It can create genuine movement in the subject,
but requires available Pollen balance.
"""
        )

    else:

        gr.Markdown(
            """
### 🆓 Local Motion Video

Local Motion is currently selected.

It creates free cinematic camera movement.
For genuine body/object movement, use Pollinations
AI Motion when Pollen is available.
"""
        )

    # -------------------------------------------------
    # CONTENT IDEA
    # -------------------------------------------------

    prompt = gr.Textbox(
        label="💡 Content Idea",
        placeholder=(
            "Example: A young African entrepreneur "
            "building a successful technology company in Lagos."
        ),
        lines=6,
    )

    # -------------------------------------------------
    # IMAGE STYLE
    # -------------------------------------------------

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
        label="🖼 Image Style",
    )

    # -------------------------------------------------
    # VOICE
    # -------------------------------------------------

    voice = gr.Dropdown(
        choices=[
            "English Female",
            "English Male",
            "British Female",
            "British Male",
        ],
        value="English Female",
        label="🎙 Narration Voice",
    )

    # -------------------------------------------------
    # MUSIC
    # -------------------------------------------------

    music_style = gr.Dropdown(
        choices=[
            "Cinematic",
            "Calm",
            "Upbeat",
            "Ambient",
        ],
        value="Cinematic",
        label="🎵 Music Style",
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
        label="🎵 Music Duration (seconds)",
    )

    # -------------------------------------------------
    # GENERATE
    # -------------------------------------------------

    generate_btn = gr.Button(
        "🚀 Create Complete Content",
        variant="primary",
    )

    status = gr.Markdown(
        "🟢 Ready"
    )

    # -------------------------------------------------
    # IMAGE OUTPUT
    # -------------------------------------------------

    gr.Markdown(
        "## 🖼 Generated Image"
    )

    image = gr.Image(
        label="Generated Image",
        type="filepath",
        height=350,
    )

    # -------------------------------------------------
    # VIDEO OUTPUT
    # -------------------------------------------------

    gr.Markdown(
        "## 🎬 Generated Video"
    )

    video = gr.Video(
        label="Generated Video",
        height=350,
    )

    # -------------------------------------------------
    # VOICE OUTPUT
    # -------------------------------------------------

    gr.Markdown(
        "## 🎙 Generated Voice"
    )

    voice_audio = gr.Audio(
        label="Voice Narration",
        type="filepath",
    )

    # -------------------------------------------------
    # MUSIC OUTPUT
    # -------------------------------------------------

    gr.Markdown(
        "## 🎵 Generated Music"
    )

    music_audio = gr.Audio(
        label="Background Music",
        type="filepath",
    )

    # -------------------------------------------------
    # GENERATION FUNCTION
    # -------------------------------------------------

    def run_composer(
        prompt_value,
        style_value,
        voice_value,
        music_style_value,
        duration_value,
    ):

        if (
            not prompt_value
            or not prompt_value.strip()
        ):

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
                "✅ Complete content package generated successfully!",
            )

        except Exception as error:

            return (
                None,
                None,
                None,
                None,
                f"❌ {error}",
            )

    # -------------------------------------------------
    # BUTTON EVENT
    # -------------------------------------------------

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