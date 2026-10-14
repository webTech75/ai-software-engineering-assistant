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