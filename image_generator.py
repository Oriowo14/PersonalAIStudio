import os
import requests
from urllib.parse import quote

def generate_image(prompt):
    os.makedirs("images", exist_ok=True)

    filename = "images/generated.png"

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
        print(response.text[:500])
        raise Exception("The server did not return an image.")

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename