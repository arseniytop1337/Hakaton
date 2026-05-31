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

#Главная функция запуска программы
def main():
    input_dir = Path("data/input") #указываем откуда брать файлы

    if not input_dir.exists():
        print('Эта папка не найдена (data/input)')
        return
    
    for path in list_input_files(input_dir): #если же папка нашлась то пройдемся по ее файлам
        try: #проходим полный пайплан обратоки файла
            raw_text = read_file(path)
            email = parse_email(path, raw_text)
            category = classify_email(email)
        except (UnsupportedFileFormatError, EmptyEmailError): #если файл попадает под исключения(нельзя прочитать или распарсить)
            category = Category.UNREADABLE #кидаем в категорию нечитаемый
        except Exception as error:
            print(f"{path.name} -> error: {error}")
            continue
        print(f"{path.name} -> {category.value}")


if __name__ == "__main__":
    main()

# Что делает:
# проходит по папке;
# читает файл;
# парсит;
# классифицирует;
# печатает результат.
