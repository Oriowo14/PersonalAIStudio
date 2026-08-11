import gradio as gr

from core.voice_generator import (
    generate_voice,
    get_available_voices,
)


def create_voice_panel():

    gr.Markdown("# 🎙 Voice Studio")

    gr.Markdown(
        """
Turn your text into natural-sounding speech.

Enter your narration, choose a voice, and generate an audio file.
"""
    )

    text = gr.Textbox(
        label="Narration",
        placeholder=(
            "Example: Welcome to Personal AI Studio. "
            "Create amazing content with AI."
        ),
        lines=8,
    )

    voice = gr.Dropdown(
        choices=get_available_voices(),
        value="English Female",
        label="Voice",
    )

    generate_btn = gr.Button(
        "🎙 Generate Voice",
        variant="primary",
    )

    audio = gr.Audio(
        label="Audio Preview",
        type="filepath",
    )

    download = gr.File(
        label="📥 Download Voice",
    )

    status = gr.Markdown("🟢 Ready")

    def generate_voice_with_status(text_value, voice_value):
        try:
            audio_path = generate_voice(
                text_value,
                voice_value,
            )

            return (
                audio_path,
                audio_path,
                "✅ Voice generated successfully!",
            )

        except Exception as error:
            return (
                None,
                None,
                f"❌ {error}",
            )

    generate_btn.click(
        fn=generate_voice_with_status,
        inputs=[text, voice],
        outputs=[audio, download, status],
    )

    return (
        text,
        voice,
        generate_btn,
        audio,
        download,
        status,
    )