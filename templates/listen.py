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

from media_tools.audio_tools import transcribe
from third_party_apis.models import LLMsList, SpeechRecList
from media_tools.text_tools import translate


def transcribe_and_translate_audio(
    file_path:str,
    transcriber:SpeechRecList = "whisper-1",
    llm:LLMsList = "gpt-4o-mini",
):
    '''
    Transcribe an audio file and translate the transcription to English.
    '''

    transcription = transcribe(file_path, model=transcriber)
    text = transcription.text
    print(f'\nTranscription:\n{text}\n')

    if 'english' not in transcription.model_extra['language']:
        translation = translate(text, model=llm)
        print(f'\nTranslation:\n{translation}\n')
    else:
        translation = text

    return {'transcription': text, 'translation': translation}


input_file = "data/audio/WhatsApp Ptt 2024-08-20 at 8.01.48 PM.ogg"
transcribe_and_translate_audio(input_file, llm="gpt-4o-mini")