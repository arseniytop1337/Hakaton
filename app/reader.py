# Отвечает за чтение файлов из файловой системы.

from pathlib import Path
from app.exceptions import UnsupportedFileFormatError, EmptyEmailError #не будем читать файлы-исключения

SUPPORTED_EXTENSIONS = {".txt", ""} #поддерживаемые форматы файлов
IGNORED_NAMES = {".DS_Store"}

#функция получает на вход путь к входной директории и выдает содержимое внутри нее
def list_input_files(input_dir: Path) -> list[Path]:

    # Возвращаем список файлов, собранный через list comprehension.
    return [

        # Берем очередной объект path из содержимого директории input_dir.
        path for path in sorted(input_dir.iterdir())

        # Оставляем только те объекты, которые:
        # 1. являются обычными файлами, а не папками
        # 2. имеют расширение, которое мы поддерживаем
        if path.is_file() and path.name not in IGNORED_NAMES #оставляем только те файлы что не находятся в игнорируемых
    ] #проходимся по содержимому папки и оставляем только обычные файлы

def is_supported_text_file(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_EXTENSIONS #возвращаем путь до файла если расширение файла подходит

def read_file(path: Path)->str: #функция читает один файл и возвращает его текст
    if not is_supported_text_file(path):
        raise UnsupportedFileFormatError(f"Unsupported file format: {path}") #вызываем класс из исключений
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        raise EmptyEmailError(f"Empty file: {path}") #если файл читается, однако он пуст, то тоже возвращаем ошибку

    # Открываем файл в UTF-8.
    # errors="replace" нужен, чтобы не упасть на странных символах:
    # если байт не читается, он будет заменен специальным символом.
    return text


