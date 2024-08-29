import os
import subprocess
from tabulate import tabulate

from aitools.third_party_apis.models import SpeechRecList, ALL_SPEECH_REC

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


def log_transcription_cost(
    duration: float,
    model:SpeechRecList = DEFAULT_SPEECH_REC,
):
    '''
    Log the cost of a transcription response.

    Args:
    - duration (int): The duration of the audio file in seconds.
    - model (str): The speech recognition model used.
    '''

    duration_sec = round(duration)
    duration_min = duration_sec / 60
    
    cost = duration_min * ALL_SPEECH_REC[model]['cost_per_min']

    minutes = int(duration_sec // 60)
    seconds = duration_sec % 60

    data = [
        ["Duration", f"{minutes}m {seconds}s"],
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

    from aitools.third_party_apis.openai_tools import transcribe_via_openai as _transcribe

    if file_path.endswith(".mp3"):
        mp3_file = file_path
    else:
        mp3_file = convert_to_mp3(file_path)

    print(f'Calling speech recognition model "{model}"...\n')

    with open(mp3_file, "rb") as audio_file:
        transcription_response = _transcribe(audio_file)

    duration = transcription_response.model_extra['duration']
    log_transcription_cost(duration, model)

    return transcription_response