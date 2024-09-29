from pathlib import Path
import sys

#----Enable script execution as if run from project root----#
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
#-----------------------------------------------------------#

from aitools.media_tools.text_tools import prompt_llm
from aitools.media_tools.utils import filenamify

args = {
    "company_name": "",
    "job_title": "",
    "job_description": "", # Reads from file if empty
    "previous_cover_letters": "", # Reads from file if empty
    "resume": "", # Reads from file if empty
    "llm": "claude-3-haiku-20240307",
    # "llm": "gpt-4o-mini",
}


parent_dir = Path(__file__).parent

for arg in ["job_description", "previous_cover_letters", "resume"]:
    for path in [parent_dir, root_path]:
        if (arg_path := path / f"{arg}.txt").exists():
            with open(arg_path, "r") as f:
                args[arg] = f.read()
            break
        if not args[arg]:
            raise Exception(f"Please provide the {arg.replace('_',' ')} in a file named '{arg}.txt'.")


prompt_template = """
You are an AI assistant tasked with helping create a great cover letter for a competitive job application. Follow these steps carefully:

1. **REVIEW** - First, review the following information:

<job_description>{JOB_DESCRIPTION}</job_description>

<previous_cover_letters>
{PREVIOUS_COVER_LETTERS}
</previous_cover_letters>

<resume>
{RESUME}
</resume>

2. **SELECT** - Select the cover letter from the previous cover letters that best represents the applicant for the new position. Print this letter verbatim within <selected_letter> tags.

3. **UPDATE** - Make minimal updates to the selected letter so that it no longer references the original position and company, but instead refers to the new company and position. Use the following information:

New Company: {COMPANY_NAME}
New Position: {JOB_TITLE}

Print the revised letter within <revised_letter> tags.

4. **ANALYZE** - Answer the following questions:
   a) Which information in the letter is irrelevant to the new position?
   b) What information is missing from the letter that would make it more suitable for the new position?

Provide your answers within <analysis> tags.

5. **RESEARCH** - Identify statements and claims from *the previous cover letters* AND *the provided resume* that could be used to fill in the letter's current data gaps. Make sure to pull this information from the previous cover letters and *NOT* from the job description. List these facts within <relevant_facts> tags, also including the specific source document of each fact.

6. **FINALIZE** - Make adjustments to the letter by removing irrelevant information and adding relevant information found in the previous letters. Be discrete and tasteful, refraining from unnecessary phrases like \"this experience matches your requirements\". Print the final version of the letter within <final_letter> tags.

7. **BRIEF** - List the specific changes you made to the letter within <changes_made> tags.

Remember to think carefully about each step before providing your response. Use <scratchpad> tags prior to each step to remind yourself of what is required for that step and work through your thought process before giving your final answer for the step.
"""


prompt = prompt_template.format(
    COMPANY_NAME=args["company_name"],
    JOB_TITLE=args["job_title"],
    JOB_DESCRIPTION=args["job_description"],
    PREVIOUS_COVER_LETTERS=args["previous_cover_letters"],
    RESUME=args["resume"],
)

response = prompt_llm(
    messages=[{"text": prompt}],
    model=args["llm"],
    max_tokens=4096
)

if "haiku" in args["llm"]:
    tag = "haiku"
elif "4o-mini" in args["llm"]:
    tag = "mini"
else:
    tag = ""

output_file = parent_dir / f"cover_letter_{filenamify(args['company_name'])}_{tag}.xml"
with open(output_file, "w") as f:
    f.write(response)