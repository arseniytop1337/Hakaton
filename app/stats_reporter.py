
processing_stats = {
    "total_processed": 0,
    "categories": {
        "critical_incidents": 0,
        "access_requests": 0,
        "technical_issues": 0,
        "monitoring": 0,
        "service_requests": 0,
        "internal_communication": 0,
        "non_support": 0,
        "spam_phishing": 0,
        "unknown": 0,
        "unreadable": 0
    },
    "errors": 0
}


def record_success(category_name: str):
    processing_stats["total_processed"] += 1
    processing_stats["categories"][category_name] += 1


def record_error():
    processing_stats["total_processed"] += 1
    processing_stats["errors"] += 1

def get_stats() -> dict:
    return processing_stats


def generate_report(run_output_dir: str) -> str:
    import os
    stats = get_stats()
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
    report_text = "\n".join(lines)
    report_path = os.path.join(run_output_dir, "report.txt")

    print(f"\n{report_text}\n")
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report_text + "\n")
    return report_path
