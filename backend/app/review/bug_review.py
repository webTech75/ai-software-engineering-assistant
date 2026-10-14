"""
===============================================================================
File: bug_review.py
Path: app/review/bug_review.py

Description:
    Converts bug analyzer findings into developer review feedback.

Responsibilities:
    - Review bug findings.
    - Add recommendations.
    - Normalize bug output.

Does NOT:
    - Scan files.
    - Analyze source code.
    - Access database.

Author:
    Amr Elhabbal
===============================================================================
"""


class BugReview:
    """
    Reviews detected bugs and creates actionable feedback.
    """

    def review(
        self,
        bugs: list[dict]
    ) -> list[dict]:

        findings = []

        for bug in bugs:

            findings.append(
                {
                    "category": "bug",
                    "severity": bug.get(
                        "severity",
                        "UNKNOWN"
                    ),
                    "file": bug.get(
                        "file"
                    ),
                    "line": bug.get(
                        "line"
                    ),
                    "problem": bug.get(
                        "message"
                    ),
                    "recommendation": self._recommend(
                        bug
                    ),
                }
            )

        return findings


    def _recommend(
        self,
        bug: dict
    ) -> str:

        bug_type = bug.get(
            "type",
            ""
        )

        if bug_type == "TODO":

            return (
                "Complete the unfinished task "
                "or remove the TODO comment."
            )


        if bug_type == "FIXME":

            return (
                "Review and resolve this "
                "unfinished implementation."
            )


        return (
            "Investigate this issue "
            "and determine the appropriate fix."
        )