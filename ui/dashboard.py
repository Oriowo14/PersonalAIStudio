import gradio as gr

from core.image_generator import generate_image
from utils.file_manager import get_saved_images

from ui.image_generator_panel import create_image_generator_panel
from ui.video_panel import create_video_panel
from ui.gallery_panel import create_gallery_panel
from ui.settings_panel import create_settings_panel
from ui.prompt_assistant_panel import create_prompt_assistant_panel
from ui.voice_panel import create_voice_panel
from ui.music_panel import create_music_panel
from ui.content_composer_panel import create_content_composer_panel


def on_generate(prompt, style):
    if not prompt.strip():
        return None, "❌ Please enter a prompt.", [], None

    image_path = generate_image(f"{style}, {prompt}")
    images = get_saved_images()

    return (
        image_path,
        "✅ Image generated successfully!",
        images,
        image_path,
    )


def create_dashboard():

    with gr.Blocks(
        title="Personal AI Studio"
    ) as app:

        gr.Markdown("# 🧠 Personal AI Studio")
        gr.Markdown(
            "### Your Complete AI Content Creation Studio"
        )

        with gr.Tabs():

            # -------------------------------------------------
            # CONTENT COMPOSER
            # -------------------------------------------------

            with gr.Tab("🚀 Content Composer"):

                create_content_composer_panel()

            # -------------------------------------------------
            # IMAGE STUDIO
            # -------------------------------------------------

            with gr.Tab("🖼 Image Studio"):

                (
                    prompt,
                    style,
                    generate_btn,
                    image,
                    download,
                    status,
                ) = create_image_generator_panel()

                gallery = create_gallery_panel()

                generate_btn.click(
                    fn=on_generate,
                    inputs=[
                        prompt,
                        style,
                    ],
                    outputs=[
                        image,
                        status,
                        gallery,
                        download,
                    ],
                )

            # -------------------------------------------------
            # VIDEO STUDIO
            # -------------------------------------------------

            with gr.Tab("🎬 Video Studio"):

                (
                    image_selector,
                    motion_style,
                    duration,
                    generate_video_btn,
                    video,
                    video_download,
                    video_status,
                ) = create_video_panel()

            # -------------------------------------------------
            # PROMPT ASSISTANT
            # -------------------------------------------------

            with gr.Tab("✨ Prompt Assistant"):

                create_prompt_assistant_panel()

            # -------------------------------------------------
            # VOICE STUDIO
            # -------------------------------------------------

            with gr.Tab("🎙 Voice Studio"):

                create_voice_panel()

            # -------------------------------------------------
            # MUSIC STUDIO
            # -------------------------------------------------

            with gr.Tab("🎵 Music Studio"):

                create_music_panel()

            # -------------------------------------------------
            # SETTINGS
            # -------------------------------------------------

            with gr.Tab("⚙️ Settings"):

                create_settings_panel()

    return app