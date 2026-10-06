"""
===============================================================================
File: service.py
Path: app/agent/service.py

Description:
    Implements the AI Agent responsible for orchestrating conversations
    between the user, the Large Language Model (LLM), and the project's
    tools.

Responsibilities:
    - Build the initial conversation.
    - Send requests to the LLM.
    - Handle LLM tool calls.
    - Execute project tools safely.
    - Feed tool results back to the LLM.
    - Return the final assistant response.

Workflow:

    User
      │
      ▼
 Build Messages
      │
      ▼
 Send to LLM
      │
      ▼
 Tool Calls?
 ├───────────────┐
 │ No            │ Yes
 ▼               ▼
Return      Execute Tool
                 │
                 ▼
         Append Tool Result
                 │
                 ▼
          Continue Conversation

Dependencies:
    - OpenAI Chat Completions API
    - ToolRegistry
    - SYSTEM_PROMPT
    - Application Settings

Author:
    Amr Elhabbal
===============================================================================
"""

import json

from app.ai.llm.client import client
from app.agent.tool_registry import ToolRegistry
from app.agent.prompts.system_prompt import SYSTEM_PROMPT
from app.core.config import settings


class AgentService:
    def __init__(self):
        self.tool_registry = ToolRegistry() 

    def ask(self, project, message: str) -> str:
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": message,
            },
        ]

        while True:
            response = client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                tools=self.tool_registry.schemas,
            )

            assistant_message = response.choices[0].message

            # Save the assistant message so the model can continue the conversation.
            messages.append(assistant_message)

            # If the model answered normally, we're done.
            if assistant_message.content:
                return assistant_message.content

            # If no tools were requested, stop.
            if not assistant_message.tool_calls:
                return "The assistant did not return a response."

            # Execute every requested tool.
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments or "{}")

                try:
                    tool = self.tool_registry.get(tool_name)

                    if tool is None:
                        result = f"Unknown tool: {tool_name}"
                    else:
                        result = tool.execute(
                            project,
                            **arguments,
                        )

                except FileNotFoundError as e:
                    result = f"File not found: {e}"

                except PermissionError:
                    result = "Permission denied."

                except Exception as e:
                    result = f"Tool error: {e}"

                tool_output = json.dumps(result)

                MAX_TOOL_OUTPUT = 50_000

                if len(tool_output) > MAX_TOOL_OUTPUT:
                    tool_output = (
                        tool_output[:MAX_TOOL_OUTPUT]
                        + "\n\n...output truncated..."
                    )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )