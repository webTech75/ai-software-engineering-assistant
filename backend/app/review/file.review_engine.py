"""
===============================================================================
File:
    app/review/project_review_engine.py

Description:
    Project-level review engine.

Responsibilities:
    - Receive project summary information.
    - Prepare high-level project context.
    - Generate architecture and design review.

Does NOT:
    - Review individual files.
    - Detect code bugs.
    - Perform line-level analysis.
    - Provide code fixes.
    - Modify project files.

Author:
    Amr Elhabbal
===============================================================================
"""

from typing import Any

from app.ai.llm.client import LLMClient


class ProjectReviewEngine:
    """
    Converts project summary information into a
    high-level software engineering review.
    """

    def __init__(self):

        self.llm = LLMClient()


    def review(
        self,
        project_summary: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Generate project-level engineering review.
        """

        prompt = f"""
        You are a senior software architect.

        Evaluate the following software project.

        This is a PROJECT LEVEL REVIEW ONLY.

        Focus on:

        - architecture quality
        - technology choices
        - project organization
        - maintainability
        - scalability
        - overall design improvements


        Do NOT:

        - review individual files
        - find bugs
        - analyze source code
        - provide line-level fixes
        - suggest refactoring specific functions


        Return a concise overview:

        1. Project summary
        2. Architecture assessment
        3. Technology assessment
        4. Project strengths
        5. Improvement recommendations
        6. Overall assessment


        Project information:

        {project_summary}
        """


        response = self.llm.generate(
            prompt
        )


        return {
            "type": "project_review",
            "summary": response
        }