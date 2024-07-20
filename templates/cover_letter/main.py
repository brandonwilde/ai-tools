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

from media_tools.text_tools import prompt_openai


company_name = ""

job_title = ""

job_description = "" # Reads from file if empty

previous_cover_letters = "" # Reads from file if empty

parent_dir = Path(__file__).parent

for path in [parent_dir, root_path]:
    if (description_path := path / "job_description.txt").exists():
        with open(description_path, "r") as f:
            job_description = f.read()
        break
if not job_description:
    raise Exception("Please provide the job description in a file named 'job_description.txt'.")

for path in [parent_dir, root_path]:
    if (letters_path := path / "previous_cover_letters.txt").exists():
        with open(letters_path, "r") as f:
            previous_cover_letters = f.read()
        break
if not previous_cover_letters:
    raise Exception("Please provide previous cover letters in a file named 'previous_cover_letters.txt'.")



prompt_template = """
You are an AI assistant tasked with helping create a great cover letter for a competitive job application. Follow these steps carefully:

1. First, review the following information:

<job_description>{JOB_DESCRIPTION}</job_description>

<previous_cover_letters>
{PREVIOUS_COVER_LETTERS}
</previous_cover_letters>

2. Select the cover letter from the previous cover letters that best represents the applicant for the new position. Print this letter verbatim within <selected_letter> tags.

3. Make minimal updates to the selected letter so that it no longer references the original position and company, but instead refers to the new company and position. Use the following information:

New Company: {COMPANY_NAME}
New Position: {JOB_TITLE}

Print the revised letter within <revised_letter> tags.

4. Answer the following questions:
   a) Which information in the letter is irrelevant to the new position?
   b) What information is missing from the letter that would make it more suitable for the new position?

Provide your answers within <analysis> tags.

5. Identify statements and claims from the previous cover letters that could be used to fill in the letter's current data gaps. Make sure to pull this information from the previous cover letters and NOT from the job description. List these facts within <relevant_facts> tags.

6. Make adjustments to the letter by removing irrelevant information and adding relevant information found in the previous letters. Be discrete and tasteful, refraining from unnecessary phrases like \"this experience matches your requirements\". Print the final version of the letter within <final_letter> tags.

7. List the changes you made to the letter within <changes_made> tags.

Remember to think carefully about each step before providing your response. If you need to, use <scratchpad> tags to work through your thought process before giving your final answer for each step.
"""


prompt = prompt_template.format(
    JOB_DESCRIPTION=job_description,
    PREVIOUS_COVER_LETTERS=previous_cover_letters,
    COMPANY_NAME=company_name,
    JOB_TITLE=job_title,
)

response = prompt_openai(messages=[{"text": prompt}])

with open(parent_dir / "cover_letter.xml", "w") as f:
    f.write(response)