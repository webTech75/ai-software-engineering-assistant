"""
===============================================================================
File:
    app/ai/llm/client.py

Description:
    LLM communication layer.

Responsibilities:
    - Send prompts to the language model.
    - Return generated responses.

Does NOT:
    - Access database.
    - Access files.
    - Execute tools.

===============================================================================
"""

from openai import OpenAI

from app.core.config import settings


class LLMClient:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
        )


    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            max_tokens=1000,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI software engineering assistant. "
                        "Help users understand, analyze, and improve software projects."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

        )

        return response.choices[0].message.content