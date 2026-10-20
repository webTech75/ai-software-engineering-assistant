"""
===============================================================================
File:
    app/agent/tool_registry.py

Description:
    Registers tools available to the AI assistant.

Responsibilities:
    - Create tool instances.
    - Retrieve tools by name.
    - Provide tool schemas.

Does NOT:
    - Execute tools.
    - Perform reasoning.
    - Create execution plans.

Author:
    Amr Elhabbal
===============================================================================
"""

from app.file_system.file_manager import FileManager

from app.agent.tools.base import BaseTool

from app.agent.tools.list_files import ListFilesTool
from app.agent.tools.read_file import ReadFileTool
from app.agent.tools.search_text import SearchTextTool
from app.agent.tools.write_file import WriteFileTool
from app.agent.tools.edit_file import EditFileTool
from app.agent.tools.delete_file import DeleteFileTool


class ToolRegistry:
    """
    Central registry for available tools.

    The registry is the single source
    of truth for agent capabilities.
    """

    def __init__(
        self,
        file_manager: FileManager | None = None,
        custom_tools: list[BaseTool] | None = None,
    ):
        """
        Initialize registry.

        FileManager is injected so tools
        remain testable.

        custom_tools allows adding tools
        without modifying the registry.
        """

        file_manager = (
            file_manager
            or FileManager()
        )


        tools: list[BaseTool] = (
            custom_tools
            if custom_tools is not None
            else [
                ListFilesTool(file_manager),
                ReadFileTool(file_manager),
                SearchTextTool(file_manager),
                WriteFileTool(file_manager),
                EditFileTool(file_manager),
                DeleteFileTool(file_manager),
            ]
        )


        self._tools: dict[str, BaseTool] = {}


        for tool in tools:

            if tool.name in self._tools:

                raise ValueError(
                    f"Duplicate tool registered: {tool.name}"
                )

            self._tools[tool.name] = tool



    def get(
        self,
        name: str,
    ) -> BaseTool | None:
        """
        Retrieve a tool by name.

        Example:

            registry.get("read_file")
        """

        return self._tools.get(name)



    def get_schemas(
        self,
    ) -> list[dict]:
        """
        Return tool schemas.

        Used later for LLM
        function calling.
        """

        return [
            tool.schema
            for tool in self._tools.values()
        ]



    @property
    def tools(
        self,
    ) -> dict[str, BaseTool]:
        """
        Return registered tools.

        Useful for debugging
        and testing.
        """

        return self._tools