from pydantic import BaseModel
from typing import Any


class StatisticsResponse(BaseModel):
    total_files: int
    total_directories: int
    extensions: dict[str, int]
    total_size: int
    average_file_size: float
    largest_file: str | None = None
    largest_file_size: int


class TechnologyResponse(BaseModel):
    languages: list[str] = []
    frameworks: list[str] = []
    database: str | None = None
    orms: list[str] = []
    migration_tools: list[str] = []
    package_manager: str | None = None
    build_tools: list[str] = []
    testing_tools: list[str] = []
    styling_tools: list[str] = []


class StructureResponse(BaseModel):
    files: list[str]


class ProjectContext(BaseModel):
    technology: TechnologyResponse
    structure: StructureResponse
    dependencies: dict[str, Any] = {}
    api: dict[str, Any] = {}


class ProjectScanResponse(BaseModel):
    api: dict[str, Any] = {}
    technology: TechnologyResponse
    dependencies: dict[str, Any] = {}
    metrics: dict[str, Any] = {}
    complexity: dict[str, Any] = {}
    tests: dict[str, Any]
    statistics: StatisticsResponse
    structure: StructureResponse
    context: ProjectContext | None = None
