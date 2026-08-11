from pathlib import Path
import asyncio
import edge_tts


VOICE_MAP = {
    "English Female": "en-US-AriaNeural",
    "English Male": "en-US-GuyNeural",
    "British Female": "en-GB-SoniaNeural",
    "British Male": "en-GB-RyanNeural",
}


def get_available_voices():
    """
    Return the voices currently available in the Voice Studio.
    """
    return list(VOICE_MAP.keys())


async def _generate_speech(text, voice, output_path):
    """
    Generate speech asynchronously with Edge TTS.
    """
    communicator = edge_tts.Communicate(
        text=text,
        voice=voice,
    )

    await communicator.save(str(output_path))


def generate_voice(text, voice_name):
    """
    Generate an MP3 voice file from text.
    """

    if not text or not text.strip():
        raise ValueError("Please enter some text.")

    if voice_name not in VOICE_MAP:
        raise ValueError(f"Unknown voice: {voice_name}")

    voices_folder = Path("outputs") / "voice"
    voices_folder.mkdir(parents=True, exist_ok=True)

    output_path = voices_folder / "generated_voice.mp3"

    voice = VOICE_MAP[voice_name]

    asyncio.run(
        _generate_speech(
            text.strip(),
            voice,
            output_path,
        )
    )

    return str(output_path)