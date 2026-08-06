from config import load_config

from providers.pollinations import generate as pollinations_generate


def generate_image(prompt):
    """
    Generate an image using the configured provider.
    """

    config = load_config()

    provider = config.get("image_provider", "pollinations")

    if provider == "pollinations":
        return pollinations_generate(prompt)

    raise ValueError(f"Unknown provider: {provider}")