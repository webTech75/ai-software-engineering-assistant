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
            "file_issues": self.generate_file_issues(
                analysis
            )
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

            file_issues[file].append(
                issue
            )


        # Bugs

        bugs = analysis.get(
            "bugs",
            {}
        )

        for issue in bugs.get(
            "issues",
            []
        ):

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

        for issue in security.get(
            "issues",
            []
        ):

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

            if item.get(
                "complexity",
                0
            ) >= 8:

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


        languages = technology.get(
            "languages",
            []
        )

        frameworks = technology.get(
            "frameworks",
            []
        )

        database = technology.get(
            "database"
        )


        language_text = (
            ", ".join(languages)
            if languages
            else "Unknown language"
        )

        framework_text = (
            ", ".join(frameworks)
            if frameworks
            else "Unknown framework"
        )

        database_text = (
            database
            if database
            else "no detected database"
        )


        total_files = statistics.get(
            "total_files",
            0
        )


        summary = (
            f"{language_text} project "
            f"using {framework_text} "
            f"with {database_text}. "
            f"The project contains "
            f"{total_files} files."
        )


        if tests.get(
            "exists"
        ):
            summary += (
                " Automated tests are included."
            )

        return summary
    

    def calculate_health_score(
        self,
        analysis: dict[str, Any]
    ) -> int:

        scores = {}

        # Security score
        security = analysis.get(
            "security",
            {}
        )

        security_issues = security.get(
            "issues",
            []
        )

        security_count = len(security_issues)

        scores["security"] = round(
            100 / (1 + security_count * 0.25)
        )


        # Bug score
        bugs = analysis.get(
            "bugs",
            {}
        )

        bug_count = len(
            bugs.get(
                "issues",
                []
            )
        )

        scores["bugs"] = round(
            100 / (1 + bug_count * 0.1)
        )


        # Complexity score
        complexity = analysis.get(
            "complexity",
            {}
        )

        complexity_count = complexity.get(
            "total_complexity",
            0
        )

        scores["complexity"] = round(
            100 / (1 + complexity_count * 0.1)
        )


        # Tests score
        tests = analysis.get(
            "tests",
            {}
        )

        test_files = tests.get(
            "total_test_files",
            0
        )

        scores["tests"] = (
            100
            if test_files > 0
            else 0
        )


        health_score = (
            scores["security"] * 0.30 +
            scores["bugs"] * 0.30 +
            scores["complexity"] * 0.20 +
            scores["tests"] * 0.20
        )


        return round(health_score)



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

            if item.get(
                "complexity",
                0
            ) >= 8:

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


        for bug in bugs.get(
            "issues",
            []
        ):

            warnings.append(
                {
                    "type": "bug",
                    "severity": bug.get(
                        "severity",
                        "LOW"
                    ),
                    "file": bug.get(
                        "file"
                    ),
                    "line": bug.get(
                        "line"
                    ),
                    "message": bug.get(
                        "message"
                    )
                }
            )



        security = analysis.get(
            "security",
            {}
        )


        for issue in security.get(
            "issues",
            []
        ):

            warnings.append(
                {
                    "type": "security",
                    "severity": issue.get(
                        "severity",
                        "HIGH"
                    ),
                    "file": issue.get(
                        "file"
                    ),
                    "line": issue.get(
                        "line"
                    ),
                    "message": issue.get(
                        "message"
                    )
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


        frameworks = technology.get(
            "frameworks",
            []
        )

        orms = technology.get(
            "orms",
            []
        )

        migration_tools = technology.get(
            "migration_tools",
            []
        )


        for framework in frameworks:

            strengths.append(
                f"Uses {framework} framework"
            )


        for orm in orms:

            strengths.append(
                f"Uses {orm} ORM"
            )


        for migration_tool in migration_tools:

            strengths.append(
                f"Uses {migration_tool} for database migrations"
            )



        database = analysis.get(
            "database",
            {}
        )


        if database.get(
            "engine"
        ):

            strengths.append(
                f"Database configured: {database['engine']}"
            )



        tests = analysis.get(
            "tests",
            {}
        )


        if tests.get(
            "exists"
        ):

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

            if item.get(
                "complexity",
                0
            ) >= 8:

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
                f"in {issue.get('file')} "
                f"line {issue.get('line')}"
            )


        return recommendations