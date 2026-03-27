import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def format_resources_for_prompt(resources):
    lines = []

    for i, r in enumerate(resources, start=1):
        lines.append(
            f"{i}. Name: {r['name']}\n"
            f"Type: {r['type']}\n"
            f"Description: {r['description']}\n"
            f"URL: {r['url']}\n"
            f"Why matched: {r['why_matched']}\n"
        )

    return "\n".join(lines)

def build_prompt(year, major, question, resources):
    resources_text = format_resources_for_prompt(resources)

    prompt = f"""
You are a helpful WashU student resource assistant.

Your job is to help a student based only on the database results provided below.
Do not make up any resources that are not in the retrieved results.

Student info:
- Year: {year}
- Major: {major}

Student question:
{question}

Retrieved database resources:
{resources_text}

Please do the following:
1. Recommend the most relevant resources.
2. Explain briefly why each resource is relevant to this student.
3. Suggest practical next steps.
4. Include the URL for each recommended resource.

Return your answer in clear English.
"""
    return prompt


def generate_ai_answer(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for WashU students."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

def generate_chat_response(year, major, question, resources):
    prompt = build_prompt(year, major, question, resources)
    answer = generate_ai_answer(prompt)
    return answer