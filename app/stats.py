#Очень похоже на reporter.py
#stats.py считает данные
#reporter.py красиво их оформляет и выводит
# Глобальный словарь, который работает как "блокнот" для нашей программы
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