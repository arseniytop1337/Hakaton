#Отвечает за действия с файлами после классификации
#Его задача: 1)создать нужные папки 2)переместить письмо в нужную папку
#То есть classifier решает что это, а organizer делает куда это положить
import os
import shutil
from app.logger import log_info

OUTPUT_DIR = "data/output"


def move_email_to_category(file_path: str, category_name: str):
    category_folder = os.path.join(OUTPUT_DIR, category_name)

    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    try:
        shutil.move(file_path, category_folder)
        log_info(file_path, "Успех", f"Перемещен в {category_folder}")
    except Exception as e:
        log_info(file_path, "Ошибка", str(e))