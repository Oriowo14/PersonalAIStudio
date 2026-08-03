from ui.sidebar import create_sidebar
from utils.file_manager import get_saved_images
import gradio as gr
from core.image_generator import generate_image


def on_generate(prompt, style):
    if not prompt.strip():
        return None, "❌ Please enter a prompt.", []

    full_prompt = f"{style}, {prompt}"
    image_path = generate_image(full_prompt)

    images = get_saved_images()

    return image_path, "✅ Image generated successfully!", images, image_path


def create_dashboard():

    with gr.Blocks(title="Personal AI Studio") as app:

        gr.Markdown("# 🧠 Personal AI Studio")
        gr.Markdown("### Create AI images with ease")

        with gr.Row():

            # Left panel
            create_sidebar()

            # Right panel
            with gr.Column(scale=3):

                prompt = gr.Textbox(
                    label="Describe your image",
                    placeholder="Example: A futuristic African city at sunset..."
                )

                style = gr.Dropdown(
                    choices=[
                        "Realistic",
                        "Fantasy",
                        "Anime",
                        "Cartoon",
                        "Oil Painting",
                        "Watercolour"
                    ],
                    value="Realistic",
                    label="Style"
                )

                generate_btn = gr.Button(
                    "🚀 Generate Image",
                    variant="primary"
                )

                image = gr.Image(
    label="Generated Image",
    type="filepath"
)
                download = gr.File(
    label="📥 Download Image"
)

                status = gr.Markdown("🟢 Ready")

                gr.Markdown("## 📂 Recent Images")

                gallery = gr.Gallery(
                    label="Generated Images",
                    columns=3,
                    height=300
                )

                generate_btn.click(
                    fn=on_generate,
                    inputs=[prompt, style],
                    outputs=[image, status, gallery, download]
                )

    return app