# Отвечает за чтение файлов из файловой системы.

from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".json", ".bin", ".jpeg", ""} #поддерживаемые форматы файлов

#функция получает на вход путь к входной директории и выдает содержимое внутри нее
def list_input_files(input_dir: Path) -> list[Path]:
    return [path for path in input_dir.iterdir() if path.is_file()] #проходимся по содержимому папки и оставляем только обычные файлы

def read_file(path: Path)->str: #функция читает один файл и возвращает его текст
    # Открываем файл в UTF-8.
    # errors="replace" нужен, чтобы не упасть на странных символах:
    # если байт не читается, он будет заменен специальным символом.
    return path.read_text(encoding="utf-8", errors="replace")


