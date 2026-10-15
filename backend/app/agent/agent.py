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

from app.core.config import settings


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

        Workflow:

            User message
                  |
                  v
              Planner
                  |
                  v
              Executor
                  |
                  v
             LLM response
                  |
                  v
          Response builder
        """



        # ---------------------------------------------------------
        # Create execution plan
        # ---------------------------------------------------------

        plan = self.planner.create_plan(
            message,
        )

        print("================ PLAN ================")
        print(plan)
        print("======================================")


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
        # Execute tools
        #
        # General questions return no actions.
        #
        # Executor should simply return empty results.
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
        # Select token limit
        # ---------------------------------------------------------

        task_type = plan.get(
            "task_type",
            "general",
        )


        max_tokens = self.get_max_tokens(
            task_type
        )


        logger.info(
            "LLM task type: %s | max_tokens: %s",
            task_type,
            max_tokens,
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

            If no tool results are available,
            answer normally using your software engineering knowledge.
            """,

            max_tokens=max_tokens,
        )



        # ---------------------------------------------------------
        # Build final response
        # ---------------------------------------------------------

        response = self.response_builder.build(
            execution_results,
            llm_answer,
        )


        return response



    def get_max_tokens(
        self,
        task_type: str,
    ) -> int:
        """
        Select LLM token limit based on task type.

        Values come from environment variables
        through application settings.

        No hardcoded token numbers here.
        """



        # ---------------------------------------------------------
        # Explanation tasks
        #
        # Example:
        #
        #   explain project_service.py
        #
        # ---------------------------------------------------------

        if task_type == "explain":

            return settings.llm_explain_max_tokens



        # ---------------------------------------------------------
        # Review tasks
        #
        # Example:
        #
        #   find bugs in auth.py
        #
        # ---------------------------------------------------------

        if task_type in [

            "review",

            "bug_analysis",

            "security_review",

            "quality_review",

        ]:

            return settings.llm_review_max_tokens



        # ---------------------------------------------------------
        # Default
        #
        # General questions:
        #
        #   what is FastAPI?
        #
        # ---------------------------------------------------------

        return settings.llm_max_tokens
    
