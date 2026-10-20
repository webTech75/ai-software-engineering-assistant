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
from app.analysis.review.engine import ProjectReviewEngine


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
            statistics=result.get("statistics"),
            technology=result.get("technology"),
            structure=result.get("structure"),
            dependencies=result.get("dependencies"),
            api=result.get("api"),
            database=result.get("database"),
            metrics=result.get("metrics"),
            complexity=result.get("complexity"),
            bugs=result.get("bugs"),
            quality=result.get("quality"),
            security=result.get("security"),
            tests=result.get("tests"),
        )
        print("\n========== PROJECT REPORT ==========")

        
        review_engine = ProjectReviewEngine()

        report["review"] = review_engine.review(report)
        
        for section, data in report.items():
            print(f"\n--- {section.upper()} ---")
            print(data)

        return report