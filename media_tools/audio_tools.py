import os
import subprocess


def convert_to_mp3(filepath):
    """
    Convert an audio file to mp3 format using ffmpeg.
    """
    output_file = os.path.splitext(filepath)[0] + ".mp3"
    subprocess.run(["ffmpeg", "-i", filepath, output_file], check=True)
    return output_file


def transcribe_via_whisper(audio_file):
    """
    Transcribe an audio file using the Whisper model.
    """

    from third_party_apis.openai_tools import CLIENT as OPENAI_CLIENT

    transcription_response = OPENAI_CLIENT.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format='verbose_json',
    )

    return transcription_response