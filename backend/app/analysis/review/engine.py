from typing import Any


class ProjectReviewEngine:

    def review(
        self,
        analysis: dict[str, Any]
    ) -> dict[str, Any]:


        summary = self.generate_summary(
            analysis
        )

        score = self.calculate_health_score(
            analysis
        )

        warnings = self.generate_warnings(
            analysis
        )

        strengths = self.generate_strengths(
            analysis
        )

        recommendations = self.generate_recommendations(
            analysis
        )

        return {
            "health_score": score,
            "summary": summary,
            "strengths": strengths,
            "warnings": warnings,
            "recommendations": recommendations,
            "file_issues": self.generate_file_issues(analysis)
        }
    

    def generate_file_issues(
        self,
        analysis: dict[str, Any]
    ) -> dict[str, list]:

        file_issues = {}


        def add_issue(file, issue):

            if not file:
                return

            if file not in file_issues:
                file_issues[file] = []

            file_issues[file].append(issue)


        # Bugs
        bugs = analysis.get(
            "bugs",
            {}
        )

        for issue in bugs.get("issues", []):

            add_issue(
                issue.get("file"),
                {
                    "type": "bug",
                    "severity": issue.get("severity"),
                    "message": issue.get("message"),
                    "line": issue.get("line")
                }
            )


        # Security
        security = analysis.get(
            "security",
            {}
        )

        for issue in security.get("issues", []):

            add_issue(
                issue.get("file"),
                {
                    "type": "security",
                    "severity": issue.get("severity"),
                    "message": issue.get("message"),
                    "line": issue.get("line")
                }
            )


        # Complexity
        complexity = analysis.get(
            "complexity",
            {}
        )

        for item in complexity.get(
            "highest_complexity",
            []
        ):

            if item.get("complexity", 0) >= 8:

                add_issue(
                    item.get("file"),
                    {
                        "type": "complexity",
                        "severity": "MEDIUM",
                        "message": (
                            f"High complexity function "
                            f"{item.get('function')}"
                        )
                    }
                )


        return file_issues
    

    def generate_summary(
        self,
        analysis: dict[str, Any]
    ) -> str:

        technology = analysis.get(
            "technology",
            {}
        )

        statistics = analysis.get(
            "statistics",
            {}
        )

        tests = analysis.get(
            "tests",
            {}
        )

        language = technology.get(
            "language",
            "Unknown"
        )

        framework = technology.get(
            "framework",
            "Unknown"
        )

        database = technology.get(
            "database",
            "Unknown"
        )

        total_files = statistics.get(
            "total_files",
            0
        )

        summary = (
            f"{language} project "
            f"using {framework} "
            f"with {database} database. "
            f"The project contains "
            f"{total_files} files."
        )


        if tests.get("exists"):
            summary += (
                " Automated tests are included."
            )

        return summary


    def calculate_health_score(
        self,
        analysis: dict[str, Any]
    ) -> int:

        score = 100

        # Security scoring
        security = analysis.get(
            "security",
            {}
        )

        security_issues = security.get(
            "issues",
            []
        )

        for issue in security_issues:
            severity = issue.get(
                "severity",
                "LOW"
            ).upper()

            if severity == "HIGH":
                score -= 15

            elif severity == "MEDIUM":
                score -= 8

            else:
                score -= 3


        # Bug scoring
        bugs = analysis.get(
            "bugs",
            {}
        )

        bug_issues = bugs.get(
            "issues",
            []
        )

        for issue in bug_issues:
            severity = issue.get(
                "severity",
                "LOW"
            ).upper()

            if severity == "HIGH":
                score -= 8

            elif severity == "MEDIUM":
                score -= 5

            else:
                score -= 1


        # Complexity scoring
        complexity = analysis.get(
            "complexity",
            {}
        )

        total_complexity = complexity.get(
            "total_complexity",
            0
        )

        if total_complexity > 200:
            score -= 10


        highest_complexity = complexity.get(
            "highest_complexity",
            []
        )

        for item in highest_complexity:
            if item.get("complexity", 0) >= 8:
                score -= 5
                break


        # Test scoring
        tests = analysis.get(
            "tests",
            {}
        )

        total_tests = tests.get(
            "total_test_files",
            0
        )

        if total_tests == 0:
            score -= 10


        return max(score, 0)


    def generate_warnings(
        self,
        analysis: dict[str, Any]
    ) -> list[str]:

        warnings = []

        complexity = analysis.get(
            "complexity",
            {}
        )

        highest = complexity.get(
            "highest_complexity",
            []
        )

        for item in highest:
            if item.get("complexity", 0) >= 8:
                warnings.append(
                    {
                        "type": "complexity",
                        "severity": "medium",
                        "file": item["file"],
                        "function": item["function"],
                        "message": "High complexity function"
                    }
                )


        bugs = analysis.get(
            "bugs",
            {}
        )

        for bug in bugs.get("issues", []):
            warnings.append(
                {
                    "type": "bug",
                    "severity": bug.get("severity", "LOW"),
                    "file": bug.get("file"),
                    "line": bug.get("line"),
                    "message": bug.get("message")
                }
            )

        security = analysis.get(
            "security",
            {}
        )

        for issue in security.get("issues", []):
            warnings.append(
                {
                    "type": "security",
                    "severity": issue.get("severity", "HIGH"),
                    "file": issue.get("file"),
                    "line": issue.get("line"),
                    "message": issue.get("message")
                }
            )


        return warnings


    def generate_strengths(
        self,
        analysis: dict[str, Any]
    ) -> list[str]:

        strengths = []

        technology = analysis.get(
            "technology",
            {}
        )

        if technology.get("framework"):
            strengths.append(
                f"Uses {technology['framework']} framework"
            )

        if technology.get("orm"):
            strengths.append(
                f"Uses {technology['orm']} ORM"
            )

        if technology.get("migration_tool"):
            strengths.append(
                f"Uses {technology['migration_tool']} for database migrations"
            )

        database = analysis.get(
            "database",
            {}
        )

        if database.get("engine"):
            strengths.append(
                f"Database configured: {database['engine']}"
            )

        tests = analysis.get(
            "tests",
            {}
        )

        if tests.get("exists"):
            strengths.append(
                "Project contains automated tests"
            )

        return strengths
    

    def generate_recommendations(
        self,
        analysis: dict[str, Any]
    ) -> list[str]:

        recommendations = []


        # Complexity recommendations
        complexity = analysis.get(
            "complexity",
            {}
        )

        highest = complexity.get(
            "highest_complexity",
            []
        )

        for item in highest:

            if item.get("complexity", 0) >= 8:

                recommendations.append(
                    f"Refactor {item.get('function')}() "
                    f"in {item.get('file')} to reduce complexity"
                )


        # Test recommendations
        tests = analysis.get(
            "tests",
            {}
        )

        total_tests = tests.get(
            "total_test_files",
            0
        )

        if total_tests == 0:

            recommendations.append(
                "Add automated tests to improve reliability"
            )


        # Security recommendations
        security = analysis.get(
            "security",
            {}
        )

        issues = security.get(
            "issues",
            []
        )

        for issue in issues:

            issue_type = issue.get(
                "type",
                ""
            )

            file = issue.get(
                "file",
                "unknown file"
            )

            if issue_type == "HARDCODED_SECRET":

                recommendations.append(
                    f"Remove hardcoded secret from {file}"
                )

            elif issue_type == "DANGEROUS_FUNCTION":

                recommendations.append(
                    f"Review dangerous function usage in {file}"
                )

            else:

                recommendations.append(
                    f"Review security issue in {file}"
                )


        # Bug recommendations
        bugs = analysis.get(
            "bugs",
            {}
        )

        bug_issues = bugs.get(
            "issues",
            []
        )

        for issue in bug_issues:

            recommendations.append(
                f"Resolve {issue.get('type')} issue "
                f"in {issue.get('file')} line {issue.get('line')}"
            )


        return recommendations