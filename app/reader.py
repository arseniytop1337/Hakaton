from pathlib import Path
from app.exceptions import UnsupportedFileFormatError, EmptyEmailError

supported_extensions = {".txt", ""}
ignored_names = {".DS_Store"}


def list_input_files(input_dir: Path) -> list[Path]:
    return [
        path for path in sorted(input_dir.iterdir())
        if path.is_file() and path.name not in ignored_names
    ]


def is_supported_text_file(path: Path) -> bool:
    return path.suffix.lower() in supported_extensions


def read_file(path: Path) -> str:
    if not is_supported_text_file(path):
        raise UnsupportedFileFormatError(f"Unsupported file format: {path}")
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        raise EmptyEmailError(f"Empty file: {path}")
    return text
