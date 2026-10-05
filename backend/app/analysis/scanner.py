from app.analysis.statistics import StatisticsAnalyzer
from app.analysis.structure import StructureAnalyzer
from app.analysis.technology import TechnologyAnalyzer
from app.analysis.base import BaseAnalyzer


class ProjectScanner:
    """
    Coordinates all project analyzers and returns a complete analysis report.
    """

    def __init__(self):
        self.analyzers: list[BaseAnalyzer] = [
        StatisticsAnalyzer(),
        TechnologyAnalyzer(),
        StructureAnalyzer(),
    ]

    def scan(self, project_directory: str) -> dict:
        """
        Run all analyzers against the project directory.
        """

        result = {}

        for analyzer in self.analyzers:
            result.update(
                analyzer.analyze(project_directory)
            )

        return result