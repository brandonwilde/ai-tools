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


prompt_template_1 = """
You are an AI assistant tasked with helping me create a great cover letter for a competitive job application. We'll do this together, but you'll take the lead. Please read the instructions carefully, and then we'll get started.

1. **REVIEW** - First, review the following information:

<job_description>{JOB_DESCRIPTION}</job_description>

<previous_cover_letters>
{PREVIOUS_COVER_LETTERS}
</previous_cover_letters>

<resume>
{RESUME}
</resume>
"""

prompt_template_2 = """
2. **SELECT** - Select the cover letter from the previous cover letters that best represents me for the new position. Print this letter verbatim within <selected_letter> tags.

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

Remember to think carefully about each step before providing your response. Please also walk me through your thought process and confirm your plans with me before taking any step, and check your results with me after each step. You can also ask me for clarification or more information to fill in data gaps.

Please only take one step at a time; I want this to be a collaborative collaboration. Let's begin with the first step.
"""


prompt1 = prompt_template_1.format(
    # COMPANY_NAME=args["company_name"],
    # JOB_TITLE=args["job_title"],
    JOB_DESCRIPTION=args["job_description"],
    PREVIOUS_COVER_LETTERS=args["previous_cover_letters"],
    RESUME=args["resume"],
)

prompt2 = prompt_template_2.format(
    COMPANY_NAME=args["company_name"],
    JOB_TITLE=args["job_title"],
)

response = chat_with_llm(
    system_prompt=[{"text": "You are a helpful assistant.", "cache": True}],
    messages=[{"text": prompt1, "cache": True}, {"text": prompt2}],
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

output_file = parent_dir / f"cover_letter_{filenamify(args['company_name'])}_{tag}.xml"
with open(output_file, "w") as f:
    f.write(response)