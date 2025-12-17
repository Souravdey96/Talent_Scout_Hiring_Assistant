"""
llm.py
------
Handles interaction with the OpenAI language model
using the OpenAI Python SDK v2.x.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import TECHNICAL_QUESTION_PROMPT

# Load environment variables
load_dotenv()

# Create OpenAI client (v2 SDK automatically reads OPENAI_API_KEY)
client = OpenAI()


def generate_technical_questions(desired_role, experience, tech_stack):
    """
    Generates 3–5 technical interview questions based on the candidate's tech stack.
    """

    # Defensive checks (professional practice)
    if not tech_stack:
        raise ValueError("Tech stack is empty")

    prompt = TECHNICAL_QUESTION_PROMPT.format(
        desired_role=desired_role,
        experience=experience,
        tech_stack=tech_stack
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # This model IS available in v2
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional technical interviewer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        # Re-raise so app.py fallback can catch it
        raise RuntimeError(f"OpenAI API error: {str(e)}")
