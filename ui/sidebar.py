import gradio as gr


def create_sidebar():
    with gr.Column(scale=1):

        gr.Markdown("## 🧰 AI Tools")

        image_btn = gr.Button("🖼 Image Generator", variant="primary")
        video_btn = gr.Button("🎬 Video Generator")
        music_btn = gr.Button("🎵 Music Generator")
        voice_btn = gr.Button("🎙 Voice Generator")
        gallery_btn = gr.Button("📂 Gallery")
        settings_btn = gr.Button("⚙️ Settings")

    return (
        image_btn,
        video_btn,
        music_btn,
        voice_btn,
        gallery_btn,
        settings_btn,
    )