"""
===============================================================================
File: response_builder.py
Path: app/agent/response_builder.py

Description:
    Builds the final response returned to the user.

Responsibilities:
    - Combine project context.
    - Combine tool execution results.
    - Create a readable assistant response.

Does NOT:
    - Execute tools.
    - Access files.
    - Query the database.

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



    def __init__(self):
        """
        Initialize response builder.
        """

        pass




    def build(
        self,
        context: dict,
        execution_results: dict,
    ) -> str:
        """
        Build final assistant response.

        Parameters:

            context:
                Information about the project.

            execution_results:
                Output returned by tools.

        """



        response_parts = []



        # ---------------------------------------------------------
        # Add project information.
        #
        # Example:
        #
        # Project:
        # Test Project
        #
        # ---------------------------------------------------------

        project = context.get(
            "project",
            {}
        )


        if project:

            response_parts.append(
                f"Project: {project.get('name')}"
            )



        # ---------------------------------------------------------
        # Add tool results.
        #
        # Example:
        #
        # list_files:
        #
        # [
        #   "app/main.py"
        # ]
        #
        # ---------------------------------------------------------

        for tool_name, result in execution_results.items():


            response_parts.append(
                f"\n{tool_name} result:"
            )


            if isinstance(
                result,
                (list, dict)
            ):

                response_parts.append(
                    json.dumps(
                        result,
                        indent=2,
                    )
                )

            else:

                response_parts.append(
                    str(result)
                )



        return "\n".join(
            response_parts
        )