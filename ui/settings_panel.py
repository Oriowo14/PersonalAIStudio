import gradio as gr

from config import load_config, save_config


def save_settings(provider):

    config = load_config()

    config["image_provider"] = provider

    save_config(config)

    return f"✅ Provider changed to: {provider}"


def create_settings_panel():

    config = load_config()

    gr.Markdown("# ⚙️ Settings")

    provider = gr.Radio(
        choices=[
            "pollinations",
        ],
        value=config["image_provider"],
        label="Image Provider",
    )

    save_btn = gr.Button(
        "💾 Save Settings",
        variant="primary",
    )

    status = gr.Markdown("")

    save_btn.click(
        fn=save_settings,
        inputs=provider,
        outputs=status,
    )

    return (
        provider,
        save_btn,
        status,
    )