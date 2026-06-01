from pathlib import Path
from app.exceptions import EmptyEmailError, UnsupportedFileFormatError
from app.reader import list_input_files, read_file
from app.parser import parse_email
from app.classifier import classify_email
from app.models import Category
from app.organizer import create_run_output_directory, copy_email_to_category
from app.stats_reporter import generate_report, record_error, record_success
from app.logger import set_log_file


def main():
    input_dir = Path("data/input")

    if not input_dir.exists():
        print('Эта папка не найдена (data/input)')
        return
    run_output_dir = create_run_output_directory()
    set_log_file(run_output_dir)
    print(f"Результаты текущего запуска сохраняются в: {run_output_dir}")
    for path in list_input_files(input_dir):
        try:
            raw_text = read_file(path)
            email = parse_email(path, raw_text)
            category = classify_email(email)
        except (UnsupportedFileFormatError, EmptyEmailError):
            category = Category.unreadable
        except Exception as error:
            print(f"{path.name} -> error: {error}")
            record_error()
            continue

        copied = copy_email_to_category(str(path), category.value, run_output_dir)
        if copied:
            record_success(category.value)
            print(f"{path.name} -> {category.value}")
        else:
            record_error()
            print(f"{path.name} -> error: file move failed")
    report_path = generate_report(run_output_dir)
    print(f"Отчет сохранен в: {report_path}")
    print(f"Готово. Результаты лежат в: {run_output_dir}")


if __name__ == "__main__":
    main()
