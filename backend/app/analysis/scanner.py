from app.analysis.statistics import StatisticsAnalyzer
from app.analysis.structure import StructureAnalyzer
from app.analysis.technology import TechnologyAnalyzer
from app.analysis.bug import BugAnalyzer
from app.analysis.base import BaseAnalyzer
from app.analysis.quality import CodeQualityAnalyzer
from app.analysis.security import SecurityAnalyzer
from app.analysis.tests import TestAnalyzer
from app.analysis.dependency import DependencyAnalyzer
from app.analysis.api import APIAnalyzer
from app.analysis.models import ModelAnalyzer
from app.analysis.database import DatabaseAnalyzer
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
            DatabaseAnalyzer(),

            BugAnalyzer(),
            CodeQualityAnalyzer(),
            SecurityAnalyzer(),

            TestAnalyzer()
        ]

    def scan(self, project_directory: str) -> dict:
        """
        Run all analyzers against the project directory.
        """
        print(
            "SCANNER DIRECTORY:",
            project_directory
        )
        result = {}

        for analyzer in self.analyzers:

            print(
                f"Running {analyzer.__class__.__name__}"
            )

            try:
                result.update(
                    analyzer.analyze(project_directory)
                )

            except Exception as error:
                result[analyzer.__class__.__name__] = {
                    "error": str(error)
                }


        report = ProjectAnalysisReportBuilder.build(
            code_quality=result.get("code_quality"),
            statistics=result.get("statistics"),
            structure=result.get("structure"),
            technology=result.get("technology"),
            dependencies=result.get("dependencies"),
            security=result.get("security"),
            tests=result.get("tests"),
            bugs=result.get("bugs"),
            api=result.get("api"),
            models=result.get("models"),
            database=result.get("database"),
            metrics=result.get("metrics"),
            complexity=result.get("complexity"),
        )


        print("\n========== PROJECT REPORT ==========")

        for section, data in report.items():
            print(f"\n--- {section.upper()} ---")
            print(data)

        return report