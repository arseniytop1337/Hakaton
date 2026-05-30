#Отсюда стартует приложение
#Задача этого файла: 1) прочитать настройку 2)запустить обработку 3)связать все модули между собой
#4) вывести итог

#Сначала сюда не надо пихать весь pipeline проекта.
# Только минимальный запуск для одного файла или папки.

from pathlib import Path

from app.reader import list_input_files, read_file
from app.parser import parse_email
from app.classifier import classify_email

#Главная функция запуска программы
def main():
    input_dir = Path("data/input") #указываем откуда брать файлы
    for path in list_input_files(input_dir): #получаем весь список файлов в этой папке
        raw_text = read_file(path) #читаем файл, получаем его текст

        email = parse_email(path, raw_text) #парсим этот текст, получаем структурированный текст
        category = classify_email(email) #определяем категорию письма
        print(f"{path.name} -> {category.value}")

if __name__ == "__main__":
    main()

# Что делает:
# проходит по папке;
# читает файл;
# парсит;
# классифицирует;
# печатает результат.
