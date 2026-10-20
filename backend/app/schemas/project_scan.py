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
    language: str | None = None
    framework: str | None = None
    database: str | None = None
    orm: str | None = None
    migration_tool: str | None = None


class StructureResponse(BaseModel):
    files: list[str]


class ProjectScanResponse(BaseModel):
    statistics: StatisticsResponse
    technology: TechnologyResponse
    structure: StructureResponse
    dependencies: dict[str, Any] = {}
    api: dict[str, Any] = {}
    database: dict[str, Any] = {}
    metrics: dict[str, Any] = {}
    complexity: dict[str, Any] = {}