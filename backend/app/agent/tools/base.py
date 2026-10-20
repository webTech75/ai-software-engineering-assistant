"""
===============================================================================
File: base.py
Path: app/agent/tools/base.py

Description:
    Defines the abstract base class for every AI tool.

Responsibilities:
    - Define the interface every tool must implement.
    - Ensure consistency across all tools.
    - Provide tool metadata for the LLM.
    - Standardize tool execution.

Architecture:

                BaseTool
                   ▲
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ReadFile   WriteFile   DeleteFile
        ▲          ▲          ▲
        └──────────┼──────────┘
                   ▼
             Tool Registry
                   ▼
                 Agent

Every tool must provide:

    • name
        Unique tool identifier.

    • description
        Natural language description shown to the LLM.

    • schema
        JSON schema defining tool parameters.

    • execute()
        Business logic executed by the application.

Execution Flow:

        Agent
          |
          v
   Tool Registry
          |
          v
     BaseTool API
          |
          v
   Specific Tool
          |
          v
   Project Filesystem

Dependencies:
    - abc

Author:
    Amr Elhabbal
===============================================================================
"""

from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Abstract interface for all AI tools.

    Every tool must implement:

        name
        description
        schema
        execute()
    """


    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique tool identifier.

        Example:

            read_file
        """

        pass



    @property
    @abstractmethod
    def description(self) -> str:
        """
        Description displayed to the LLM.
        """

        pass



    @property
    @abstractmethod
    def schema(self) -> dict:
        """
        JSON schema for tool parameters.

        Used for future LLM function calling.
        """

        pass



    @abstractmethod
    def execute(
        self,
        project_directory: str,
        **kwargs,
    ) -> dict:
        """
        Execute the tool.

        Args:

            project_directory:
                Root directory of the project.

            kwargs:
                Tool-specific parameters.

        Returns:

            Dictionary containing execution result.
        """

        pass