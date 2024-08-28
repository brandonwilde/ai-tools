import os
import subprocess
from tabulate import tabulate

from third_party_apis.models import SpeechRecList, ALL_SPEECH_REC

DEFAULT_SPEECH_REC = "whisper-1"


def convert_to_mp3(filepath):
    """
    Convert an audio file to mp3 format using ffmpeg.
    """
    output_file = os.path.splitext(filepath)[0] + ".mp3"
    if os.path.exists(output_file):
        overwrite = input(f"Overwrite {output_file}? (y/n): ")
        if overwrite.lower() != "y":
            return output_file
    subprocess.run(
        ["ffmpeg", "-y", "-i", filepath, output_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )
    return output_file


def get_duration(filepath):
    """
    Get the duration of an audio file in seconds using ffprobe.
    """
    duration = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    ).stdout
    return round(float(duration))


def log_transcription_cost(
    duration: int,
    model:SpeechRecList = DEFAULT_SPEECH_REC,
):
    '''
    Log the cost of a transcription response.

    Args:
    - duration (int): The duration of the audio file in seconds.
    - model (str): The speech recognition model used.
    '''

    minutes = duration / 60
    plus_seconds = duration % 60
    cost = minutes * ALL_SPEECH_REC[model]['cost_per_min']

    data = [
        ["Duration", f"{int(minutes)}m {int(plus_seconds)}s"],
        ["Cost", f"${cost:.5f}"],
    ]

    print(tabulate(data, colalign=("left", "right")))

    return


def transcribe(
    file_path: str,
    model:SpeechRecList = DEFAULT_SPEECH_REC,
):
    """
    Transcribe an audio file using the Whisper model.
    """

    from third_party_apis.openai_tools import transcribe_via_openai as _transcribe

    if file_path.endswith(".mp3"):
        mp3_file = file_path
    else:
        mp3_file = convert_to_mp3(file_path)

    duration_s = get_duration(mp3_file)

    print(f'Calling speech recognition model "{model}"...\n')

    with open(mp3_file, "rb") as audio_file:
        transcription_response = _transcribe(audio_file)

    log_transcription_cost(duration_s, model)

    return transcription_response