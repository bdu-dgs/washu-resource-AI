import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def format_resources_for_prompt(resources):
    lines = []

    for i, r in enumerate(resources, start=1):
        block = (
            f"Resource {i}:\n"
            f"Name: {r.get('name','')}\n"
            f"Type: {r.get('type','')}\n"
            f"Description: {r.get('description','')}\n"
            f"URL: {r.get('url','')}\n"
            f"Why matched: {r.get('why_matched','')}"
        )
        lines.append(block)

    return "\n\n".join(lines)

def build_prompt(year, major, question, resources, history = None):
    resources_text = format_resources_for_prompt(resources)

    
    if history:
        prompt = f"""
You are a helpful WashU student resource assistant.

This is a follow-up question from the student.

Previous answer:
{history}

Student info:
- Year: {year}
- Major: {major}

Follow-up question:
{question}

Retrieved database resources:
{resources_text}

Please do the following:
1. Answer the follow-up question.
2. Do NOT repeat the full previous answer.
3. Provide new details, clarification, or next steps.
4. Only use resources listed above.

Return your answer in clear English.
"""
    else:
        prompt = f"""
    You are a helpful WashU student resource assistant.

    our job is to help a student based only on the database results provided below.
    Do not make up any resources that are not in the retrieved results.
    Do not make up any information that is not in the student's question.
    Do not make up any information that is not in the student's year or major.
    Do not make up any information that is not in the student's history.

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

def generate_chat_response(year, major, question, resources, history = None):
    prompt = build_prompt(year, major, question, resources, history)
    answer = generate_ai_answer(prompt)
    return answer