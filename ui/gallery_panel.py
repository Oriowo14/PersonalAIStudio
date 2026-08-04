import gradio as gr
from utils.file_manager import get_saved_images


def create_gallery_panel():
    gr.Markdown("## 📂 Recent Images")

    gallery = gr.Gallery(
        label="Saved Images",
        columns=4,
        height=250
    )

    refresh_btn = gr.Button("🔄 Refresh Gallery")

    refresh_btn.click(
        fn=get_saved_images,
        outputs=gallery
    )

    return gallery