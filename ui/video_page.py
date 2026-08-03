import gradio as gr


def create_video_page():

    with gr.Column():

        gr.Markdown("## 🎬 AI Video Generator")

        image = gr.Image(
            label="Image to Animate",
            type="filepath"
        )

        generate_btn = gr.Button(
            "🎬 Create Video",
            variant="primary"
        )

        video = gr.Video(
            label="Generated Video"
        )

        status = gr.Markdown(
            "🚧 Video generation coming soon..."
        )