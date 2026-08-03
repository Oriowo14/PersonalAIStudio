import os

def get_saved_images():
    folder = "images"

    if not os.path.exists(folder):
        return []

    files = []

    for file in os.listdir(folder):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            files.append(os.path.join(folder, file))

    files.sort(reverse=True)

    return files