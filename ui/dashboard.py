import gradio as gr

from core.image_generator import generate_image
from utils.file_manager import get_saved_images

from ui.sidebar import create_sidebar
from ui.gallery_panel import create_gallery_panel
from ui.image_generator_panel import create_image_generator_panel


def on_generate(prompt, style):
    if not prompt.strip():
        return None, "❌ Please enter a prompt.", [], None

    full_prompt = f"{style}, {prompt}"

    image_path = generate_image(full_prompt)

    images = get_saved_images()

    return (
        image_path,
        "✅ Image generated successfully!",
        images,
        image_path,
    )


def create_dashboard():

    with gr.Blocks(title="Personal AI Studio") as app:

        gr.Markdown("# 🧠 Personal AI Studio")
        gr.Markdown("### Create AI images with ease")
        gr.Markdown("## 🖼 Image Generator")

        with gr.Row():

            (
                image_btn,
                video_btn,
                music_btn,
                voice_btn,
                gallery_btn,
                settings_btn,
            ) = create_sidebar()

            with gr.Column(scale=3):

                (
                    prompt,
                    style,
                    generate_btn,
                    image,
                    download,
                    status,
                ) = create_image_generator_panel()

                gallery = create_gallery_panel()

                gallery_btn.click(
                    fn=get_saved_images,
                    outputs=gallery,
                )

                generate_btn.click(
                    fn=on_generate,
                    inputs=[prompt, style],
                    outputs=[
                        image,
                        status,
                        gallery,
                        download,
                    ],
                )

    return app