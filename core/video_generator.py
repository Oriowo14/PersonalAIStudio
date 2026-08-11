from pathlib import Path
import os

import numpy as np
import requests
from dotenv import load_dotenv
from PIL import Image
import imageio.v2 as imageio

from config import load_config


load_dotenv()


LOCAL_MOTION_STYLES = [
    "Zoom In",
    "Zoom Out",
    "Pan Left",
    "Pan Right",
]


VIDEO_PROVIDERS = [
    "local",
    "pollinations",
]


def get_video_providers():
    """Return available video providers."""
    return VIDEO_PROVIDERS


def get_available_images():
    """
    Return generated images sorted from newest to oldest.
    """

    images_folder = Path("images")

    if not images_folder.exists():
        return []

    image_files = []

    for extension in (
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.webp",
    ):
        image_files.extend(
            images_folder.glob(extension)
        )

    image_files.sort(
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )

    return [str(image) for image in image_files]


def get_motion_styles():
    """
    Return available local cinematic motion styles.
    """

    return LOCAL_MOTION_STYLES


def _resize_and_crop(image, width, height, zoom=1.0):

    image = image.convert("RGB")

    source_width, source_height = image.size

    target_width = int(width * zoom)
    target_height = int(height * zoom)

    scale = max(
        target_width / source_width,
        target_height / source_height,
    )

    resized_width = int(source_width * scale)
    resized_height = int(source_height * scale)

    image = image.resize(
        (resized_width, resized_height),
        Image.Resampling.LANCZOS,
    )

    left = max(
        (resized_width - target_width) // 2,
        0,
    )

    top = max(
        (resized_height - target_height) // 2,
        0,
    )

    right = left + target_width
    bottom = top + target_height

    image = image.crop(
        (left, top, right, bottom)
    )

    image = image.resize(
        (width, height),
        Image.Resampling.LANCZOS,
    )

    return np.asarray(image)


def _create_frame(
    image,
    width,
    height,
    progress,
    motion_style,
):

    if motion_style == "Zoom In":

        zoom = 1.0 + (0.12 * progress)

        return _resize_and_crop(
            image,
            width,
            height,
            zoom,
        )

    if motion_style == "Zoom Out":

        zoom = 1.12 - (0.12 * progress)

        return _resize_and_crop(
            image,
            width,
            height,
            zoom,
        )

    zoom = 1.10

    image_rgb = image.convert("RGB")

    source_width, source_height = image_rgb.size

    scale = max(
        (width * zoom) / source_width,
        (height * zoom) / source_height,
    )

    enlarged_width = int(source_width * scale)
    enlarged_height = int(source_height * scale)

    enlarged = image_rgb.resize(
        (enlarged_width, enlarged_height),
        Image.Resampling.LANCZOS,
    )

    max_x = max(
        enlarged_width - width,
        0,
    )

    max_y = max(
        enlarged_height - height,
        0,
    )

    if motion_style == "Pan Left":

        x = int(max_x * (1.0 - progress))

    else:

        x = int(max_x * progress)

    y = max_y // 2

    frame = enlarged.crop(
        (
            x,
            y,
            x + width,
            y + height,
        )
    )

    frame = frame.resize(
        (width, height),
        Image.Resampling.LANCZOS,
    )

    return np.asarray(frame)


def _generate_local_video(
    image_path,
    motion_style="Zoom In",
    duration=5,
):

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    if motion_style not in LOCAL_MOTION_STYLES:
        raise ValueError(
            f"Unknown motion style: {motion_style}"
        )

    duration = float(duration)

    if duration <= 0:
        raise ValueError(
            "Duration must be greater than zero."
        )

    if duration > 30:
        raise ValueError(
            "Maximum local video duration is 30 seconds."
        )

    image = Image.open(image_path).convert("RGB")

    width = 768
    height = 432

    fps = 24
    total_frames = int(duration * fps)

    videos_folder = Path("videos")
    videos_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        videos_folder
        / f"{image_path.stem}_local_motion.mp4"
    )

    writer = imageio.get_writer(
        str(output_path),
        fps=fps,
        codec="libx264",
        quality=8,
    )

    try:

        for frame_number in range(total_frames):

            if total_frames <= 1:
                progress = 0
            else:
                progress = frame_number / (
                    total_frames - 1
                )

            frame = _create_frame(
                image=image,
                width=width,
                height=height,
                progress=progress,
                motion_style=motion_style,
            )

            writer.append_data(frame)

    finally:

        writer.close()

    return str(output_path)


def _upload_image_to_pollinations(image_path):

    api_key = os.getenv("POLLINATIONS_API_KEY")

    if not api_key:
        raise RuntimeError(
            "POLLINATIONS_API_KEY is not configured."
        )

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    upload_url = "https://media.pollinations.ai/upload"

    with open(image_path, "rb") as image_file:

        response = requests.post(
            upload_url,
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            files={
                "file": (
                    image_path.name,
                    image_file,
                    "image/png",
                )
            },
            timeout=120,
        )

    if response.status_code == 402:

        raise RuntimeError(
            "Pollinations AI Motion requires available Pollen. "
            "Your current Pollinations balance is zero."
        )

    if not response.ok:

        raise RuntimeError(
            f"Pollinations image upload failed "
            f"({response.status_code}): "
            f"{response.text}"
        )

    data = response.json()

    image_url = data.get("url")

    if not image_url:
        raise RuntimeError(
            "Pollinations upload did not return an image URL."
        )

    return image_url


def _generate_pollinations_video(
    image_path,
    motion_style="Zoom In",
    duration=6,
):

    api_key = os.getenv("POLLINATIONS_API_KEY")

    if not api_key:
        raise RuntimeError(
            "POLLINATIONS_API_KEY is not configured."
        )

    duration = int(duration)

    if duration < 6:
        duration = 6

    if duration > 120:
        duration = 120

    # nova-reel requires durations in multiples of 6.
    duration = (duration // 6) * 6

    if duration == 0:
        duration = 6

    image_url = _upload_image_to_pollinations(
        image_path
    )

    motion_instruction = {
        "Zoom In": (
            "The camera moves gently forward while "
            "the subject naturally moves."
        ),
        "Zoom Out": (
            "The camera slowly pulls back while "
            "the subject naturally moves."
        ),
        "Pan Left": (
            "The camera moves gently left while "
            "the subject naturally moves."
        ),
        "Pan Right": (
            "The camera moves gently right while "
            "the subject naturally moves."
        ),
    }.get(
        motion_style,
        "Natural cinematic movement.",
    )

    prompt = (
        "Animate the reference image into a realistic video. "
        "Preserve the identity, appearance, clothing, environment "
        "and overall composition of the subject. "
        "Create natural human movement where appropriate: "
        "subtle body movement, natural head movement, blinking, "
        "realistic hand and arm movement, and natural posture changes. "
        f"{motion_instruction} "
        "Avoid frozen subjects, distorted hands, extra limbs, "
        "identity changes, and unnatural movement."
    )

    video_url = (
        "https://gen.pollinations.ai/video/"
        + requests.utils.quote(
            prompt,
            safe="",
        )
    )

    response = requests.get(
        video_url,
        params={
            "model": "nova-reel",
            "duration": duration,
            "image": image_url,
            "aspectRatio": "16:9",
            "audio": False,
        },
        headers={
            "Authorization": f"Bearer {api_key}",
        },
        timeout=1200,
    )

    if response.status_code == 402:

        raise RuntimeError(
            "Pollinations AI Motion requires available Pollen. "
            "Your current Pollinations balance is zero."
        )

    if not response.ok:

        raise RuntimeError(
            f"Pollinations video generation failed "
            f"({response.status_code}): "
            f"{response.text}"
        )

    videos_folder = Path("videos")
    videos_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        videos_folder
        / f"{Path(image_path).stem}_ai_motion.mp4"
    )

    output_path.write_bytes(
        response.content
    )

    return str(output_path)


def generate_video(
    image_path,
    motion_style="Zoom In",
    duration=5,
):
    """
    Generate video using the configured provider.

    Default provider is local motion because it is free.
    Pollinations provides genuine AI image-to-video when
    the account has available Pollen.
    """

    config = load_config()

    provider = config.get(
        "video_provider",
        "local",
    )

    if provider == "local":

        return _generate_local_video(
            image_path,
            motion_style,
            duration,
        )

    if provider == "pollinations":

        return _generate_pollinations_video(
            image_path,
            motion_style,
            duration,
        )

    raise ValueError(
        f"Unknown video provider: {provider}"
    )