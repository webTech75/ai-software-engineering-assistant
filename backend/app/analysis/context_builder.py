"""
Builds structured project context from analysis results for AI responses.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

from typing import Any


class ProjectContextBuilder:

    @staticmethod
    def _build_project_type(report: dict[str, Any]) -> str:

        technology = report.get("technology", {})

        frameworks = technology.get("frameworks", [])
        database = technology.get("database")
        api = report.get("api", {})

        has_react = "React" in frameworks
        has_api = api.get("total_routes", 0) > 0

        if has_react and has_api:
            return "Full-stack web application"

        if has_react:
            return "Frontend web application"

        if has_api:
            return "Backend API application"

        if database:
            return "Database-driven application"

        return "Software project"

    @staticmethod
    def _build_architecture_context(report: dict[str, Any]) -> str:
        technology = report.get("technology", {})
        api = report.get("api", {})
        structure = report.get("structure", {})
        files = structure.get("files", [])

        architecture = []

        frameworks = technology.get("frameworks", [])
        database = technology.get("database")

        # Application type
        if "React" in frameworks:
            architecture.append("- Frontend React application")

        if api.get("total_routes", 0) > 0:
            architecture.append("- REST API endpoints detected")

        if database:
            architecture.append("- Database layer detected")

        # Detect common architecture patterns from files
        file_paths = " ".join(files).lower()

        # Authentication
        auth_keywords = [
            "auth",
            "login",
            "register",
            "signup",
            "user",
        ]

        if any(keyword in file_paths for keyword in auth_keywords):
            architecture.append("- Authentication and user management features")

        # Component architecture
        if "/components/" in file_paths or "\\components\\" in file_paths:
            architecture.append("- Component-based UI architecture")

        # Service/repository pattern
        if "service" in file_paths or "repository" in file_paths:
            architecture.append("- Service-oriented application structure")

        # API communication
        if "/api/" in file_paths or "\\api\\" in file_paths:
            architecture.append("- API communication layer detected")

        if not architecture:
            architecture.append("- No architecture patterns detected")

        return ", ".join(architecture)

    @staticmethod
    def build(project_name: str, analysis: dict[str, Any]) -> str:

        report = analysis.get("report", analysis)

        technology = report.get("technology", {})
        statistics = report.get("statistics", {})
        structure = report.get("structure", {})
        dependencies = report.get("dependencies", {})
        architecture_context = ProjectContextBuilder._build_architecture_context(report)
        project_type = ProjectContextBuilder._build_project_type(report)
        languages = technology.get("languages", [])
        frameworks = technology.get("frameworks", [])

        return f"""
            Project: {project_name}

            Project Type:
            - {project_type}
            
            Project Overview:
            - Total files: {statistics.get("total_files", 0)}
            - Total directories: {statistics.get("total_directories", 0)}

            Technology Stack:
            - Languages: {", ".join(languages) if languages else "Unknown"}
            - Frameworks: {", ".join(frameworks) if frameworks else "Unknown"}
            - Package manager: {technology.get("package_manager", "Unknown")}
            - Build tools: {", ".join(technology.get("build_tools", []))}

            Styling:
            - {", ".join(technology.get("styling_tools", []))}

            Dependencies:
            - Manager: {dependencies.get("manager", "Unknown")}

            Project Structure:
            - Files detected: {len(structure.get("files", []))}

            Architecture:
            {architecture_context}
            """
