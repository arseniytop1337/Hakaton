#Отсюда стартует приложение
#Задача этого файла: 1) прочитать настройку 2)запустить обработку 3)связать все модули между собой
#4) вывести итог

#Сначала сюда не надо пихать весь pipeline проекта.
# Только минимальный запуск для одного файла или папки.

from pathlib import Path
from app.exceptions import EmptyEmailError, UnsupportedFileFormatError
from app.reader import list_input_files, read_file
from app.parser import parse_email
from app.classifier import classify_email
from app.models import Category
from app.organizer import create_run_output_directory, copy_email_to_category
from app.reporter import generate_report
from app.stats import record_error, record_success
from app.logger import set_log_file  # Импортируем функцию, которая настраивает лог для конкретного запуска.

#Главная функция запуска программы
def main():
    input_dir = Path("data/input") #указываем откуда брать файлы

    if not input_dir.exists():
        print('Эта папка не найдена (data/input)')
        return
    run_output_dir = create_run_output_directory() #создаем конкретную папку результата для текущего запроса
    set_log_file(run_output_dir) #теперь лог пишется именно в эту папку запуска
    print(f"Результаты текущего запуска сохраняются в: {run_output_dir}")
    for path in list_input_files(input_dir): #если же папка нашлась то пройдемся по ее файлам
        try: #проходим полный пайплан обратоки файла
            raw_text = read_file(path)
            email = parse_email(path, raw_text)
            category = classify_email(email)
        except (UnsupportedFileFormatError, EmptyEmailError): #если файл попадает под исключения(нельзя прочитать или распарсить)
            category = Category.UNREADABLE #кидаем в категорию нечитаемый
        except Exception as error:
            print(f"{path.name} -> error: {error}")
            record_error() #увеличили счетчик ошибок
            continue

        copied = copy_email_to_category(str(path), category.value, run_output_dir) #копируем папку внутрь именно текущего запуска
        if copied:
            record_success(category.value) #записали что перемистится удалось успешно
            print(f"{path.name} -> {category.value}") #напечатали результат обработки файла
        else:
            record_error()
            print(f"{path.name} -> error: file move failed")
    report_path = generate_report(run_output_dir) #генериуем отчет текущего запуска
    print(f"Отчет сохранен в: {report_path}")
    print(f"Готово. Результаты лежат в: {run_output_dir}")


if __name__ == "__main__":
    main()

# Что делает:
# проходит по папке;
# читает файл;
# парсит;
# классифицирует;
# печатает результат.
