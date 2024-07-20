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

from media_tools.image_tools import ask_gpt4v


system_prompt = "You are expert in deciphering difficult-to-read handwriting. You are now correcting a poor transcription of an excerpt from the journals of a Mormon missionary in eastern Canada. Note that when the author writes an 'I', it sometimes looks like an 'S' or a '2'."

image_path = "data/IMG_20240210_115126.jpg"

transcription = """Good 410
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

messages = [
    {'text': "Here is an image of the excerpt."},
    {'image': image_path},
    {'text': "And here is an attempted character-for-character transcription. Please correct it based on context clues and your analysis of the handwriting. Since there is writing in the margins, some of the transcript text may be out of place too."},
    {'text': transcription}
]

result = ask_gpt4v(messages, system_prompt)

print(result)