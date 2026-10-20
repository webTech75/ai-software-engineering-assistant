"""
===============================================================================
File: planner.py
Path: app/agent/planner.py

Description:
    Creates execution plans for the AI software engineering agent.

Responsibilities:
    - Analyze user requests.
    - Detect user intent.
    - Determine required actions.
    - Select appropriate tools.
    - Prepare execution workflows.

Notes:
    - Does not execute tools.
    - Does not access the database directly.
    - Does not read project files directly.
    - Only creates execution plans.

Architecture:

    User Request
          |
          v
       Planner
          |
          v
    Execution Plan
          |
          v
      Executor
          |
          v
       Tools

Author:
    Amr Elhabbal
===============================================================================
"""

import re


class Planner:
    """
    Converts natural language requests into execution plans.

    The Planner decides WHAT needs to happen.

    The Executor decides HOW tools are executed.
    """


    def __init__(self):
        """
        Initialize planner.
        """
        pass



    def create_plan(
        self,
        request: str,
    ) -> dict:
        """
        Create an execution plan from a user request.

        General questions return an empty action list.

        This allows the LLM to answer normally without tools.

        task_type is used later by the LLM client
        to dynamically select token limits.
        """


        request_clean = request.strip().rstrip(").,")
        request_lower = request_clean.lower()


        # ---------------------------------------------------------
        # Default task type
        #
        # General conversation starts here.
        #
        # Example:
        #
        #   "what is dependency injection?"
        #
        # No tools required.
        # ---------------------------------------------------------

        task_type = "general"



        # ---------------------------------------------------------
        # Ignore general questions and normal conversation
        #
        # The LLM should answer directly.
        #
        # Examples:
        #
        #   "what you just did is awesome"
        #   "what is FastAPI?"
        #
        # ---------------------------------------------------------

        if not self.requires_project_context(
            request_lower
        ):

            return self.build_plan(
                request,
                task_type,
                [],
            )



        intent = self.detect_intent(
            request_lower
        )



        # ---------------------------------------------------------
        # Convert detected intent into task type
        #
        # task_type controls LLM behavior.
        #
        # Example:
        #
        # review -> larger response
        # general -> small response
        #
        # ---------------------------------------------------------

        task_type_map = {

            "bug_review": "bug_analysis",

            "security_review": "security_review",

            "quality_review": "quality_review",

            "file_review": "review",

            "file_read": "explain",

            "search": "search",

            "write": "write",

            "edit": "edit",

            "delete": "delete",

            "list_files": "list",

        }


        task_type = task_type_map.get(
            intent,
            "unknown_project",
        )



        # ---------------------------------------------------------
        # Create execution workflow
        # ---------------------------------------------------------

        if intent == "bug_review":

            plan = self.plan_bug_review(
                request
            )


        elif intent == "security_review":

            plan = self.plan_security_review(
                request
            )


        elif intent == "quality_review":

            plan = self.plan_quality_review(
                request
            )


        elif intent == "file_review":

            plan = self.plan_file_review(
                request
            )


        elif intent == "file_read":

            plan = self.plan_file_read(
                request
            )


        elif intent == "search":

            plan = self.plan_search(
                request
            )


        elif intent == "write":

            plan = self.plan_write(
                request
            )


        elif intent == "edit":

            plan = self.plan_edit(
                request
            )


        elif intent == "delete":

            plan = self.plan_delete(
                request
            )


        elif intent == "list_files":

            plan = self.plan_list_files(
                request
            )


        else:

            return self.build_plan(
                request,
                "general",
                [],
            )



        return self.build_plan(
            request,
            task_type,
            plan["actions"],
        )



    def build_plan(
        self,
        request: str,
        task_type: str,
        actions: list,
    ) -> dict:
        """
        Build a consistent execution plan.

        All planner responses should use this format.

        Example:

        {
            "goal": "...",
            "task_type": "review",
            "actions": []
        }
        """


        return {

            "goal": request,

            "task_type": task_type,

            "actions": actions,

        }



    def requires_project_context(
        self,
        request: str,
    ) -> bool:
        """
        Determine whether the request requires project tools.

        General programming questions should not trigger tools.

        Examples:

            "what is FastAPI?"
                False


            "review main.py"
                True


            "find UserService"
                True
        """


        # ---------------------------------------------------------
        # Direct file references
        #
        # These are strong signals.
        # ---------------------------------------------------------

        file_extensions = (

            ".py",
            ".js",
            ".ts",
            ".tsx",
            ".jsx",
            ".java",
            ".cpp",
            ".go",
            ".rs",
            ".md",
            ".json",
            ".yaml",
            ".yml",

        )


        if any(
            ext in request
            for ext in file_extensions
        ):

            return True



        # ---------------------------------------------------------
        # Project operation keywords
        # ---------------------------------------------------------

        project_keywords = [

            "project",

            "review",

            "inspect",

            "analyze",

            "analysis",

            "bug",

            "bugs",

            "error",

            "errors",

            "issue",

            "debug",

            "security",

            "vulnerability",

            "refactor",

            "quality",

            "read",

            "open",

            "edit",

            "modify",

            "update",

            "change",

            "create",

            "write",

            "generate",

            "delete",

            "remove",

            "list files",

        ]


        return any(
            keyword in request
            for keyword in project_keywords
        )

    def detect_intent(
        self,
        request: str,
    ) -> str:
        """
        Detect the requested project operation.

        Priority matters.

        Example:

            "find bugs in main.py"

        becomes:

            bug_review

        instead of:

            search
        """


        # ---------------------------------------------------------
        # Bug analysis
        # ---------------------------------------------------------

        if any(
            word in request
            for word in [
                "bug",
                "bugs",
                "error",
                "errors",
                "issue",
                "issues",
                "debug",
                "debugging",
                "broken",
                "wrong",
            ]
        ):

            return "bug_review"



        # ---------------------------------------------------------
        # Security review
        # ---------------------------------------------------------

        if any(
            word in request
            for word in [
                "security",
                "vulnerability",
                "vulnerabilities",
                "unsafe",
                "risk",
            ]
        ):

            return "security_review"



        # ---------------------------------------------------------
        # Code quality review
        # ---------------------------------------------------------

        if any(
            word in request
            for word in [
                "quality",
                "clean",
                "refactor",
                "improve",
                "maintainability",
                "best practice",
            ]
        ):

            return "quality_review"



        # ---------------------------------------------------------
        # File review
        # ---------------------------------------------------------

        if any(
            word in request
            for word in [
                "review",
                "inspect",
                "analyze",
            ]
        ):

            return "file_review"



        # ---------------------------------------------------------
        # Read / explain file
        # ---------------------------------------------------------

        if any(
            word in request
            for word in [
                "read",
                "open",
                "explain",
            ]
        ):

            return "file_read"



        # ---------------------------------------------------------
        # Delete file
        # ---------------------------------------------------------

        if any(
            word in request
            for word in [
                "delete",
                "remove",
            ]
        ):

            return "delete"



        # ---------------------------------------------------------
        # Create file
        # ---------------------------------------------------------

        if any(
            word in request
            for word in [
                "create",
                "write",
                "generate",
            ]
        ):

            return "write"



        # ---------------------------------------------------------
        # Edit file
        # ---------------------------------------------------------

        if any(
            word in request
            for word in [
                "edit",
                "modify",
                "update",
            ]
        ):

            return "edit"



        # ---------------------------------------------------------
        # Search project
        # ---------------------------------------------------------

        if (
            "search" in request
            or "find" in request
        ):

            return "search"



        # ---------------------------------------------------------
        # List files
        # ---------------------------------------------------------

        if (
            "list files" in request
            or "show files" in request
            or "project files" in request
        ):

            return "list_files"



        return "unknown"



    def plan_file_review(
        self,
        request: str,
    ) -> dict:
        """
        Workflow:

            search_text
                 |
                 v
             read_file
                 |
                 v
             LLM review
        """


        file_path = self.extract_file_path(
            request,
        )


        return {
            "actions": [
                {
                    "tool": "search_text",
                    "parameters": {
                        "query": file_path,
                        "search_type": "file",
                    },
                },
                {
                    "tool": "read_file",
                    "parameters": {
                        "path": "{{search_text.file}}",
                    },
                },
            ]
        }



    def plan_bug_review(
        self,
        request: str,
    ) -> dict:
        """
        Workflow for bug analysis.

        The LLM receives the source code
        after the file tool completes.
        """


        return self.plan_file_review(
            request
        )



    def plan_security_review(
        self,
        request: str,
    ) -> dict:
        """
        Workflow for security review.
        """


        return self.plan_file_review(
            request
        )



    def plan_quality_review(
        self,
        request: str,
    ) -> dict:
        """
        Workflow for quality review.
        """


        return self.plan_file_review(
            request
        )



    def plan_file_read(
        self,
        request: str,
    ) -> dict:
        """
        Read a specific file.
        """


        file_path = self.extract_file_path(
            request
        )


        return {
            "actions": [
                {
                    "tool": "read_file",
                    "parameters": {
                        "path": file_path,
                    },
                }
            ]
        }



    def plan_search(
        self,
        request: str,
    ) -> dict:
        """
        Search project files or content.
        """


        query = self.extract_search_query(
            request
        )


        return {
            "actions": [
                {
                    "tool": "search_text",
                    "parameters": {
                        "query": query,
                        "search_type": self.detect_search_type(
                            query
                        ),
                    },
                }
            ]
        }



    def plan_write(
        self,
        request: str,
    ) -> dict:
        """
        Create a new file.
        """


        return {
            "actions": [
                {
                    "tool": "write_file",
                    "parameters": {
                        "path": self.extract_file_path(
                            request
                        ),
                        "content": "",
                        "overwrite": False,
                    },
                }
            ]
        }



    def plan_edit(
        self,
        request: str,
    ) -> dict:
        """
        Edit existing file.
        """


        return {
            "actions": [
                {
                    "tool": "edit_file",
                    "parameters": {
                        "path": self.extract_file_path(
                            request
                        ),
                        "old_text": "",
                        "new_text": "",
                    },
                }
            ]
        }



    def plan_delete(
        self,
        request: str,
    ) -> dict:
        """
        Delete file.
        """


        return {
            "actions": [
                {
                    "tool": "delete_file",
                    "parameters": {
                        "path": self.extract_file_path(
                            request
                        ),
                    },
                }
            ]
        }



    def plan_list_files(
        self,
        request: str,
    ) -> dict:
        """
        List project files.
        """


        return {
            "actions": [
                {
                    "tool": "list_files",
                    "parameters": {},
                }
            ]
        }



    def extract_file_path(
        self,
        request: str,
    ) -> str:
        """
        Extract filename from request.

        Supports:
            main.py
            package.json
            LICENSE
            README
            Dockerfile
        """

        known_files = (
            "license",
            "readme",
            "dockerfile",
            "makefile",
            "procfile",
            ".env",
        )

        extensions = (
            ".py",
            ".js",
            ".ts",
            ".tsx",
            ".jsx",
            ".java",
            ".cpp",
            ".go",
            ".rs",
            ".md",
            ".json",
            ".yaml",
            ".yml",
            ".toml",
        )

        common_files = (
    "license",
    "readme",
    "dockerfile",
    "makefile",
    ".gitignore",
    ".env",
    "procfile",
)


        for word in request.split():

            cleaned = word.rstrip(").,:'\"")

            lower_word = cleaned.lower()

            if cleaned.endswith(extensions):
                return cleaned

            if lower_word in common_files:
                return cleaned



    def extract_search_query(
        self,
        request: str,
    ) -> str:
        """
        Extract search phrase.
        """


        match = re.search(
            r"(?:search|find)\s+(?:for\s+)?(.+)",
            request,
            re.IGNORECASE,
        )


        if match:

            return match.group(1).strip()


        return ""



    def detect_search_type(
        self,
        query: str,
    ) -> str:
        """
        Decide filename search vs content search.
        """


        extensions = (
            ".py",
            ".js",
            ".ts",
            ".tsx",
            ".jsx",
            ".java",
            ".cpp",
            ".go",
            ".rs",
            ".md",
            ".json",
            ".yaml",
            ".yml",
        )


        if query.endswith(
            extensions
        ):

            return "file"


        return "content"