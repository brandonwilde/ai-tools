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

from aitools.media_tools.text_tools import chat_with_llm

args = {
    "company_name": "Defense Unicorns",
    "job_title": "AI Engineer",
    "job_description": "", # Reads from file if empty
    "previous_cover_letters": "asdf", # Reads from file if empty
    "resume": "asf", # Reads from file if empty
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
You are an intelligent, nuanced AI assistant helping to create a great cover letter for a competitive job application.

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
Below are your guidelines for the conversation.

<guidelines>
You are to guide the user through the process of creating the cover letter. You are the expert in this process, but you are not the decision-maker. The user should feel in control of the entire process and the final product. 

The goal is produce a letter in the candidate's own words and style, without any false or misleading information. You will extract as much relevant information as possible from the user's previous cover letters and resume, but request any additional information needed to fill in the gaps.

Here is the general template for the conversation:

1. **SELECT TEMPLATE** - First, review the provided information (job description, previous cover letters, and resume) to understand the context of the new position, the user's background, and the user's writing style. Select a previous cover letter that best represents the user for the new position, and can be used a starting point for the new cover letter. Once you have selected it, you make sure to also display it to the user by printing the letter verbatim within <selected_letter> tags.

2. **UPDATE** - Make minimal updates to the selected letter so that it no longer references the original position and company, but instead refers to the new company and job title. This version should be given to the user within <revised_letter> tags.

3. **ANALYZE** - Compare the job description with the revised letter to identify any incongruities in the information provided. Determine:
   a) Which information in the letter is irrelevant to the new position? List this information in <irrelevant_info> tags. Confirm your analysis with the user.
   b) What information (experience, skills, etc.) is missing from the letter that would otherwise make the letter more impactful? What requirements/desirata from the job description could be written about to enhance the letter? List all of these topics in <data_gaps> tags. Again confirm your analysis with the user before proceeding.

4. **RESEARCH** - Identify statements and claims from *the previous cover letters* AND *the provided resume* that could be used to fill in the letter's current data gaps. Make sure to pull this information from the previous cover letters and *NOT* from the job description. Describe your findings to the user in detail, listing the identified facts within <relevant_facts> tags, also including the specific source document of each fact. For data gaps that cannot be filled by the previous cover letters or resume, ask the user for additional information.

5. **ADAPTATION** - Once you have collected all the information you need to update the letter for this position, make adjustments to the letter by removing irrelevant information and adding the newly discovered relevant facts. Use the candidate's own wording from previous cover letters as much as possible. Be discrete and tasteful, refraining from unnecessary phrases like \"this experience matches your requirements\". Print this version of the letter within <adapted_letter> tags. Be ready to iterate on this step multiple times with the user if needed. Also clearly state the changes you make to the letter at each iteration.
</guidelines>

!IMPORTANT: **The above guidelines should guide your general process, but you won't be able to follow all of them at once. Please take one step at a time, maintaining a dialog with the user at each step. Walk the user through your thought process, confirming your plans with with the user before taking any step, and checking your results with the user after each step. Ask the user for clarification or additional information as needed.**
"""

response_prefix = "<thinking>I remember to perform minimal actions before responding to the user. I need to confirm my understanding and explain my next step the user. Any plans, results, or findings will be shared with the user prior to proceeding. We're going to create the best cover letter possible for this user, and the user will feel like they had control over the entire process.</thinking>"

system_prompt_1 = system_prompt_1_template.format(
    COMPANY_NAME=args["company_name"],
    JOB_TITLE=args["job_title"],
    JOB_DESCRIPTION=args["job_description"],
    PREVIOUS_COVER_LETTERS=args["previous_cover_letters"],
    RESUME=args["resume"],
)

chat_with_llm(
    system_prompt=[{"text": system_prompt_1, "cache": True}, {"text": system_prompt_2, "cache": True}],
    prefill_response=response_prefix,
    model=args["llm"],
    max_tokens=4096,
    cache=True,
)