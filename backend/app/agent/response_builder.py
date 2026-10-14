"""
===============================================================================
File:
    app/agent/response_builder.py

Description:
    Builds the final response returned to the user.

Responsibilities:
    - Combine LLM response.
    - Include tool execution results.
    - Create a readable assistant response.

Does NOT:
    - Execute tools.
    - Access files.
    - Query the database.
    - Manage project context.

Author:
    Amr Elhabbal
===============================================================================
"""


import json


class ResponseBuilder:
    """
    Converts agent execution results into
    a user-facing response.
    """

    def build(
        self,
        execution_results: dict,
        llm_answer: str,
    ) -> str:
        """
        Build final assistant response.
        """

        response_parts = []


        if llm_answer:
            response_parts.append(
                llm_answer
            )


        if execution_results:

            for tool_name, result in execution_results.items():

                response_parts.append(
                    f"\n{tool_name} result:"
                )


                if isinstance(
                    result,
                    (dict, list)
                ):

                    response_parts.append(
                        json.dumps(
                            result,
                            indent=2
                        )
                    )

                else:

                    response_parts.append(
                        str(result)
                    )


        return "\n".join(
            response_parts
        )