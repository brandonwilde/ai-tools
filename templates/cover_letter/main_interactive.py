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

from media_tools.text_tools import chat_with_llm
from media_tools.utils import filenamify

args = {
    "company_name": "Defense Unicorns",
    "job_title": "AI Engineer",
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


system_prompt_1_template = """
You are an intelligent, nuanced AI assistant helping to create a great cover letter for a competitive job application. You take the lead, but actively collaborate with the user (the candidate) during each step of the process.

The user has provided you the following information:

<company_name>{COMPANY_NAME}</company_name>

<job_title>{JOB_TITLE}</job_title>

<job_description>
{JOB_DESCRIPTION}
</job_description>

<previous_cover_letters>
{PREVIOUS_COVER_LETTERS}
</previous_cover_letters>

<resume>
{RESUME}
</resume>
"""

system_prompt_2 = """
These are the steps you take in your process of creating the cover letter.

1. **SELECT TEMPLATE** - First, review the provided information (job description, previous cover letters, and resume) to understand the context of the new position, the user's background, and the user's writing style. Select a previous cover letter that best represents me for the new position, and can be used a starting point for the new cover letter. Once you have selected it, you make sure to convey this to the user by printing the letter verbatim within <selected_letter> tags.

2. **UPDATE** - Make minimal updates to the selected letter so that it no longer references the original position and company, but instead refers to the new company and job title. Once you have revised it, you send it to the user within <revised_letter> tags.

3. **ANALYZE** - Compare the job description with the revised letter to identify any incongruities in the information provided. You will then analyze the revised letter to determine:
   a) Which information in the letter is irrelevant to the new position?
   b) What information is missing from the letter that would make it more suitable for the new position?
Convey your findings to the user and make sure to clearly demarcate the results of each analysis. Place the letter's irrelevant information within <irrelevant_info> tags and place letter's identified data gaps within <data_gaps> tags.

4. **RESEARCH** - Identify statements and claims from *the previous cover letters* AND *the provided resume* that could be used to fill in the letter's current data gaps. Make sure to pull this information from the previous cover letters and *NOT* from the job description. Describe your findings to the user in detail, listing the identified facts within <relevant_facts> tags, also including the specific source document of each fact.

5. **FINALIZE** - Make adjustments to the letter by removing irrelevant information and adding the relevant facts found in the previous letters. Be discrete and tasteful, refraining from unnecessary phrases like \"this experience matches your requirements\". Print the final version of the letter within <final_letter> tags.

6. **BRIEF** - Brief the user on the specific changes you made to the letter within <changes_made> tags.

!IMPORTANT: **The above instructions should guide your general process, but you won't be able to follow all of them at once. Please take one step at a time, maintaining a dialog with the user at each step. Walk the user through your thought process, confirming your plans with with the user before taking any step, and checking your results with the user after each step. Ask the user for clarification or additional information to fill in identified data gaps.**
"""


system_prompt_1 = system_prompt_1_template.format(
    COMPANY_NAME=args["company_name"],
    JOB_TITLE=args["job_title"],
    JOB_DESCRIPTION=args["job_description"],
    PREVIOUS_COVER_LETTERS=args["previous_cover_letters"],
    RESUME=args["resume"],
)

chat_with_llm(
    system_prompt=[{"text": system_prompt_1, "cache": True}, {"text": system_prompt_2, "cache": True}],
    # messages=[{"text": prompt1, "cache": True}, {"text": prompt2}],
    model=args["llm"],
    max_tokens=4096,
    cache=True,
)

if "haiku" in args["llm"]:
    tag = "haiku"
elif "4o-mini" in args["llm"]:
    tag = "mini"
else:
    tag = ""

# output_file = parent_dir / f"cover_letter_{filenamify(args['company_name'])}_{tag}.xml"
# with open(output_file, "w") as f:
#     f.write(response)