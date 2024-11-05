from openai import OpenAI

from website import OPEN_AI_API_TOKEN

client = OpenAI(api_key=OPEN_AI_API_TOKEN)


def generate_letter(resume_text: str, job_role: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant skilled at writing cover letters for job applications.",
        },
        {"role": "user", "content": f"Here is a resume:\n{resume_text}"},
        {"role": "user", "content": f"Here is a job description:\n{job_role}"},
        {
            "role": "user",
            "content": f"Write a cover letter for the {job_role} for the person with {resume_text}.",
        },
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.5,
        max_tokens=1000,
    )

    cover_letter_text = completion.choices[0].message.content

    with open("cover_letter.txt", "w") as file:
        file.write("Generated Cover Letter:\n")
        file.write(cover_letter_text)

    return cover_letter_text
