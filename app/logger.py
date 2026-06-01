import os


LOG_FILE_PATH = "process.log" #по умоляанию лог будет писатся в файл process.log

def set_log_file(run_output_dir:str) -> None: #Функция задает путь к лог-файлу для конкретного запуска.
    global LOG_FILE_PATH #будем менять глобальную перменную
    LOG_FILE_PATH = os.path.join(run_output_dir, "process.log")#соьрали путь ввида data/output/<run_id>/process.log.

def log_info(filename, action, details):
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as file:
        file.write(f"{filename} - {action} - {details}\n") #имя_файла - действие - подробности