import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_json(text):
    """
    Extract JSON array safely from LLM output
    """
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return []
    return []


def generate_quiz_from_chunk(text):

    prompt = f"""
Generate exactly 3 quiz questions from the following educational text.

{text}

Return ONLY a JSON array in this format:

[
{{
"question":"...",
"type":"MCQ",
"options":["A","B","C","D"],
"answer":"A",
"difficulty":"easy"
}}
]
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        output = response.choices[0].message.content

        print("LLM Output:", output)

        questions = extract_json(output)

        return questions

    except Exception as e:

        print("Quiz generation error:", e)

        return []