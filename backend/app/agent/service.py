"""
===============================================================================
File: service.py
Path: app/agent/service.py

Description:
    Service layer responsible for connecting the API layer
    with the AI Agent.

Responsibilities:
    - Receive project requests from the API.
    - Pass the Project object to the agent.
    - Initialize agent components.

Important:
    The filesystem path:

        project.project_directory

    is only used by tools that require filesystem access.

Author:
    Amr Elhabbal
===============================================================================
"""

import logging

from app.agent.agent import Agent
from app.agent.planner import Planner
from app.agent.executor import Executor
from app.agent.response_builder import ResponseBuilder
from app.ai.llm.client import LLMClient


logger = logging.getLogger(__name__)


class AgentService:
    """
    Application service responsible for running
    the AI software engineering agent.
    """


    def __init__(self):
        """
        Initialize the agent pipeline.

        The agent needs:

            - Planner
            - Executor
            - Response Builder
            - LLM Client
        """

        self.agent = Agent(

            # Creates the execution plan
            planner=Planner(),


            # Executes tools from the plan
            executor=Executor(),


            # Converts execution results
            # into the final assistant response
            response_builder=ResponseBuilder(),


            # Generates final AI responses
            llm=LLMClient(),
        )



    def ask(
        self,
        project,
        message: str,
    ) -> str:
        """
        Send a request to the AI agent.

        The Project object is passed only because
        tools may need:

            project.project_directory

        The agent does not load project files
        or project index data here.
        """

        return self.agent.run(
            project.project_directory,
            message,
        )