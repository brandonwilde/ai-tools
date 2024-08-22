from pathlib import Path
import sys

#----Enable imports as if run from project root----#
def find_repo_root(repo_name):
    current_path = Path(__file__).resolve()
    while current_path.parent != current_path: # Stop at filesystem root
        if current_path.name == repo_name:
            return current_path
        current_path = current_path.parent
    raise FileNotFoundError(f'Could not find the root of the "{repo_name}" repository in the file path.')

root_path = find_repo_root(repo_name="ai-tools")
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))
#--------------------------------------------------#

from media_tools.audio_tools import convert_to_mp3, transcribe
from third_party_apis.models import LLMsList
from media_tools.text_tools import translate


def transcribe_and_translate_audio(
    file_path:str,
    llm:LLMsList = "gpt-4o-mini",
):
    '''
    Transcribe an audio file and translate the transcription to English.
    '''
    try:
        if not file_path.endswith(".mp3"):
            mp3_file = convert_to_mp3(file_path)
        else:
            mp3_file = file_path
    except Exception as e:
        print(f"An error occurred during conversion to mp3: {e}")

    try:
        with open(mp3_file, "rb") as audio_file:
            transcription = transcribe(audio_file)
        text = transcription.text
        print(f'\nTranscription:\n{text}\n')
    except Exception as e:
        print(f"An error occurred during transcription: {e}")

    try:
        if 'english' not in transcription.model_extra['language']:
            translation = translate(text, model=llm)
            print(f'\nTranslation:\n{translation}\n')
        else:
            translation = text
    except Exception as e:
        print(f"An error occurred during translation: {e}")

    return {'transcription': text, 'translation': translation}


input_file = "data/audio/WhatsApp Ptt 2024-08-20 at 8.01.48 PM.ogg"
transcribe_and_translate_audio(input_file, llm="gpt-4o-mini")