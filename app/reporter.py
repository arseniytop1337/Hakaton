#Формирует отчет о работе системы.
#Сколько писем обработано, сколько попало в каждую категорию, сколько файлов не удалось прочитать,
#какие письма ушли в unknwown
from app.stats import get_stats
import os


def generate_report(run_output_dir: str) -> str:
    stats = get_stats() #перемещаем итоговый отчет(только цифры) в отдельную переменную
    lines = [
        "--- ИТОГОВЫЙ ОТЧЕТ О РАБОТЕ ---",
        f"Всего обработано файлов: {stats['total_processed']}",
        f"Ошибки при копировании: {stats['errors']}",
        "",
        "Разбивка по категориям:",
    ]
    for category, count in stats["categories"].items():
        lines.append(f"- {category}: {count}")
    lines.append("-------------------------------")
    report_text = "\n".join(lines) #собрали весь lines воедино
    report_path = os.path.join(run_output_dir, "report.txt") #собрали путь к файлу отчета

    print(f"\n{report_text}\n")
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report_text + "\n")
    return report_path #возвращаем путь к сохранненому отчету

#Итого - берет статистику из app.stats и красиво ее оформляет
