"""
===============================================================================
File:
    app/agent/executor.py

Description:
    Executes actions created by the Planner.

Responsibilities:
    - Receive execution plans.
    - Select tools from ToolRegistry.
    - Provide execution context.
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

from app.file_system.file_manager import FileManager

from app.agent.tool_registry import ToolRegistry


logger = logging.getLogger(__name__)



class Executor:
    """
    Executes tools selected by the Planner.
    """


    def __init__(
        self,
        registry: ToolRegistry | None = None,
        file_manager: FileManager | None = None,
    ):
        """
        Initialize executor.

        Dependencies are injected so the
        executor remains testable.
        """

        self.file_manager = (
            file_manager
            or FileManager()
        )


        self.registry = (
            registry
            or ToolRegistry(
                self.file_manager
            )
        )



    def resolve_parameters(
        self,
        parameters: dict,
        results: dict,
    ) -> dict:
        """
        Resolve references from previous tools.

        Example:

            {{search_text.file}}

        becomes:

            app/main.py
        """

        resolved = {}


        for key, value in parameters.items():

            if (
                isinstance(value, str)
                and value.startswith("{{")
            ):

                reference = (
                    value
                    .replace("{{", "")
                    .replace("}}", "")
                )


                parts = reference.split(".")


                if len(parts) == 2:

                    tool_name, field = parts


                    previous = results.get(
                        tool_name
                    )


                    if isinstance(
                        previous,
                        dict,
                    ):

                        resolved[key] = (
                            previous.get(field)
                        )

                        continue


            resolved[key] = value


        return resolved



    def execute(
        self,
        plan: dict,
        project_directory: str,
    ) -> dict:
        """
        Execute planner actions.

        Returns:

        {
            "tool_name": {
                "success": True,
                "data": ...
            }
        }
        """

        results: dict = {}


        if not plan:

            return results



        actions = plan.get(
            "actions",
            [],
        )



        for action in actions:

            tool_name = action.get(
                "tool"
            )


            parameters = action.get(
                "parameters",
                {},
            )


            if not tool_name:

                continue



            tool = self.registry.get(
                tool_name
            )


            if not tool:

                results[tool_name] = {
                    "success": False,
                    "error": "Tool not found",
                }

                continue



            try:

                logger.info(
                    "Executing tool: %s",
                    tool_name,
                )


                parameters = (
                    self.resolve_parameters(
                        parameters,
                        results,
                    )
                )


                # Inject project context
                parameters.setdefault(
                    "project_directory",
                    project_directory,
                )



                if any(
                    value is None
                    for value in parameters.values()
                ):

                    results[tool_name] = {
                        "success": False,
                        "error": (
                            "Missing required "
                            "tool parameter"
                        ),
                        "parameters": parameters,
                    }

                    continue



                logger.debug(
                    "Tool arguments: %s",
                    parameters,
                )


                output = tool.execute(
                    **parameters
                )


                results[tool_name] = {
                    "success": True,
                    "data": output,
                }



            except Exception as error:

                logger.exception(
                    "Tool failed: %s",
                    tool_name,
                )


                results[tool_name] = {
                    "success": False,
                    "error": str(error),
                    "type": (
                        type(error).__name__
                    ),
                }



        return results