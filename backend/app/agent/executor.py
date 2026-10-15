"""
===============================================================================
File:
    app/agent/executor.py

Description:
    Executes actions created by the Planner.

Responsibilities:
    - Receive execution plans.
    - Select tools from ToolRegistry.
    - Provide tool execution context.
    - Collect tool results.

Does NOT:
    - Create plans.
    - Perform reasoning.
    - Access database directly.
    - Manage project objects.

Author:
    Amr Elhabbal
===============================================================================
"""

import logging

from app.agent.tool_registry import ToolRegistry


logger = logging.getLogger(__name__)


class Executor:
    """
    Executes tools selected by the Planner.
    """

    def __init__(self):

        self.registry = ToolRegistry()

    def resolve_parameters(
        self,
        parameters: dict,
        results: dict,
    ) -> dict:
        """
        Replace references to previous tool results.

        Example:
            {{search_text.path}}

        becomes:

            app/services/project_service.py
        """

        resolved = {}

        for key, value in parameters.items():

            if isinstance(value, str) and value.startswith("{{"):

                reference = (
                    value
                    .replace("{{", "")
                    .replace("}}", "")
                )

                parts = reference.split(".")

                if len(parts) == 2:

                    tool_name = parts[0]
                    field = parts[1]

                    tool_result = results.get(
                        tool_name
                    )

                    if isinstance(tool_result, list):
                        tool_result = tool_result[0]

                    if isinstance(tool_result, dict):
                        resolved[key] = tool_result.get(field)

                        continue

            resolved[key] = value

        return resolved
        
    def execute(
        self,
        plan: dict,
        project_directory: str,
    ) -> dict:
        """
        Execute the generated plan.

        Tools receive only the information
        they need.

        Example:
            project_directory
            file path
            search query
        """

        results = {}

        if not plan:
            return {}


        for action in plan.get(
            "actions",
            []
        ):

            tool_name = action.get(
                "tool"
            )


            parameters = action.get(
                "parameters",
                {}
            )


            tool = self.registry.get(
                tool_name
            )


            if not tool:

                results[tool_name] = {
                    "error": "Tool not found"
                }

                continue


            logger.info(
                "Executing tool: %s",
                tool_name,
            )


            try:

                if (
                    "project_directory"
                    not in parameters
                ):
                    parameters[
                        "project_directory"
                    ] = project_directory


                print("================ TOOL CALL ================")
                print("TOOL:", tool_name)
                print("ARGUMENTS:", parameters)
                print("==========================================")

                parameters = self.resolve_parameters(
                    parameters,
                    results,
                )


                results[tool_name] = tool.execute(
                    **parameters,
                )


            except Exception as error:

                logger.exception(
                    "Tool execution failed"
                )

                results[tool_name] = {
                    "error": str(error),
                    "type": type(error).__name__,
                }


        return results