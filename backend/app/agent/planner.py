"""
===============================================================================
File: planner.py
Path: app/agent/planner.py

Description:
    Creates execution plans for the AI software engineering agent.

Responsibilities:
    - Analyze user requests.
    - Determine required actions.
    - Select appropriate tools.
    - Prepare a workflow for execution.

Notes:
    - Does not execute tools.
    - Does not access the database directly.
    - Only creates plans.

Author:
    Amr Elhabbal
===============================================================================
"""

import re


class Planner:
    """
    Responsible for creating execution plans
    based on user requests.
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
        """

        request_clean = request.strip().rstrip(").,")
        request_lower = request_clean.lower()

        actions = []


        # ---------------------------------------------------------
        # Read a file
        #
        # Examples:
        #   Read app/main.py
        #   Show README.md
        #   Explain app/services/user_service.py
        # ---------------------------------------------------------

        if (
            "read" in request_lower
            or "show" in request_lower
            or "explain" in request_lower
        ):

            path_match = re.search(
                r"(?:read|show|explain)\s+([^\s]+)",
                request,
                re.IGNORECASE,
            )

            file_path = ""

            if path_match:
                file_path = path_match.group(1)


            actions.append(
                {
                    "tool": "read_file",
                    "parameters": {
                        "path": file_path,
                    },
                }
            )


        # ---------------------------------------------------------
        # Write / Create file
        #
        # Examples:
        #   Create file test/amr.py
        #   Write app/test.py
        #   Generate a new file
        # ---------------------------------------------------------

        if (
            (
            "create" in request_lower
            or "write" in request_lower
            or "generate" in request_lower
            )
            and "delete" not in request_lower
            and "remove" not in request_lower
        ):

            path_match = re.search(
                r"(?:create|write|generate)\s+(?:file\s+)?([^\s]+)",
                request,
                re.IGNORECASE,
            )

            file_path = ""

            if path_match:
                file_path = path_match.group(1)


            content_match = re.search(
                r"(?:with|content:)\s*(.*)",
                request,
                re.IGNORECASE,
            )

            content = ""

            if content_match:
                content = content_match.group(1)


            actions.append(
                {
                    "tool": "write_file",
                    "parameters": {
                        "path": file_path,
                        "content": content,
                        "overwrite": False,
                    },
                }
            )


        # ---------------------------------------------------------
        # Edit existing file
        #
        # Examples:
        #   Edit app/main.py
        #   Modify README.md
        # ---------------------------------------------------------

        if (
            "edit" in request_lower
            or "modify" in request_lower
            or "update" in request_lower
        ):

            path_match = re.search(
                r"(?:edit|modify|update)\s+(?:file\s+)?([^\s]+)",
                request,
                re.IGNORECASE,
            )

            file_path = ""

            if path_match:
                file_path = path_match.group(1)


            actions.append(
                {
                    "tool": "edit_file",
                    "parameters": {
                        "path": file_path,
                        "old_text": "",
                        "new_text": "",
                    },
                }
            )


        # ---------------------------------------------------------
        # Delete file
        #
        # Examples:
        #   Delete test/amr.py
        #   Remove old.py
        # ---------------------------------------------------------

        if (
            "delete" in request_lower
            or "remove" in request_lower
        ):

            path_match = re.search(
                r"(?:delete|remove)\s+(?:file\s+)?([^\s]+)",
                request_clean,
                re.IGNORECASE,
            )

            file_path = ""

            if path_match:
                file_path = path_match.group(1).rstrip(").,")


            actions.append(
                {
                    "tool": "delete_file",
                    "parameters": {
                        "path": file_path,
                    },
                }
            )


        # ---------------------------------------------------------
        # Search project contents
        #
        # Examples:
        #   Search for UserService
        #   Find authentication
        # ---------------------------------------------------------

        if (
            "search" in request_lower
            or "find" in request_lower
        ):

            query_match = re.search(
                r"(?:search|find)\s+(?:for\s+)?(.+)",
                request,
                re.IGNORECASE,
            )

            query = ""

            if query_match:
                query = query_match.group(1)


            actions.append(
                {
                    "tool": "search_text",
                    "parameters": {
                        "query": query,
                    },
                }
            )


        # ---------------------------------------------------------
        # List project files
        #
        # Examples:
        #   List files
        #   Show project files
        # ---------------------------------------------------------

        if (
            "list files" in request_lower
            or "show files" in request_lower
            or "project files" in request_lower
        ):

            actions.append(
                {
                    "tool": "list_files",
                    "parameters": {},
                }
            )

        actions = [
            action
            for action in actions
            if not (
                (
                    "delete" in request_lower
                    or "remove" in request_lower
                )
                and action["tool"] == "write_file"
            )
        ]

        return {
            "goal": request,
            "actions": actions,
        }