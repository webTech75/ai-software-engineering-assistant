from sqlalchemy.orm import Session

from app.agent.intelligence.file_indexer import FileIndexer
from app.models.project_file import ProjectFile


class FileIndexService:
    """
    Handles project file indexing and database synchronization.
    """

    def __init__(self, db: Session):
        self.db = db
        self.indexer = FileIndexer()


    def index_project(
        self,
        project_id: int,
        project_directory: str,
    ):
        print("INDEX ROOT>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>:", project_directory)
        files = self.indexer.index(project_directory)

        indexed_files = []

        for file in files:

            existing = (
                self.db.query(ProjectFile)
                .filter(
                    ProjectFile.project_id == project_id,
                    ProjectFile.path == file["path"],
                )
                .first()
            )

            if existing:
                continue

            project_file = ProjectFile(
                project_id=project_id,
                path=file["path"],
                language=file["language"],
                extension=file["extension"],
                size=file["size"],
            )

            self.db.add(project_file)

            indexed_files.append(project_file)

        self.db.commit()

        return indexed_files