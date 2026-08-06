from pathlib import Path
from moviepy import ImageClip


def get_available_images():
    """
    Returns all generated images sorted by newest first.
    """
    images_folder = Path("images")

    if not images_folder.exists():
        return []

    image_files = []

    for extension in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
        image_files.extend(images_folder.glob(extension))

    image_files.sort(
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    return [str(image) for image in image_files]


def generate_video(image_path):
    """
    Generate a simple MP4 video from a still image.
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(image_path)

    videos_folder = Path("videos")
    videos_folder.mkdir(exist_ok=True)

    output_path = videos_folder / f"{image_path.stem}.mp4"

    clip = (
        ImageClip(str(image_path))
        .with_duration(5)
        .resized(height=720)
    )

    clip.write_videofile(
        str(output_path),
        fps=24,
        codec="libx264",
        audio=False,
        logger=None
    )

    return str(output_path)