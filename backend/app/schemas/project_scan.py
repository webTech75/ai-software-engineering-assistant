from pydantic import BaseModel


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
    directories: list[str]
    files: list[str]


# class PackageResponse(BaseModel):
#     name: str
#     version: str | None = None


# class LanguageDependencyResponse(BaseModel):
#     manager: str
#     packages: list[PackageResponse]


# class DependencyResponse(BaseModel):
#     python: LanguageDependencyResponse | None = None
#     javascript: LanguageDependencyResponse | None = None


class ProjectScanResponse(BaseModel):
    statistics: StatisticsResponse
    technology: TechnologyResponse
    structure: StructureResponse
    # dependencies: DependencyResponse