import requests
from pathlib import Path
from datetime import datetime


def generate(prompt):

    url = f"https://image.pollinations.ai/prompt/{prompt}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Image generation failed.")

    Path("images").mkdir(exist_ok=True)

    filename = (
        "images/"
        + datetime.now().strftime("image_%Y%m%d_%H%M%S.jpg")
    )

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename