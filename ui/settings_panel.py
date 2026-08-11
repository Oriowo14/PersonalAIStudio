import gradio as gr

from config import load_config, save_config


IMAGE_PROVIDERS = [
    "pollinations",
]


VIDEO_PROVIDERS = [
    "local",
    "pollinations",
]


def save_settings(
    image_provider,
    video_provider,
):

    config = load_config()

    config["image_provider"] = image_provider
    config["video_provider"] = video_provider

    save_config(config)

    return (
        "✅ Settings saved successfully!\n\n"
        f"🖼 Image Provider: `{image_provider}`\n"
        f"🎬 Video Provider: `{video_provider}`"
    )


def create_settings_panel():

    config = load_config()

    gr.Markdown("# ⚙️ Settings")

    gr.Markdown(
        "Configure the AI providers used by Personal AI Studio."
    )

    gr.Markdown("## 🖼 Image Provider")

    image_provider = gr.Radio(
        choices=IMAGE_PROVIDERS,
        value=config.get(
            "image_provider",
            "pollinations",
        ),
        label="Image Provider",
    )

    gr.Markdown("## 🎬 Video Provider")

    video_provider = gr.Radio(
        choices=VIDEO_PROVIDERS,
        value=config.get(
            "video_provider",
            "local",
        ),
        label="Video Provider",
    )

    gr.Markdown(
        """
**Local:** Free cinematic camera motion.

**Pollinations:** AI image-to-video with actual subject
movement. Requires available Pollen balance.
"""
    )

    save_btn = gr.Button(
        "💾 Save Settings",
        variant="primary",
    )

    status = gr.Markdown("")

    save_btn.click(
        fn=save_settings,
        inputs=[
            image_provider,
            video_provider,
        ],
        outputs=status,
    )

    return (
        image_provider,
        video_provider,
        save_btn,
        status,
    )