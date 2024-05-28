
from openai_llms import ask_gpt4v


image_path = "data/IMG_20240210_115126.jpg"

messages = [
  {
    "role": "system",
    "content": [
      {
        "type": "text",
        "text": "You are expert in deciphering difficult-to-read handwriting. You are now correcting a poor transcription of an excerpt from the journals of a Mormon missionary in eastern Canada. Note that the author writes an 'I', it sometimes looks like an 'S' or a '2'."
      }
    ]
  },
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "Here is an image of the excerpt."
      },
      {
        "type": "image_url",
        "image_url": {
          "url": "Will be replaced with the base64 encoded image."
        }
      }
    ]
  },
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "And here is an attempted character-for-character transcription. Please correct it based on context clues and your analysis of the handwriting. Since there is writing in the margins, some of the transcript text may be out of place too."
      },
      {
        "type": "text",
        "text": """Good 410
Feb 10/90 - Sat. We brought mom out today Got along pretty good - She's pretty weak to do that on her own though. Washed a late on Surl. Path har mening Misses bevill of afternoon
Good
Feb 11/90 -Sun - attended meetings including Early meeting. We were going to tale special Intervaladas en to ferendo for cla v Betty tout but storm candy Claude Petersendied Friday and they are going to
tel tout
Sman Sim
(Ehrent Betty) Sunt fill to pickpick up La vanne
Pold. Feb 12/90 - Mm - D'ident do much owtal today - word To Town & helped man the evening - cas stayes for a little program after suppen - Somequals sans forthe patents Wedloe picked up Como that Heggen filler out for us on quella Excise tax rebate. fabio shared toute - Preston has the chickenpox. - Cold Feb 13/90 - Isas - Clarade Peteron funeral
Sung today . Bele Zabell 8 2 were uchen. Ruch helped Avide family dinner - 2 dia à laite
futer 8
SUPER CON
Feb14/90 - Wed - Hauled hay & Chipped lead - Roth watched how fra alle-og had prima meeting
Sunny Feb 15/90- Ifun - John wany deed Codan -7. Canal suggested gothing to tech- franke
Bellers lo get a coupled birthday cards der Jimmithe con radia paper - When she can
out hemos avcomuni- de nearly dead. She"""
      }
    ]
  }
]

result = ask_gpt4v(image_path, messages)

print(result)