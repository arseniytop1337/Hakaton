#Отвечает за действия с файлами после классификации
#Его задача: 1)создать нужные папки 2)переместить письмо в нужную папку
#То есть classifier решает что это, а organizer делает куда это положить
import os
import shutil

# Путь к главной папке, куда мы будем складывать отсортированные письма
OUTPUT_DIR = "data/output"


def move_email_to_category(file_path: str, category_name: str):
    """
    Функция берет исходный файл и перемещает его в папку категории.
    """

    # 1. Формируем путь к нужной папке (например: data/output/CRITICAL_INCIDENTS)
    category_folder = os.path.join(OUTPUT_DIR, category_name)

    # 2. Проверяем, существует ли такая папка. Если нет - создаем её.
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    # 3. Перемещаем файл из старого места в новую папку
    try:
        shutil.move(file_path, category_folder)
        print(f"Успех: файл {file_path} перемещен в {category_folder}")
    except Exception as e:
        print(f"Ошибка при перемещении файла {file_path}: {e}")