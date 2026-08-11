import gradio as gr

from config import load_config
from core.video_generator import (
    generate_video,
    get_available_images,
    get_motion_styles,
)


def create_video_panel():

    images = get_available_images()

    config = load_config()

    video_provider = config.get(
        "video_provider",
        "local",
    )

    gr.Markdown("# 🎬 Video Studio")

    if video_provider == "pollinations":

        gr.Markdown(
            """
### 🤖 AI Motion Mode

Pollinations AI Motion creates genuine image-to-video
movement. It requires available Pollen balance.
"""
        )

        duration_choices = [
            6,
            12,
            18,
            24,
        ]

        default_duration = 6

    else:

        gr.Markdown(
            """
### 🆓 Local Motion Mode

Local Motion is free and creates cinematic camera
movement from your generated images.
"""
        )

        duration_choices = [
            5,
            10,
            15,
            20,
        ]

        default_duration = 5

    provider_status = gr.Markdown(
        f"**Current Video Provider:** `{video_provider}`"
    )

    image_selector = gr.Dropdown(
        choices=images,
        value=images[0] if images else None,
        label="Select Generated Image",
    )

    motion_style = gr.Dropdown(
        choices=get_motion_styles(),
        value="Zoom In",
        label="Motion Style",
    )

    duration = gr.Dropdown(
        choices=duration_choices,
        value=default_duration,
        label="Duration (seconds)",
    )

    generate_video_btn = gr.Button(
        "🎬 Generate Video",
        variant="primary",
    )

    video = gr.Video(
        label="Video Preview",
        height=400,
    )

    download = gr.File(
        label="📥 Download Video",
    )

    status = gr.Markdown("🟢 Ready")

    def generate_video_with_status(
        image_path,
        motion_value,
        duration_value,
    ):

        if not image_path:

            return (
                None,
                None,
                "❌ Please select an image first.",
            )

        try:

            video_path = generate_video(
                image_path,
                motion_value,
                duration_value,
            )

            return (
                video_path,
                video_path,
                "✅ Video generated successfully!",
            )

        except Exception as error:

            return (
                None,
                None,
                f"❌ {error}",
            )

    generate_video_btn.click(
        fn=generate_video_with_status,
        inputs=[
            image_selector,
            motion_style,
            duration,
        ],
        outputs=[
            video,
            download,
            status,
        ],
    )

    return (
        image_selector,
        motion_style,
        duration,
        generate_video_btn,
        video,
        download,
        status,
    )