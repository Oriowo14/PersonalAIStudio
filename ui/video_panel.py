import gradio as gr

from core.video_generator import get_available_images


def create_video_panel():

    images = get_available_images()

    gr.Markdown("# 🎬 Video Studio")

    gr.Markdown(
        """
Generate short AI videos from your AI-generated images.

Choose one of your generated images below.
"""
    )

    image_selector = gr.Dropdown(
        choices=images,
        value=images[0] if images else None,
        label="Select Generated Image"
    )

    generate_video_btn = gr.Button(
        "🎬 Generate Video",
        variant="primary"
    )

    video = gr.Video(
        label="Video Preview",
        height=400
    )

    status = gr.Markdown("🟢 Ready")

    return (
        image_selector,
        generate_video_btn,
        video,
        status,
    )