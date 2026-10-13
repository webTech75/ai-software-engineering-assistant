"""
===============================================================================
File: analyze_project.py
Path: app/agent/tools/analyze_project.py

Description:
    Tool used by the AI assistant to analyze a software project.

Responsibilities:
    - Trigger project analysis.
    - Execute ProjectScanner.
    - Return engineering analysis report.

Architecture:

    AgentService
          |
          v
    AnalyzeProjectTool
          |
          v
    ProjectScanner
          |
          v
    ProjectReportBuilder

Author:
    Amr Elhabbal
===============================================================================
"""

from typing import Any

from app.agent.tools.base import BaseTool
from app.analysis.scanner import ProjectScanner


class AnalyzeProjectTool(BaseTool):
    """
    Analyze a software project and generate an engineering report.
    """

    name = "analyze_project"

    description = """
    Analyze a software project and provide an engineering review.

    Use this tool when the user asks for:
    - project review
    - code analysis
    - architecture feedback
    - bugs and fixes
    - improvement suggestions
    - missing implementations

    The analysis includes:
    - technology stack
    - project structure
    - dependencies
    - security findings
    - bugs
    - code quality issues
    - complexity metrics
    - API information
    - database information
    - code metrics
    """

    @property
    def schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_directory": {
                            "type": "string",
                            "description": (
                                "Path to the project directory "
                                "that should be analyzed."
                            ),
                        }
                    },
                    "required": [
                        "project_directory"
                    ],
                },
            },
        }

    def execute(
        self,
        project_directory: str,
        **kwargs
    ) -> dict[str, Any]:
        """
        Run project analysis.
        """
        
        print(
            "ANALYZE TOOL DIRECTORY:",
            project_directory
        ) 

        try:
            scanner = ProjectScanner()

            report = scanner.scan(
                project_directory
            )

            return {
                "success": True,
                "instruction": (
                    "Review this project analysis and provide "
                    "a software engineering assessment. "
                    "Prioritize bugs, security issues, "
                    "missing implementations, and improvements."
                ),
                "report": report,
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error),
            }