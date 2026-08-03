import gradio as gr

from core.image_generator import generate_image
from utils.file_manager import get_saved_images


def on_generate(prompt, style, aspect_ratio):
    if not prompt.strip():
        return None, "❌ Please enter a prompt.", []

    # Build the prompt
    full_prompt = f"{style}, {aspect_ratio}, {prompt}"

    # Generate image
    image_path = generate_image(full_prompt)

    # Reload gallery
    images = get_saved_images()

    return image_path, "✅ Image generated successfully!", images


def create_dashboard():

    with gr.Blocks(title="Personal AI Studio") as app:

        gr.Markdown("# 🧠 Personal AI Studio")
        gr.Markdown("### Create AI Images with Ease")

        with gr.Row():

            # =========================
            # Left Sidebar
            # =========================
            with gr.Column(scale=1):

                gr.Markdown("## 🧰 AI Tools")

                gr.Button("🖼 Image Generator", interactive=False)
                gr.Button("🎬 Video Generator", interactive=False)
                gr.Button("🎵 Music Generator", interactive=False)
                gr.Button("🎙 Voice Generator", interactive=False)
                gr.Button("📂 Gallery", interactive=False)
                gr.Button("⚙ Settings", interactive=False)

            # =========================
            # Main Content
            # =========================
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

                aspect_ratio = gr.Dropdown(
                    choices=[
                        "Square (1:1)",
                        "Portrait (2:3)",
                        "Landscape (16:9)"
                    ],
                    value="Square (1:1)",
                    label="Aspect Ratio"
                )

                generate_btn = gr.Button(
                    "🚀 Generate Image",
                    variant="primary"
                )

                image = gr.Image(
                    label="Generated Image"
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
                    inputs=[prompt, style, aspect_ratio],
                    outputs=[image, status, gallery]
                )

    return app