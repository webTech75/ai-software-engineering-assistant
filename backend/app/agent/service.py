"""
===============================================================================
File: service.py
Path: app/agent/service.py

Description:
    Service layer responsible for connecting the API layer
    with the AI Agent.

Responsibilities:
    - Receive project requests from the API.
    - Pass the database Project object to the agent.
    - Initialize agent components.

Important:
    The Project object is the source of truth.

    The filesystem path:
        project.project_directory

    is only used by tools that access files.

Author:
    Amr Elhabbal
===============================================================================
"""

import logging

from sqlalchemy.orm import Session

from app.agent.agent import Agent
from app.agent.planner import Planner
from app.agent.executor import Executor
from app.agent.context_builder import ContextBuilder
from app.agent.response_builder import ResponseBuilder


logger = logging.getLogger(__name__)


class AgentService:
    """
    Application service responsible for running
    the AI software engineering agent.
    """


    def __init__(
        self,
        db: Session,
    ):
        """
        Initialize the agent pipeline.

        The agent needs:
            - Planner
            - Executor
            - Context Builder
            - Response Builder
        """

        self.agent = Agent(

            # Creates the execution plan
            planner=Planner(),


            # Executes tools from the plan
            executor=Executor(),


            # Loads project information from database
            #
            # Receives a DB session because it needs:
            #   - ProjectFile
            #   - ProjectSymbol
            #
            context_builder=ContextBuilder(db),


            # Converts execution results
            # into the final assistant response
            response_builder=ResponseBuilder(),
        )



    def ask(
        self,
        project,
        message: str,
    ) -> str:
        """
        Send a request to the AI agent.

        IMPORTANT:

        We pass the whole Project object.

        because the agent needs database information:

            project.id
            project.name
            project.description
            project.project_directory

        """

        return self.agent.run(
            project,
            message,
        )