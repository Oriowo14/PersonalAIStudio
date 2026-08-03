def on_generate(prompt, style):

    if not prompt.strip():
        return None, "❌ Please enter a prompt.", []

    full_prompt = f"{style}, {prompt}"

    image = generate_image(full_prompt)

    images = get_saved_images()

    return image, "✅ Image generated successfully!", images