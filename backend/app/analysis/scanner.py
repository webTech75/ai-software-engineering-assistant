"""
Coordinates project analyzers and builds complete analysis reports.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

from app.analysis.statistics import StatisticsAnalyzer
from app.analysis.structure import StructureAnalyzer
from app.analysis.technology import TechnologyAnalyzer
from app.analysis.base import BaseAnalyzer
from app.analysis.tests import TestAnalyzer
from app.analysis.dependency import DependencyAnalyzer
from app.analysis.api import APIAnalyzer
from app.analysis.models import ModelAnalyzer
from app.analysis.metrics import MetricsAnalyzer
from app.analysis.complexity import ComplexityAnalyzer
from app.analysis.report import ProjectAnalysisReportBuilder


class ProjectScanner:
    """
    Coordinates all project analyzers and returns a complete analysis report.
    """

    def __init__(self):

        self.analyzers: list[BaseAnalyzer] = [
            StatisticsAnalyzer(),
            StructureAnalyzer(),
            MetricsAnalyzer(),
            TechnologyAnalyzer(),
            DependencyAnalyzer(),
            ComplexityAnalyzer(),
            APIAnalyzer(),
            ModelAnalyzer(),
            TestAnalyzer(),
        ]

    def scan(self, project_directory: str) -> dict:
        """
        Run all analyzers against the project directory.
        """
        print("SCANNER DIRECTORY:", project_directory)
        result = {}

        for analyzer in self.analyzers:

            print(f"Running {analyzer.__class__.__name__}")

            try:
                result.update(analyzer.analyze(project_directory))

            except Exception as error:
                import traceback

                print(f"ERROR in {analyzer.__class__.__name__}: {error}")

                traceback.print_exc()

                result[analyzer.__class__.__name__] = {"error": str(error)}

        report = ProjectAnalysisReportBuilder.build(
            statistics=result.get("statistics"),
            technology=result.get("technology"),
            structure=result.get("structure"),
            dependencies=result.get("dependencies"),
            api=result.get("api"),
            metrics=result.get("metrics"),
            complexity=result.get("complexity"),
            tests=result.get("tests"),
        )

        return report
