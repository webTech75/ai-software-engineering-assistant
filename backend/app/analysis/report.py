from typing import Any


class ProjectAnalysisReportBuilder:
    """
    Builds factual project analysis reports.

    Purpose:
        - Combine analyzer results.
        - Provide structured project information.
        - Prepare data for project review.

    Does NOT:
        - Generate recommendations.
        - Evaluate architecture quality.
        - Find code issues.
        - Produce AI responses.

    AI interpretation happens in:
        ProjectReviewEngine
    """

    @staticmethod
    def build(
        statistics: dict[str, Any] | None = None,
        technology: dict[str, Any] | None = None,
        structure: dict[str, Any] | None = None,
        dependencies: dict[str, Any] | None = None,
        api: dict[str, Any] | None = None,
        database: dict[str, Any] | None = None,
        metrics: dict[str, Any] | None = None,
        complexity: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Create a factual project analysis report.

        This report describes:
            - Project statistics.
            - Technology stack.
            - Architecture structure.
            - Dependencies.
            - Technical information.

        It intentionally avoids:
            - Recommendations.
            - Code review comments.
            - Bug reports.
        """

        return {
            "statistics": statistics or {},

            "technology": technology or {},

            "structure": structure or {},

            "dependencies": dependencies or {},

            "api": api or {},

            "database": database or {},

            "metrics": metrics or {},

            "complexity": complexity or {},
        }