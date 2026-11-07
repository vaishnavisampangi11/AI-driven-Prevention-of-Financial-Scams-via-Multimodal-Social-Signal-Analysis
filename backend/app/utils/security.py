import os
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/bmp"}
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_upload_file(file: UploadFile, upload_dir: str):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded.")

    filename = file.filename or ""
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type.")

    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported MIME type.")

    target_dir = Path(upload_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(filename).name
    target_path = target_dir / safe_name
    return target_path


def validate_file_size(size: int):
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Uploaded file exceeds the 5MB limit.")
