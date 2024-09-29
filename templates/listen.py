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

    if 'english' not in transcription.model_extra['language']:
        translation = translate(text, model=llm)
        print(f'\nTranslation:\n{translation}\n')
    else:
        translation = text

    return {'transcription': text, 'translation': translation}


input_file = "data/audio/WhatsApp Ptt 2024-09-11 at 12.03.07 PM.ogg"
transcribe_and_translate_audio(input_file, llm="gpt-4o-mini")