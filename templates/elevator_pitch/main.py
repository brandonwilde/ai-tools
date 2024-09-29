from pathlib import Path

from aitools.media_tools.text_tools import prompt_llm
from aitools.media_tools.utils import filenamify

args = {
    "company_name": "",
    "job_title": "",
    "job_description": "", # Reads from file if empty
    "previous_cover_letters": "", # Reads from file if empty
    "resume": "", # Reads from file if empty
}

parent_dir = Path(__file__).parent

for arg in ["job_description", "previous_cover_letters", "resume"]:
    if (arg_path := parent_dir / f"{arg}.txt").exists():
        with open(arg_path, "r") as f:
            args[arg] = f.read()
        break
    if not args[arg]:
        raise Exception(f"Please provide the {arg.replace('_',' ')} in a file named '{arg}.txt'.")


prompt_template = """
You are an AI assistant tasked with helping create a great elevator pitch to help a candidate land their dream job. Follow these steps carefully:

1. **READ** - First, carefully study the following information:

<company_name>
{COMPANY_NAME}
</company_name>

<job_title>
{JOB_TITLE}
</job_title>

<job_description>
{JOB_DESCRIPTION}
</job_description>

<previous_cover_letters>
{PREVIOUS_COVER_LETTERS}
</previous_cover_letters>

<resume>
{RESUME}
</resume>

2. **SEARCH** - Identify the key skills and experiences from the resume and previous cover letters that are relevant to the new position as described in the job description. List these within <relevant_traits> tags.

3. **IDENTIFY_GAPS** - Compare the relevant traits you identified with the job description. Highlight any traits important to the job description that have not been included in the candidate's relevant traits.
List these within <missing_traits> tags.

4. **RE-SEARCH** - Review the resume and previous cover letters again to identify any skills or experiences that could be made relevant to the job description to account for the missing traits. List these within <additional_traits> tags.

5. **VERIFY** - Confirm that the relevant traits (and additional traits) you identified are indeed aligned with the job description, and that they are backed by a previous cover letter or the candidate's resume. Remove any irrelevant traits from the list, and provide the final list within <verified_traits> tags. For each trait, include the specific cover letter or resume section where the trait is mentioned. If a source is not found, state that the source is missing.

6. **DRAFT** - Use the verified traits to draft a compelling elevator pitch of 100 words or less that highlights the candidate's strengths and experiences, and how they align with the job description. The pitch should sound natural, such that it could be spoken by the candidate to the hiring manager. It's not necessary to include the job title or name of the company. Write the pitch within <elevator_pitch> tags.

7. **CRITIQUE** - Provide a brief critique of the elevator pitch, highlighting its strengths and any areas that could be improved. Be constructive and specific in your feedback, and offer suggestions for enhancement within <critique> tags.

8. **FINALIZE** - Make any necessary adjustments to the elevator pitch based on your critique, and finalize the pitch within <final_elevator_pitch> tags.

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
    model="gpt-4o-mini",
)

output_file = parent_dir / f"elevator_pitch_{filenamify(args['company_name'])}.xml"
with open(output_file, "w") as f:
    f.write(response)