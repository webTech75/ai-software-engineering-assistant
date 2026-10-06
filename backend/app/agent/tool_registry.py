"""
===============================================================================
File: tool_registry.py
Path: app/agent/tool_registry.py

Description:
    Registers every tool available to the AI assistant.

Responsibilities:
    - Create tool instances.
    - Provide tool schemas to the LLM.
    - Retrieve tools by name.
    - Maintain a single source of truth for available tools.

Architecture:

             AgentService
                  │
                  ▼
           Tool Registry
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
  ReadFile   WriteFile   ListFiles
                  │
                  ▼
             Project Filesystem

Dependencies:
    - All tool implementations

Author:
    Amr Elhabbal
===============================================================================
"""

from app.agent.tools.list_files import ListFilesTool
from app.agent.tools.read_file import ReadFileTool
from app.agent.tools.search_text import SearchTextTool
from app.agent.tools.write_file import WriteFileTool
from app.agent.tools.edit_file import EditFileTool
from app.agent.tools.delete_file import DeleteFileTool


class ToolRegistry:
    """Stores and provides access to all agent tools."""

    def __init__(self):
        tools = [
            ListFilesTool(),
            ReadFileTool(),
            SearchTextTool(),
            WriteFileTool(),
            EditFileTool(),
            DeleteFileTool(),
        ]

        self._tools = {
            tool.name: tool
            for tool in tools
        }

    def get(self, name: str):
        return self._tools.get(name)

    @property
    def schemas(self):
        return [
            tool.schema
            for tool in self._tools.values()
        ]