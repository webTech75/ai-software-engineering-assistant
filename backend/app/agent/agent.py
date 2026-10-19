"""
===============================================================================
File:
    app/agent/agent.py

Description:
    Main AI agent orchestrator.

Responsibilities:
    - Coordinate planner workflow.
    - Execute project tools when required.
    - Build LLM context.
    - Generate final responses.

Does NOT:
    - Access files directly.
    - Execute tools directly.
    - Manage database sessions.

Author:
    Amr Elhabbal
===============================================================================
"""

import logging

from app.core.config import settings


logger = logging.getLogger(__name__)


class Agent:
    """
    Main AI assistant orchestrator.

    Flow:

        User Message
              |
              v
           Planner
              |
              v
     General or Project?
              |
        +-----+------+
        |            |
     General      Project
        |            |
        |         Executor
        |            |
        +-----+------+
              |
              v
             LLM
              |
              v
       Response Builder
    """

    def __init__(
        self,
        planner,
        executor,
        response_builder,
        llm,
    ):
        self.planner = planner
        self.executor = executor
        self.response_builder = response_builder
        self.llm = llm


    def run(
        self,
        message: str,
        project_directory: str | None = None,
        history: list[dict] | None = None,
    ) -> str:

        # ---------------------------------------------------------
        # Create execution plan
        # ---------------------------------------------------------

        plan = self.planner.create_plan(
            message
        )


        if plan is None:
            plan = {
                "goal": message,
                "task_type": "general",
                "actions": [],
            }


        logger.info(
            "Execution plan: %s",
            plan,
        )


        # ---------------------------------------------------------
        # Execute tools only for project tasks
        # ---------------------------------------------------------

        execution_results = []


        if (
            plan.get("task_type")
            in [
                "project",
                "review",
                "search",
                "write",
                "edit",
                "delete",
                "explain",
                "bug_analysis",
                "security_review",
                "quality_review",
            ]
            and project_directory
        ):

            execution_results = self.executor.execute(
                plan,
                project_directory,
            )


        logger.info(
            "Tool results: %s",
            execution_results,
        )


        # ---------------------------------------------------------
        # Build conversation history
        # ---------------------------------------------------------

        conversation = ""


        if history:

            for item in history[-6:]:

                conversation += (
                    f"{item['role']}: "
                    f"{item['content'][:500]}\n"
                )


        # ---------------------------------------------------------
        # Token selection
        # ---------------------------------------------------------

        task_type = plan.get(
            "task_type",
            "general",
        )


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


            Tool results:

            {execution_results}
            """,
                max_tokens=max_tokens,
        )


        # ---------------------------------------------------------
        # Build response
        # ---------------------------------------------------------

        return self.response_builder.build(
            execution_results,
            llm_answer,
        )


    def get_max_tokens(
        self,
        task_type: str,
    ) -> int:

        if task_type == "explain":

            return settings.llm_explain_max_tokens


        if task_type in [
            "review",
            "bug_analysis",
            "security_review",
            "quality_review",
        ]:

            return settings.llm_review_max_tokens


        return settings.llm_max_tokens