#Формирует отчет о работе системы.
#Сколько писем обработано, сколько попало в каждую категорию, сколько файлов не удалось прочитать,
#какие письма ушли в unknwown
from app.stats import get_stats

def generate_report():
    stats = get_stats()

    print("\n--- ИТОГОВЫЙ ОТЧЕТ О РАБОТЕ ---")
    print(f"Всего обработано файлов: {stats['total_processed']}")
    print(f"Ошибки при перемещении: {stats['errors']}")

    print("\nРазбивка по категориям:")
    for category, count in stats['categories'].items():
        print(f"- {category}: {count}")

    print("-------------------------------\n")
