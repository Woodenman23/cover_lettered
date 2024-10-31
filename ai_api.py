from openai import OpenAI

client = OpenAI()

resume_text = "Joseph Foster, Devops engineer (2 years), Linux, python, automation"
job_role = "Devops engineer, Software Ltd, requires: python, bash scripting, knowlege of cloud."

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
)

generated_text = completion.choices[0].message.content


with open("cover_letter.txt", "w") as file:
    file.write("Generated Cover Letter:\n")
    file.write(generated_text)
