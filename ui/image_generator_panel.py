import gradio as gr


def create_image_generator_panel():

    prompt = gr.Textbox(
        label="Describe your image",
        placeholder="Example: A futuristic African city at sunset..."
    )

    style = gr.Dropdown(
        choices=[
            "Realistic",
            "Fantasy",
            "Anime",
            "Cartoon",
            "Oil Painting",
            "Watercolour"
        ],
        value="Realistic",
        label="Style"
    )

    generate_btn = gr.Button(
        "🚀 Generate Image",
        variant="primary"
    )

    image = gr.Image(
        label="Generated Image",
        type="filepath",
        height=450
    )

    download = gr.File(
        label="📥 Download Image"
    )

    status = gr.Markdown("🟢 Ready")

    return (
        prompt,
        style,
        generate_btn,
        image,
        download,
        status,
    )