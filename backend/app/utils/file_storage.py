from pathlib import Path
from fastapi import UploadFile
import shutil
import zipfile
import os

# backend/uploads
UPLOAD_DIR = Path("uploads")

# ensures the uploads folder always exists.
UPLOAD_DIR.mkdir(exist_ok=True)


def get_project_directory(project_id: int) -> Path:
    """
    Returns the directory where a project's files are stored.
    """
    project_dir = UPLOAD_DIR / f"project_{project_id}"
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def save_uploaded_file(project_id: int, file: UploadFile) -> str:
    """
    Save an uploaded file inside the project's directory.
    """

    project_dir = get_project_directory(project_id)

    file_path = project_dir / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)


def extract_zip(project_id: int, zip_path: str) -> str:
    project_dir = get_project_directory(project_id)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        safe_extract_zip(zip_ref, project_dir)

    os.remove(zip_path)

    return str(project_dir)


def safe_extract_zip(zip_ref, destination: Path):
    """
    Safely extract a ZIP archive, preventing ZIP Slip attacks.
    """

    destination = destination.resolve()

    for member in zip_ref.infolist():
        member_path = (destination / member.filename).resolve()

        if not str(member_path).startswith(str(destination)):
            raise ValueError(
                f"Unsafe ZIP entry detected: {member.filename}"
            )

        zip_ref.extract(member, destination)