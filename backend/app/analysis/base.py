from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):
    """
    Base class for all project analyzers.
    """

    @abstractmethod
    def analyze(self, project_directory: str) -> dict:
        """
        Analyze a project and return structured data.
        """
        pass