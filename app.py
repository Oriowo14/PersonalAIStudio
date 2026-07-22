import gradio as gr

from image_generator import generate_image


def create_image(prompt):
    return generate_image(prompt)


app = gr.Interface(
    fn=create_image,
    inputs=gr.Textbox(
        label="Describe the image you want",
        placeholder="Example: A futuristic city at sunset with flying cars"
    ),
    outputs=gr.Image(
        label="Generated Image"
    ),
    title="🎨 Personal AI Studio",
    description="Generate AI images from your imagination."
)

app.launch()
