import gradio as gr


def create_placeholder(title):
    with gr.Column():
        gr.Markdown(f"# {title}")
        gr.Markdown("🚧 This feature is under development.")