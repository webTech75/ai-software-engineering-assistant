"""
Abstract base class defining the interface for all AI tools.

Author: Amr Elhabbal | Powered by Meta AI Muse
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
