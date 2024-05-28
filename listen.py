import os
import subprocess

from openai import OpenAI


OPENAI_API_KEY=os.environ.get('OPENAI_API_KEY')
OPENAI_ORGANIZATION=os.environ.get('OPENAI_ORGANIZATION')

CLIENT = OpenAI(
    api_key=OPENAI_API_KEY,
    organization=OPENAI_ORGANIZATION,
)

input_file = "/home/brandon/Documents/Sound recordings/WhatsApp Ptt 2024-05-28 at 8.07.58 AM.ogg"

if not input_file.endswith(".mp3"):
    output_file = os.path.splitext(input_file)[0] + ".mp3"
    subprocess.run(["ffmpeg", "-i", input_file, output_file], check=True)
else:
    output_file = input_file

audio_file= open(output_file, "rb")
transcription = CLIENT.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format='verbose_json',
)
text = transcription.text
print(transcription.text)

if 'english' not in transcription.model_extra['language']:
    translation_response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": [{"type": "text", "text": "Translate the following text into English."}]},
            {"role": "user", "content": [{"type": "text", "text": text}]}
        ]
    )
    print('\nTranslation:')
    print(translation_response.choices[0].message.content)
    print()

print()