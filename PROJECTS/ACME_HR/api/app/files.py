import re
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

STORAGE_DIR = Path(__file__).resolve().parents[1] / "storage"
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
STORED_NAME = re.compile(r"^[a-f0-9]{32}(?:\.[A-Za-z0-9]{1,10})?$")


def save_upload(upload: UploadFile) -> tuple[str, str]:
    original = Path(upload.filename or "").name
    if original in {"", ".", ".."}:
        raise HTTPException(status_code=422, detail="A file name is required.")
    payload = upload.file.read(MAX_UPLOAD_BYTES + 1)
    if not payload:
        raise HTTPException(status_code=422, detail="The file is empty.")
    if len(payload) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="The file is larger than 10 MB.")
    suffix = Path(original).suffix.lower()
    if not re.fullmatch(r"\.[A-Za-z0-9]{1,10}", suffix or ""):
        suffix = ""
    stored = f"{uuid.uuid4().hex}{suffix}"
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    (STORAGE_DIR / stored).write_bytes(payload)
    return stored, original


def stored_path(stored_name: str) -> Path:
    if not STORED_NAME.fullmatch(stored_name):
        raise HTTPException(status_code=404, detail="File not found.")
    path = STORAGE_DIR / stored_name
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")
    return path


def delete_stored(stored_name: str | None) -> None:
    if not stored_name or not STORED_NAME.fullmatch(stored_name):
        return
    path = STORAGE_DIR / stored_name
    if path.is_file():
        path.unlink()
