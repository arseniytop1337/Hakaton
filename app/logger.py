def log_info(filename, action, details):
    with open("process.log", "a", encoding="utf-8") as file:
        file.write(f"{filename} - {action} - {details}\n")