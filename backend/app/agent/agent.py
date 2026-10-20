"""
===============================================================================
File:
    app/agent/agent.py

Description:
    Main AI agent orchestrator.

Responsibilities:
    - Route user requests.
    - Create execution plans.
    - Execute project tools when required.
    - Build LLM context.
    - Generate final responses.

Does NOT:
    - Access files directly.
    - Execute tools directly.
    - Manage database sessions.
    - Decide individual tool workflows.

Architecture:

    User Message
          |
          v
       Router
          |
    +-----+------+
    |            |
 General      Project
    |            |
    |         Planner
    |            |
    |         Executor
    |            |
    +-----+------+
          |
          v
         LLM
          |
          v
      Response

Author:
    Amr Elhabbal
===============================================================================
"""

import logging

from app.core.config import settings

from app.agent.router import (
    AgentRouter,
    RequestType,
)

from app.agent.planner import Planner
from app.agent.executor import Executor


logger = logging.getLogger(__name__)


class Agent:
    """
    Main AI assistant orchestrator.

    Coordinates:

        Router
        Planner
        Executor
        LLM

    The Agent does not decide
    individual tool workflows.
    """

    def __init__(
        self,
        llm,
        planner: Planner | None = None,
        executor: Executor | None = None,
    ):
        """
        Initialize agent.
        """

        self.router = AgentRouter()

        self.planner = (
            planner
            or Planner()
        )

        self.executor = (
            executor
            or Executor()
        )

        self.llm = llm


    def run(
        self,
        message: str,
        project_directory: str | None = None,
        history: list[dict] | None = None,
    ) -> str:
        """
        Execute user request.

        Flow:

            Message
              |
            Router
              |
            Planner
              |
            Executor
              |
             LLM
        """

        # ---------------------------------------------------------
        # Route request
        # ---------------------------------------------------------

        request_type = self.router.route(
            message
        )


        logger.info(
            "Request route: %s",
            request_type,
        )


        # ---------------------------------------------------------
        # Default values
        # ---------------------------------------------------------

        tool_results = {}

        task_type = request_type.value



        # ---------------------------------------------------------
        # Create plan and execute tools
        # ---------------------------------------------------------

        if (
            project_directory
            and request_type != RequestType.GENERAL
        ):

            plan = self.planner.create_plan(
                message
            )


            logger.info(
                "Execution plan: %s",
                plan,
            )


            task_type = plan.get(
                "task_type",
                task_type,
            )


            tool_results = self.executor.execute(
                plan,
                project_directory,
            )



        # ---------------------------------------------------------
        # Build conversation history
        # ---------------------------------------------------------

        conversation = (
            self.build_conversation_context(
                history
            )
        )



        # ---------------------------------------------------------
        # Token selection
        # ---------------------------------------------------------

        max_tokens = self.get_max_tokens(
            task_type
        )



        # ---------------------------------------------------------
        # Ask LLM
        # ---------------------------------------------------------

        llm_answer = self.llm.generate(
            prompt=f"""
Conversation:

{conversation}


User request:

{message}


Project tool results:

{tool_results}
""",
            max_tokens=max_tokens,
        )



        if not llm_answer or not llm_answer.strip():

            llm_answer = (
                "I was unable to generate a response. "
                "Please try again."
            )


        logger.info(
            "LLM response generated"
        )


        return llm_answer



    def build_conversation_context(
        self,
        history: list[dict] | None,
    ) -> str:
        """
        Build conversation context for LLM.

        Limits history size to prevent
        unnecessary token usage.
        """

        if not history:

            return ""


        conversation = ""


        for item in history[-6:]:

            conversation += (
                f"{item['role']}: "
                f"{item['content'][:500]}\n"
            )


        return conversation



    def get_max_tokens(
        self,
        task_type: str,
    ) -> int:
        """
        Select token limit based on task.
        """

        if task_type == "explain":

            return (
                settings.llm_explain_max_tokens
            )


        if task_type in [
            "review",
            "bug_analysis",
            "security_review",
            "quality_review",
        ]:

            return (
                settings.llm_review_max_tokens
            )


        return settings.llm_max_tokens