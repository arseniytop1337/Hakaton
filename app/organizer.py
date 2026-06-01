import os
from datetime import datetime
import shutil
from app.logger import log_info

output_dir = "data/output"


def create_run_output_directory() -> str:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    run_folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
    run_output_dir = os.path.join(output_dir, run_folder_name)
    os.makedirs(run_output_dir)
    return run_output_dir


def copy_email_to_category(file_path: str, category_name: str, run_output_dir: str):
    category_folder = os.path.join(run_output_dir, category_name)

    if not os.path.exists(category_folder):
        os.makedirs(category_folder)
    destination_path = os.path.join(category_folder, os.path.basename(file_path))
    try:
        shutil.copy2(file_path, destination_path)
        log_info(file_path, "Успех", f"Скопирован в {destination_path}")
        return True
    except Exception as error:
        log_info(file_path, "Ошибка", str(error))
        return False
