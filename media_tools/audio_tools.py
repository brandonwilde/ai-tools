import os
import subprocess
from typing import BinaryIO

from third_party_apis.models import TTSList


def convert_to_mp3(filepath):
    """
    Convert an audio file to mp3 format using ffmpeg.
    """
    output_file = os.path.splitext(filepath)[0] + ".mp3"
    if os.path.exists(output_file):
        overwrite = input(f"Overwrite {output_file}? (y/n): ")
        if overwrite.lower() != "y":
            return output_file
    subprocess.run(["ffmpeg", "-y", "-i", filepath, output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return output_file


def transcribe(
    audio_file: BinaryIO,
    model:TTSList = "whisper-1",
):
    """
    Transcribe an audio file using the Whisper model.
    """

    from third_party_apis.openai_tools import transcribe_via_whisper as _transcribe

    transcription_response = _transcribe(audio_file)

    return transcription_response