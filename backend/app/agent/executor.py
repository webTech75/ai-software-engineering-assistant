"""
===============================================================================
File: executor.py
Path: app/agent/executor.py

Description:
    Executes actions created by the Planner.

Responsibilities:
    - Receive execution plans.
    - Select tools from ToolRegistry.
    - Pass project filesystem information.
    - Collect tool results.

Does NOT:
    - Create plans.
    - Perform reasoning.
    - Access database directly.

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
        project,
    ) -> dict:
        """
        Execute the generated plan.

        Project contains:

            project.id
            project.name
            project.project_directory

        Tools receive:

            project.project_directory
        """

        results = {}

        project_directory = (
            project.project_directory
        )


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


            print(
                "TOOL:",
                tool_name
            )

            print(
                "PARAMETERS:",
                parameters
            )


            try:

                results[tool_name] = tool.execute(
                    project_directory=project_directory,
                    **parameters,
                )


            except Exception as error:

                logger.exception(
                    "Tool execution failed"
                )

                results[tool_name] = {
                    "error": str(error)
                }


        return results