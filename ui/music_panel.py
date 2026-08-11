import gradio as gr

from core.music_generator import (
    generate_music,
    get_available_music_styles,
)


def create_music_panel():

    gr.Markdown("# 🎵 Music Studio")

    gr.Markdown(
        """
Create an original musical background track for your AI content.

Choose a style and duration, then generate your music.
"""
    )

    style = gr.Dropdown(
        choices=get_available_music_styles(),
        value="Cinematic",
        label="Music Style",
    )

    duration = gr.Dropdown(
        choices=[
            5,
            10,
            15,
            20,
            30,
        ],
        value=10,
        label="Duration (seconds)",
    )

    generate_btn = gr.Button(
        "🎵 Generate Music",
        variant="primary",
    )

    audio = gr.Audio(
        label="Music Preview",
        type="filepath",
    )

    download = gr.File(
        label="📥 Download Music",
    )

    status = gr.Markdown("🟢 Ready")

    def generate_music_with_status(style_value, duration_value):

        try:
            audio_path = generate_music(
                style_value,
                duration_value,
            )

            return (
                audio_path,
                audio_path,
                "✅ Music generated successfully!",
            )

        except Exception as error:

            return (
                None,
                None,
                f"❌ {error}",
            )

    generate_btn.click(
        fn=generate_music_with_status,
        inputs=[
            style,
            duration,
        ],
        outputs=[
            audio,
            download,
            status,
        ],
    )

    return (
        style,
        duration,
        generate_btn,
        audio,
        download,
        status,
    )