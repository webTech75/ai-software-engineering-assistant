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
    - Decide task type.
    - Decide token limits.
    - Access database.
    - Access files.
    - Execute tools.

===============================================================================
"""

from openai import OpenAI

from app.core.config import settings


class LLMClient:

    def __init__(self):
        """
        Initialize LLM client.
        """

        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
        )



    def generate(
        self,
        prompt: str,
        max_tokens: int | None = None,
    ) -> str:
        """
        Generate response from LLM.

        max_tokens is selected by Agent based on task type.

        Examples:

            general question
                -> settings.llm_max_tokens

            explanation
                -> settings.llm_explain_max_tokens

            review
                -> settings.llm_review_max_tokens
        """


        try:

            # -----------------------------------------------------
            # Safety fallback
            #
            # If caller does not provide token limit,
            # use default environment setting.
            # -----------------------------------------------------

            if max_tokens is None:

                max_tokens = settings.llm_max_tokens

            print(
                f"LLM request | model={settings.LLM_MODEL} | max_tokens={max_tokens}"
            )

            response = self.client.chat.completions.create(

                model=settings.LLM_MODEL,

                max_tokens=max_tokens,

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "You are an AI software engineering assistant. "
                            "Help users understand, analyze, "
                            "and improve software projects."
                        ),
                    },

                    {
                        "role": "user",
                        "content": prompt,
                    },

                ],

            )


        except Exception as e:

            return (
                "I could not generate an AI response right now. "
                f"LLM error: {str(e)}"
            )



        return response.choices[0].message.content