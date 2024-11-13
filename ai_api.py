from openai import OpenAI

from website import OPEN_AI_API_TOKEN

client = OpenAI(api_key=OPEN_AI_API_TOKEN)


def generate_letter_text(
    resume_text: str, job_title: str, company: str, job_role: str
) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant, skilled at writing cover letters for job applications.",
        },
        {"role": "user", "content": f"Here is a resume:\n{resume_text}"},
        {"role": "user", "content": f"Here is a job description:\n{job_role}"},
        {"role": "user", "content": f"The job title is:\n{job_title}"},
        {"role": "user", "content": f"The company is called:\n{company}"},
        {
            "role": "user",
            "content": "You should write the cover letter in the following format only:\nDear [company] hiring team,\n\n[Letter content without any header or contact information]\n\n[well-wishing sign-off],\n[Applicant name]",
        },
        {
            "role": "user",
            "content": "Do not include any contact information, headers, addresses, or irrelevant details. Focus only on writing a concise, targeted cover letter based on the provided resume and job description.",
        },
        {
            "role": "user",
            "content": f"Write a cover letter for the {job_role} for the person with {resume_text}.",
        },
    ]

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
    )

    cover_letter_text = completion.choices[0].message.content

    return cover_letter_text
