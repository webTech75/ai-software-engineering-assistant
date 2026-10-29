"""
===============================================================================
File:
    app/utils/file_storage.py

Description:
    Handles project upload, extraction, and storage operations.

Responsibilities:
    - Save and validate uploaded project files.
    - Safely extract ZIP archives.
    - Manage project storage directories.
    - Remove temporary and ignored files.

Notes:
    - Does not analyze files or communicate with AI.

Author:
    Amr Elhabbal
===============================================================================
"""

from pathlib import Path
import shutil
import zipfile

from fastapi import UploadFile

from app.file_system.file_policy import (
    MAX_EXTRACTED_SIZE,
    MAX_FILES_IN_ZIP,
    is_zip_size_allowed,
    should_ignore_path,
)

UPLOAD_DIR = Path("uploads")

ALLOWED_UPLOAD_EXTENSIONS = {
    ".zip",
}


UPLOAD_DIR.mkdir(
    exist_ok=True,
)


# ============================================================================
# Directory helpers
# ============================================================================


def get_project_directory(project_id: int) -> Path:
    """
    Return project storage directory.
    """

    directory = UPLOAD_DIR / f"project_{project_id}"

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def get_source_directory(project_id: int) -> Path:
    """
    Return project source directory.
    """

    source = get_project_directory(project_id) / "source"

    source.mkdir(
        parents=True,
        exist_ok=True,
    )

    return source


def get_existing_project_directory(project_id: int) -> Path:
    """
    Return existing project directory without creating it.
    """

    return UPLOAD_DIR / f"project_{project_id}"


# ============================================================================
# Upload handling
# ============================================================================


def validate_upload(file: UploadFile) -> None:
    """
    Validate uploaded file type.
    """

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_UPLOAD_EXTENSIONS:
        raise ValueError("Only ZIP files are supported.")


def save_uploaded_file(
    project_id: int,
    file: UploadFile,
) -> str:
    """
    Save uploaded ZIP file temporarily.
    """

    validate_upload(file)

    project_dir = get_project_directory(project_id)

    safe_name = Path(file.filename).name

    file_path = project_dir / safe_name

    file.file.seek(0, 2)

    size = file.file.tell()

    file.file.seek(0)

    if not is_zip_size_allowed(size):
        raise ValueError("Upload exceeds maximum size limit.")

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return str(file_path)


# ============================================================================
# ZIP extraction
# ============================================================================


def extract_zip(
    project_id: int,
    zip_path: str,
) -> str:
    """
    Extract ZIP into clean source directory.
    """

    print("EXTRACTING ZIP:", zip_path)

    source_dir = get_source_directory(project_id)

    if source_dir.exists():
        shutil.rmtree(source_dir)

    source_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    with zipfile.ZipFile(zip_path, "r") as zip_file:

        validate_zip_contents(zip_file)

        safe_extract_zip(
            zip_file,
            source_dir,
        )

    Path(zip_path).unlink(
        missing_ok=True,
    )

    normalize_extracted_folder(source_dir)

    remove_ignored_paths(source_dir)

    return str(source_dir)


def validate_zip_contents(
    zip_file: zipfile.ZipFile,
) -> None:
    """
    Validate ZIP contents before extraction.
    """

    files = []

    extracted_size = 0

    for member in zip_file.infolist():

        member_path = Path(member.filename)

        if should_ignore_path(member_path):
            continue

        files.append(member)

        extracted_size += member.file_size

    if len(files) > MAX_FILES_IN_ZIP:
        raise ValueError(f"ZIP contains too many analyzable files ({len(files)}).")

    if extracted_size > MAX_EXTRACTED_SIZE:
        raise ValueError("Extracted ZIP size exceeds limit.")


def safe_extract_zip(
    zip_file: zipfile.ZipFile,
    destination: Path,
) -> None:
    """
    Prevent ZIP Slip attacks.
    """

    destination = destination.resolve()

    for member in zip_file.infolist():

        member_path = Path(member.filename)

        if should_ignore_path(member_path):
            continue

        target = (destination / member.filename).resolve()

        if destination not in target.parents:
            raise ValueError(f"Unsafe ZIP file: {member.filename}")

        zip_file.extract(
            member,
            destination,
        )


# ============================================================================
# Folder normalization
# ============================================================================


def normalize_extracted_folder(
    source_dir: Path,
) -> None:
    """
    Remove unnecessary root folder created by some ZIP tools.
    """

    children = list(source_dir.iterdir())

    if len(children) != 1:
        return

    folder = children[0]

    if not folder.is_dir():
        return

    for item in folder.iterdir():

        shutil.move(
            str(item),
            str(source_dir),
        )

    folder.rmdir()


def remove_ignored_paths(
    directory: Path,
) -> None:
    """
    Remove ignored files and directories after extraction.
    """

    if not directory.exists():
        return

    for path in sorted(
        directory.rglob("*"),
        key=lambda p: len(p.parts),
        reverse=True,
    ):

        relative_path = path.relative_to(directory)

        if should_ignore_path(relative_path):

            print(
                "REMOVING IGNORED PATH:",
                path,
            )

            if path.is_dir():
                shutil.rmtree(
                    path,
                    ignore_errors=True,
                )

            elif path.is_file():
                path.unlink(
                    missing_ok=True,
                )


# ============================================================================
# Cleanup
# ============================================================================


def delete_project_directory(
    project_directory: str,
) -> None:
    """
    Remove complete project storage.
    """

    path = Path(project_directory)

    if path.exists():
        shutil.rmtree(path)
