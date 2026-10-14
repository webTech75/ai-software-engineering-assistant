"""
===============================================================================
File: agent.py
Path: app/agent/agent.py

Description:
    Main AI agent orchestrator.

Responsibilities:
    - Coordinate the agent workflow.
    - Create execution plans.
    - Execute tools.
    - Build final responses.

Does NOT:
    - Access files directly.
    - Execute tools directly.
    - Manage database sessions.

Author:
    Amr Elhabbal
===============================================================================
"""

import logging


logger = logging.getLogger(__name__)


class Agent:

    def __init__(
        self,
        planner,
        executor,
        response_builder,
        llm,
    ):
        """
        Initialize agent components.
        """

        self.planner = planner
        self.executor = executor
        self.response_builder = response_builder
        self.llm = llm

    def run(
        self,
        project_directory,
        message: str,
        history: list[dict] | None = None,
    ) -> str:
        """
        Execute the agent workflow.

        The project directory is only passed
        to tools that require filesystem access.
        """

        # ---------------------------------------------------------
        # Create execution plan
        # ---------------------------------------------------------

        plan = self.planner.create_plan(
            message,
            "",
        )

        if plan is None:
            plan = {
                "goal": message,
                "actions": [],
            }

        logger.info("Execution plan: %s", plan)

        # ---------------------------------------------------------
        # Execute tools
        # ---------------------------------------------------------

        execution_results = self.executor.execute(
            plan,
            project_directory,
        )

        logger.info(
            "Execution results: %s",
            execution_results,
        )

        # ---------------------------------------------------------
        # Build conversation context
        # ---------------------------------------------------------

        conversation = ""

        if history:
            for item in history[-6:]:
                conversation += (
                    f"{item['role']}: "
                    f"{item['content'][:300]}\n"
                )

        # ---------------------------------------------------------
        # Generate LLM response
        # ---------------------------------------------------------

        llm_answer = self.llm.generate(
            f"""
                You are a software engineering assistant.

                Conversation:
                {conversation}

                User request:
                {message}

                Tool results:
                {execution_results}

                Answer the user using the tool results when available.
                If no tool results are available, answer using your software engineering knowledge.
            """
        )

        # ---------------------------------------------------------
        # Build final response
        # ---------------------------------------------------------

        response = self.response_builder.build(
            execution_results,
            llm_answer,
        )

        return response