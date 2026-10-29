"""
Core AI agent orchestrator managing tools, context, and LLM responses.

Author: Amr Elhabbal | Powered by Meta AI Muse
"""

import logging

from app.agent.tool_registry import ToolRegistry
from app.analysis.storage import AnalysisStorage

logger = logging.getLogger(__name__)

NEURA_WELCOME_MESSAGE = """
            👋 Hi, I'm Neura, your AI Software Engineering Assistant, 
            powered by Meta AI's Muse Spark 1.3 model.

            I can help you understand your codebase, debug issues, 
            review architecture, explain concepts, and improve your software projects.
            """


class Agent:
    """
    Main AI assistant orchestrator.

    Coordinates:

        Tool Registry
        LLM

    The Agent does not perform
    individual tool operations.

    It only:
        - selects required tools
        - provides tool results to the LLM
        - returns the final response
    """

    def __init__(self, llm):
        """
        Initialize agent.
        """

        self.llm = llm
        self.tool_registry = ToolRegistry()

    def run(
        self,
        message: str,
        project_directory: str | None = None,
        history: list[dict] | None = None,
    ) -> str:

        # ---------------------------------------------------------
        # Execute required tools
        # ---------------------------------------------------------
        tool_results = {}

        project_context = None

        if project_directory:
            stored_analysis = AnalysisStorage.load(project_directory)
            project_context = stored_analysis.get("context")

        # Listing project files
        if project_directory and self.should_list_files(message):

            logger.info("Listing project files")

            list_tool = self.tool_registry.get("list_files")

            if list_tool:

                tool_results = list_tool.execute(
                    project_directory=project_directory,
                )
        # search route
        elif project_directory and self.should_search_text(message):

            logger.info("Searching project files")

            search_tool = self.tool_registry.get("search_text")

            if search_tool:

                tool_results = search_tool.execute(
                    project_directory=project_directory,
                    query=self.extract_search_query(message),
                )

        #  read file
        elif project_directory and self.should_read_file(message):

            logger.info("Reading project file")

            file_name = self.extract_file_name(message)

            logger.info(
                "Requested file: %s",
                file_name,
            )

            read_tool = self.tool_registry.get("read_file")

            if read_tool:

                tool_results = read_tool.execute(
                    project_directory=project_directory,
                    path=file_name,
                )

                from pprint import pformat

                logger.info(
                    "File content:\n%s",
                    pformat(tool_results, width=120),
                )

        elif project_directory and self.should_search_project(message):

            logger.info("Running project search tool")

            search_tool = self.tool_registry.get("search_text")

            if search_tool:

                tool_results = search_tool.execute(
                    project_directory=project_directory,
                    query=self.extract_search_query(message),
                )

        #  analyze project
        elif project_directory and self.should_analyze_project(message):

            logger.info("Running project analysis tool")

            analyze_tool = self.tool_registry.get("analyze_project")

            tool_results = analyze_tool.execute(
                project_directory=project_directory,
            )

            from pprint import pformat

            logger.info(
                "Tool results:\n%s",
                pformat(tool_results, width=120),
            )

        # ---------------------------------------------------------
        # Build conversation history
        # ---------------------------------------------------------

        conversation = self.build_conversation_context(history)

        # ---------------------------------------------------------
        # Generate LLM response
        # ---------------------------------------------------------

        llm_answer = self.llm.generate(prompt=f"""
            Conversation:

            {conversation}


            User request:

            {message}


            Project information:

            Project uploaded: {bool(project_directory)}

            Project context:

            {project_context}

            Tool results:

            {tool_results}
            """)

        if not llm_answer or not llm_answer.strip():

            llm_answer = "I was unable to generate a response. " "Please try again."

        logger.info("LLM response generated")

        return llm_answer

    def should_analyze_project(
        self,
        message: str,
    ) -> bool:
        """
        Determine whether project analysis
        is required.

        Temporary lightweight routing.

        Future:
            Replace with LLM based
            tool selection.
        """

        keywords = [
            "review",
            "analyze",
            "analysis",
            "scan",
            "project",
            "code review",
            "architecture",
            "bugs",
            "security",
        ]

        message = message.lower()

        return any(keyword in message for keyword in keywords)

    def build_conversation_context(
        self,
        history: list[dict] | None,
    ) -> str:
        """
        Build conversation context.

        Limits history size to reduce
        unnecessary token usage.
        """

        if not history:
            return NEURA_WELCOME_MESSAGE

        conversation = ""

        for item in history[-6:]:
            conversation += f"{item['role']}: " f"{item['content'][:500]}\n"

        return conversation

    def should_read_file(
        self,
        message: str,
    ) -> bool:
        """
        Determine whether the user is requesting
        inspection of a specific file.
        """

        message = message.lower()

        file_reference = ".py" in message or ".tsx" in message or ".ts" in message

        action_request = any(
            keyword in message
            for keyword in [
                "read",
                "open",
                "show",
                "explain",
                "review",
                "inspect",
                "analyze",
                "check",
            ]
        )

        return file_reference and action_request

    def extract_file_name(self, message: str) -> str:
        """
        Extract file path from user message.

        Example:
        "Review app/services/user_service.py"

        returns:
        "app/services/user_service.py"
        """

        words = message.split()

        for word in words:
            if "/" in word and "." in word:
                return word.strip("`'\"")

        return ""

    def should_list_files(
        self,
        message: str,
    ) -> bool:
        """
        Determine whether the user wants
        to inspect project files.
        """

        keywords = [
            "list files",
            "show files",
            "file list",
            "folder",
            "directory",
            "structure",
            "tree",
        ]

        message = message.lower()

        return any(keyword in message for keyword in keywords)

    def should_search_text(
        self,
        message: str,
    ) -> bool:
        """
        Determine whether user wants
        to search project contents.
        """

        keywords = [
            "find",
            "search",
            "where is",
            "contains",
            "usage of",
            "references",
        ]

        message = message.lower()

        return any(keyword in message for keyword in keywords)

    def extract_search_query(
        self,
        message: str,
    ) -> str:

        ignored = {
            "search",
            "for",
            "find",
            "where",
            "locate",
        }

        words = message.split()

        return " ".join(word for word in words if word.lower() not in ignored)

    def should_search_project(
        self,
        message: str,
    ) -> bool:

        keywords = [
            "search",
            "find",
            "where",
            "locate",
        ]

        message = message.lower()

        return any(keyword in message for keyword in keywords)

    def get_project_welcome(
        self,
        project_name: str,
        context: str | None = None,
    ) -> dict:

        return {"message": f"""
            👋 Hi, I'm Neura, your AI Software Engineering Assistant, 
            powered by Meta AI's Muse Spark 1.3 model to analyze, 
            understand, and assist with your software projects.

            Here's what I can help you with:
            
            I analyzed your project: {project_name}

            {context}

            You can ask me anything about your codebase.
        """}
