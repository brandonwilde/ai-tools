from media_tools.audio_tools import convert_to_mp3, transcribe_via_whisper
from media_tools.text_tools import translate_via_openai


def transcribe_and_translate_audio(file_path, model="gpt-3.5-turbo"):
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
            transcription = transcribe_via_whisper(audio_file)
        text = transcription.text
        print(f'\nTranscription:\n{text}\n')
    except Exception as e:
        print(f"An error occurred during transcription: {e}")

    try:
        if 'english' not in transcription.model_extra['language']:
            translation = translate_via_openai(text,model)
            print(f'\nTranslation:\n{translation}\n')
        else:
            translation = text
    except Exception as e:
        print(f"An error occurred during translation: {e}")

    return {'transcription': text, 'translation': translation}


input_file = "/home/brandon/Documents/Sound recordings/WhatsApp Ptt 2024-06-01 at 5.18.53 PM.ogg"
transcribe_and_translate_audio(input_file)