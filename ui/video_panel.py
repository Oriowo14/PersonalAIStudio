import gradio as gr


def create_video_panel():

    gr.Markdown("# 🎬 Video Studio")

    gr.Markdown(
        """
Generate short AI videos from your generated images.

Version 2.0 will allow you to:

• Select a generated image

• Animate the image

• Preview the video

• Download the MP4
"""
    )

    image_selector = gr.Dropdown(
        choices=[],
        label="Select an Image",
        interactive=True
    )

    generate_video_btn = gr.Button(
        "🎬 Generate Video",
        variant="primary"
    )

    video = gr.Video(
        label="Generated Video",
        height=450
    )

    status = gr.Markdown("🟢 Ready")

    return (
        image_selector,
        generate_video_btn,
        video,
        status,
    )