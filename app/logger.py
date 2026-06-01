import os


log_file_path = "process.log"


def set_log_file(run_output_dir: str) -> None:
    global log_file_path
    log_file_path = os.path.join(run_output_dir, "process.log")


def log_info(filename, action, details):
    with open(log_file_path, "a", encoding="utf-8") as file:
        file.write(f"{filename} - {action} - {details}\n")
