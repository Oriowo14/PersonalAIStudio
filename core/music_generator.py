from pathlib import Path
import math
import wave

import numpy as np


NOTE_FREQUENCIES = {
    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
    "B": 493.88,
}


MUSIC_STYLES = {
    "Cinematic": {
        "chords": [
            ["C", "E", "G"],
            ["A", "C", "E"],
            ["F", "A", "C"],
            ["G", "B", "D"],
        ],
        "melody": ["E", "G", "A", "G", "E", "D", "C", "E"],
    },
    "Calm": {
        "chords": [
            ["C", "E", "G"],
            ["F", "A", "C"],
            ["A", "C", "E"],
            ["G", "B", "D"],
        ],
        "melody": ["E", "G", "C", "G", "A", "C", "E", "D"],
    },
    "Upbeat": {
        "chords": [
            ["C", "E", "G"],
            ["G", "B", "D"],
            ["F", "A", "C"],
            ["G", "B", "D"],
        ],
        "melody": ["C", "E", "G", "E", "D", "G", "B", "G"],
    },
    "Ambient": {
        "chords": [
            ["C", "G", "E"],
            ["A", "E", "C"],
            ["F", "C", "A"],
            ["G", "D", "B"],
        ],
        "melody": ["G", "E", "C", "E", "A", "G", "E", "D"],
    },
}


def get_available_music_styles():
    """Return the available music styles."""
    return list(MUSIC_STYLES.keys())


def _note_wave(frequency, duration, sample_rate=44100):
    """Create a soft musical note."""
    sample_count = int(duration * sample_rate)

    t = np.linspace(
        0,
        duration,
        sample_count,
        endpoint=False,
    )

    fundamental = np.sin(2 * np.pi * frequency * t)
    harmonic_2 = 0.30 * np.sin(2 * np.pi * frequency * 2 * t)
    harmonic_3 = 0.12 * np.sin(2 * np.pi * frequency * 3 * t)

    signal = fundamental + harmonic_2 + harmonic_3

    # Smooth attack and release.
    attack = min(int(sample_rate * 0.05), sample_count)
    release = min(int(sample_rate * 0.15), sample_count)

    envelope = np.ones(sample_count)

    if attack > 0:
        envelope[:attack] = np.linspace(
            0,
            1,
            attack,
        )

    if release > 0:
        envelope[-release:] = np.linspace(
            1,
            0,
            release,
        )

    return signal * envelope


def _chord_wave(notes, duration, sample_rate=44100):
    """Create a soft chord from several notes."""
    waves = []

    for note in notes:
        waves.append(
            _note_wave(
                NOTE_FREQUENCIES[note],
                duration,
                sample_rate,
            )
        )

    chord = np.sum(waves, axis=0)

    maximum = np.max(np.abs(chord))

    if maximum > 0:
        chord = chord / maximum

    return chord


def generate_music(style="Cinematic", duration=10):
    """
    Generate a procedural music track as a WAV file.
    """

    if style not in MUSIC_STYLES:
        raise ValueError(f"Unknown music style: {style}")

    duration = float(duration)

    if duration <= 0:
        raise ValueError("Duration must be greater than zero.")

    if duration > 60:
        raise ValueError("Maximum music duration is 60 seconds.")

    sample_rate = 44100
    total_samples = int(duration * sample_rate)

    music = np.zeros(total_samples)

    style_data = MUSIC_STYLES[style]

    chord_duration = 2.0

    # Create the chord progression.
    for index, chord in enumerate(style_data["chords"]):

        start_time = index * chord_duration
        start_sample = int(start_time * sample_rate)

        if start_sample >= total_samples:
            break

        chord_audio = _chord_wave(
            chord,
            chord_duration,
            sample_rate,
        )

        end_sample = min(
            start_sample + len(chord_audio),
            total_samples,
        )

        music[start_sample:end_sample] += (
            chord_audio[:end_sample - start_sample] * 0.30
        )

    # Create a simple melody.
    melody_duration = 0.5

    for index, note in enumerate(style_data["melody"]):

        start_time = index * melody_duration
        start_sample = int(start_time * sample_rate)

        if start_sample >= total_samples:
            break

        melody_audio = _note_wave(
            NOTE_FREQUENCIES[note],
            melody_duration,
            sample_rate,
        )

        end_sample = min(
            start_sample + len(melody_audio),
            total_samples,
        )

        music[start_sample:end_sample] += (
            melody_audio[:end_sample - start_sample] * 0.45
        )

    # Add a gentle fade at the beginning and end.
    fade_length = min(
        int(sample_rate * 0.5),
        total_samples // 2,
    )

    if fade_length > 0:
        music[:fade_length] *= np.linspace(
            0,
            1,
            fade_length,
        )

        music[-fade_length:] *= np.linspace(
            1,
            0,
            fade_length,
        )

    # Normalize audio.
    maximum = np.max(np.abs(music))

    if maximum > 0:
        music = music / maximum

    audio_data = np.int16(
        np.clip(music, -1, 1) * 32767
    )

    music_folder = Path("music")
    music_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = music_folder / "generated_music.wav"

    with wave.open(str(output_path), "wb") as audio_file:

        audio_file.setnchannels(1)
        audio_file.setsampwidth(2)
        audio_file.setframerate(sample_rate)

        audio_file.writeframes(
            audio_data.tobytes()
        )

    return str(output_path)