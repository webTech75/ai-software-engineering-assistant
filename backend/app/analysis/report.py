from typing import Any


class ProjectAnalysisReportBuilder:
    """
    Combines all analyzer results into a single project report.
    """

    @staticmethod
    def build(
        code_quality: list[dict[str, Any]] | None = None,
        statistics: dict[str, Any] | None = None,
        structure: dict[str, Any] | None = None,
        technology: dict[str, Any] | None = None,
        dependencies: dict[str, Any] | None = None,
        security: list[dict[str, Any]] | None = None,
        tests: dict[str, Any] | None = None,
        bugs: list[dict[str, Any]] | None = None,
        api: dict[str, Any] | None = None,
        models: list[dict[str, Any]] | None = None,
        database: dict[str, Any] | None = None,
        metrics: dict[str, Any] | None = None,
        complexity: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        return {
            "code_quality": code_quality or [],
            "statistics": statistics or {},
            "structure": structure or {},
            "technology": technology or {},
            "dependencies": dependencies or {},
            "security": security or [],
            "tests": tests or {},
            "bugs": bugs or [],
            "api": api or {},
            "models": models or [],
            "database": database or {},
            "metrics": metrics or {},
            "complexity": complexity or {},
        }