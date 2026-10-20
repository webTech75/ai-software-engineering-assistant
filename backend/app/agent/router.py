"""
===============================================================================
File:
    app/agent/router.py

Description:
    Fast request classification before using LLM or project tools.

Responsibilities:
    - Decide whether a request is general.
    - Decide whether project context is required.
    - Decide whether request performs a project action.

Does NOT:
    - Call LLM.
    - Execute tools.
    - Read files.
    - Extract filenames.
    - Create execution plans.

Architecture:

    User Request
          |
          v
       Router
          |
    +-----+------+
    |            |
General      Project
                 |
                 v
              Planner

===============================================================================
"""

from enum import Enum



class RequestType(str, Enum):
    """
    High-level request categories.
    """

    GENERAL = "general"

    PROJECT = "project"

    ACTION = "action"




class AgentRouter:
    """
    Determines the user's request category.

    Router performs only fast classification.

    Detailed intent detection belongs to Planner.
    """



    PROJECT_KEYWORDS = [

        "project",

        "file",

        "folder",

        "directory",

        "code",

        "class",

        "function",

        "review",

        "analyze",

        "inspect",

        "architecture",

        "implementation",

        "bug",

        "error",

        "security",

        "quality",

        "refactor",

        "search",

        "find",

        "read",

        "open",

        "show",

        "view",

        ".py",

        ".js",

        ".ts",

        ".tsx",

        ".jsx",

        ".md",

        ".json",

        ".yaml",

        ".yml",

    ]



    ACTION_KEYWORDS = [

        "create",

        "write",

        "generate",

        "update",

        "modify",

        "change",

        "edit",

        "delete",

        "remove",

        "rename",

    ]



    def route(
        self,
        message: str,
    ) -> RequestType:
        """
        Determine request category.

        Priority:

            ACTION
              |
            PROJECT
              |
            GENERAL
        """


        text = message.lower()



        # ---------------------------------------------------------
        # File modification requests
        # ---------------------------------------------------------

        if any(
            keyword in text
            for keyword in self.ACTION_KEYWORDS
        ):

            return RequestType.ACTION



        # ---------------------------------------------------------
        # Project analysis requests
        # ---------------------------------------------------------

        if any(
            keyword in text
            for keyword in self.PROJECT_KEYWORDS
        ):

            return RequestType.PROJECT



        # ---------------------------------------------------------
        # Normal conversation
        # ---------------------------------------------------------

        return RequestType.GENERAL