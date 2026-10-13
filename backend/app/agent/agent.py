"""
===============================================================================
File: agent.py
Path: app/agent/agent.py

Description:
    Main AI agent orchestrator.

Responsibilities:
    - Coordinate the agent workflow.
    - Build project context.
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
    """
    Main AI software engineering agent.

    Coordinates:

        Project
          |
          v
        ContextBuilder
          |
          v
        Planner
          |
          v
        Executor
          |
          v
        ResponseBuilder

    """


    def __init__(
        self,
        planner,
        executor,
        context_builder,
        response_builder,
    ):
        """
        Initialize agent components.
        """

        self.planner = planner

        self.executor = executor

        self.context_builder = context_builder

        self.response_builder = response_builder



    def run(
        self,
        project,
        message: str,
    ) -> str:
        """
        Execute one AI request.

        Parameters:

            project:
                SQLAlchemy Project object.

                Contains:

                    project.id
                    project.name
                    project.description
                    project.project_directory


            message:
                User request.

        """


        # ---------------------------------------------------------
        # Step 1:
        # Build project knowledge context.
        #
        # Example:
        #
        # {
        #     "files_count": 50,
        #     "symbols_count": 200
        # }
        #
        # This comes from the database.
        # ---------------------------------------------------------

        context = self.context_builder.build(
            project
        )


        logger.info(
            "Project context built for %s",
            project.name,
        )



        # ---------------------------------------------------------
        # Step 2:
        # Convert user message into actions.
        #
        # Example:
        #
        # User:
        #   "show files"
        #
        # Planner:
        #
        # {
        #    "actions": [
        #        {
        #           "tool": "list_files"
        #        }
        #    ]
        # }
        #
        # ---------------------------------------------------------

        plan = self.planner.create_plan(
            message
        )


        logger.info(
            "Execution plan created: %s",
            plan,
        )



        # ---------------------------------------------------------
        # Step 3:
        # Execute the selected tools.
        #
        # IMPORTANT:
        #
        # We pass Project.
        #
        # Executor will extract:
        #
        # project.project_directory
        #
        # when filesystem access is required.
        #
        # ---------------------------------------------------------

        execution_results = self.executor.execute(
            plan,
            project,
        )



        logger.info(
            "Tool execution completed"
        )



        # ---------------------------------------------------------
        # Step 4:
        # Create final assistant response.
        #
        # ResponseBuilder combines:
        #
        # - project context
        # - tool results
        #
        # into user-friendly output.
        #
        # ---------------------------------------------------------

        response = self.response_builder.build(
            context,
            execution_results,
        )


        return response