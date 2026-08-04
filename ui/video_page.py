import gradio as gr


def create_video_panel():
    with gr.Column():
        gr.Markdown("# 🎬 Video Generator")
        gr.Markdown(
            """
            ## 🚧 Coming Soon

            This workspace will allow you to:

            ✅ Generate videos from AI images

            ✅ Preview MP4 videos

            ✅ Download videos

            Stay tuned!
            """
        )