"""
===============================================================================
File: base.py
Path: app/agent/tools/base.py

Description:
    Defines the abstract base class for every AI tool.

Responsibilities:
    - Define the interface every tool must implement.
    - Ensure consistency across all tools.
    - Provide tool metadata for the LLM.
    - Standardize tool execution.

Architecture:

                BaseTool
                   ▲
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ReadFile   WriteFile   DeleteFile
        ▲          ▲          ▲
        └──────────┼──────────┘
                   ▼
              Tool Registry
                   ▼
              Agent Service

Every tool must provide:

    • name
        Unique tool identifier.

    • description
        Natural language description shown to the LLM.

    • schema
        JSON schema defining the tool parameters.

    • execute()
        Business logic executed by the application.

Execution Flow

        LLM
         │
         ▼
   Tool Registry
         │
         ▼
    BaseTool API
         │
         ▼
 Specific Tool
         │
         ▼
 Project Filesystem

Dependencies:
    - abc
    - Project model

Author:
    Amr Elhabbal
===============================================================================
"""

from abc import ABC, abstractmethod

from app.models.project import Project


class BaseTool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def schema(self) -> dict:
        pass

    @abstractmethod
    def execute(self, project: Project):
        pass