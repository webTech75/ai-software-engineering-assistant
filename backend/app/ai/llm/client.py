"""
LLM communication layer handling model requests and responses.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

from openai import OpenAI

from app.core.config import settings
from app.agent.prompts.system_prompt import SYSTEM_PROMPT


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
        # max_tokens: int | None = None,
    ) -> str:
        """
        Generate response from LLM.

        The system prompt is automatically applied
        to every request.

        Token limits are selected by Agent.
        """

        try:

            # if max_tokens is None:

            #     max_tokens = settings.llm_max_tokens

            print(f"LLM request | " f"model={settings.LLM_MODEL} | ")

            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                # max_tokens=max_tokens,
                timeout=30,
                temperature=0.2,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            print("================ LLM RESPONSE ================")
            print(response.model_dump())
            print("===============================================")

            if not response:

                return "The AI model returned an empty response."

            if not response.choices:

                return "The AI model returned no choices."

            message = response.choices[0].message

            content = message.content

            if not content:

                reasoning = getattr(message, "reasoning", None)

                if reasoning:

                    return reasoning

                return "The model completed reasoning " "but did not return an answer."

            if not content:

                return "The AI model returned empty content."

            return content

        except Exception as error:

            print("================ LLM ERROR ================")
            print(type(error).__name__)
            print(error)
            print("============================================")

            return "I could not generate a response right now. " "Please try again."
