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
    review: dict[str, Any]
    quality: dict[str, Any]
    bugs: dict[str, Any]
    security: dict[str, Any]
    api: dict[str, Any] = {}
    technology: TechnologyResponse
    database: dict[str, Any] = {}
    dependencies: dict[str, Any] = {}
    metrics: dict[str, Any] = {}
    complexity: dict[str, Any] = {}
    tests: dict[str, Any]
    statistics: StatisticsResponse
    structure: StructureResponse