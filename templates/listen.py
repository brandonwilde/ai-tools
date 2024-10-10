#-------------Enable execution from non-root----------------#
import sys
from pathlib import Path
sys.path.append(str(next(p for p in Path(__file__).resolve().parents if p.name == 'ai-tools')))
#-----------------------------------------------------------#

from aitools.media_tools.audio_tools import transcribe
from aitools.media_tools.text_tools import translate
from aitools.third_party_apis.models import LLMsList, SpeechRecList


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

    if 'english' not in transcription.language:
        translation = translate(text, model=llm)
        print(f'\nTranslation:\n{translation}\n')
    else:
        translation = text

    return {'transcription': text, 'translation': translation}


input_file = "data/audio/WhatsApp Ptt 2024-10-02 at 4.35.05 PM.ogg"
transcribe_and_translate_audio(input_file, llm="gpt-4o-mini")