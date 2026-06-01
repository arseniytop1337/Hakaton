#Отвечает за действия с файлами после классификации
#Его задача: 1)создать нужные папки 2)переместить письмо в нужную папку
#То есть classifier решает что это, а organizer делает куда это положить
import os
from datetime import datetime
import shutil #умеет перемещать файлы
from app.logger import log_info #импортируем функцию логирования чтобы записывать результат перемещения

OUTPUT_DIR = "data/output"

def create_run_output_directory() -> None: #функция создания выходной папки
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    run_folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f") #будет дата прогона всего пайплайна
    run_output_dir = os.path.join(OUTPUT_DIR, run_folder_name)
    os.makedirs(run_output_dir)
    return run_output_dir #создается выходная папка, которая будет включатьв себя время




def copy_email_to_category(file_path: str, category_name: str, run_output_dir: str): #создаем папку нужной категории, если ее еще нет, перемещаем файл в нужную папку
    category_folder = os.path.join(run_output_dir, category_name) #собрали путь куда надо положить готовый файл

    if not os.path.exists(category_folder): #если папки пока не существует, то создаем ее
        os.makedirs(category_folder)
    destination_path = os.path.join(category_folder, os.path.basename(file_path)) #папка назначения = папка категории + исходное имя файла
    try:
        shutil.copy2(file_path, destination_path) #копируем файл в папку категории, т е он не будет удалятся из начальной папки(input)
        log_info(file_path, "Успех", f"Скопирован в {destination_path}")
        return True
    except Exception as error: #если случилась ошибка при перемещении то передаем это в лог.
        log_info(file_path, "Ошибка", str(error))
        return False
#Это важно потому что теперь app.main.py будет понимать что возвращать record_succes() или record_error()