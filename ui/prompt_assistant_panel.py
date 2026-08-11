import gradio as gr


def enhance_prompt(prompt, style):
    if not prompt or not prompt.strip():
        return ""

    prompt = prompt.strip()

    style_details = {
        "Realistic": (
            "photorealistic, natural lighting, realistic textures, "
            "detailed environment, professional photography"
        ),
        "Fantasy": (
            "epic fantasy atmosphere, magical environment, dramatic lighting, "
            "rich details, cinematic composition"
        ),
        "Anime": (
            "anime art style, expressive details, vibrant composition, "
            "beautiful background, polished illustration"
        ),
        "Cartoon": (
            "stylized cartoon art, expressive characters, clean shapes, "
            "colourful environment, polished illustration"
        ),
        "Oil Painting": (
            "traditional oil painting, rich brushwork, textured canvas, "
            "dramatic composition, fine artistic detail"
        ),
        "Watercolour": (
            "delicate watercolour painting, soft brushwork, flowing colours, "
            "artistic paper texture, atmospheric detail"
        ),
    }

    details = style_details.get(
        style,
        "highly detailed, beautiful composition, professional quality"
    )

    enhanced = (
        f"{prompt}. "
        f"{details}, "
        f"carefully composed scene, strong subject focus, "
        f"high visual quality, detailed background."
    )

    return enhanced


def create_prompt_assistant_panel():

    gr.Markdown("## ✨ Prompt Assistant")

    gr.Markdown(
        "Turn a simple idea into a richer image-generation prompt."
    )

    assistant_prompt = gr.Textbox(
        label="Your Simple Idea",
        placeholder="Example: Someone riding a horse",
        lines=3,
    )

    assistant_style = gr.Dropdown(
        choices=[
            "Realistic",
            "Fantasy",
            "Anime",
            "Cartoon",
            "Oil Painting",
            "Watercolour",
        ],
        value="Realistic",
        label="Preferred Style",
    )

    enhance_btn = gr.Button(
        "✨ Enhance Prompt",
        variant="primary",
    )

    enhanced_prompt = gr.Textbox(
        label="Enhanced Prompt",
        lines=6,
    )

    enhance_btn.click(
        fn=enhance_prompt,
        inputs=[assistant_prompt, assistant_style],
        outputs=enhanced_prompt,
    )

    return (
        assistant_prompt,
        assistant_style,
        enhance_btn,
        enhanced_prompt,
    )