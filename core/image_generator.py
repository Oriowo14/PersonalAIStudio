import os
import requests
from urllib.parse import quote
from datetime import datetime


def generate_image(prompt):
    os.makedirs("images", exist_ok=True)

    # Create a unique filename using the current date and time
    filename = datetime.now().strftime("image_%Y%m%d_%H%M%S.png")
    filepath = os.path.join("images", filename)

    prompt = quote(prompt)

    url = f"https://image.pollinations.ai/prompt/{prompt}"

    response = requests.get(
        url,
        timeout=120,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    print("Status Code:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))

    if response.status_code != 200:
        raise Exception(f"Image generation failed: {response.status_code}")

    if not response.headers.get("Content-Type", "").startswith("image/"):
        raise Exception("The server did not return an image.")

    with open(filepath, "wb") as f:
        f.write(response.content)

    return filepath