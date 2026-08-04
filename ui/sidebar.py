import gradio as gr


def create_sidebar():
    with gr.Column(scale=1):
        gr.Markdown("## 🧰 AI Tools")

        gr.Button("🖼 Image Generator", interactive=False)
        gr.Button("🎬 Video Generator", interactive=False)
        gr.Button("🎵 Music Generator", interactive=False)
        gr.Button("🎙 Voice Generator", interactive=False)
        gr.Button("📂 Gallery", interactive=False)
        gr.Button("⚙️ Settings", interactive=False)