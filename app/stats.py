#Очень похоже на reporter.py
#stats.py считает данные
#reporter.py красиво их оформляет и выводит
# Глобальный словарь, который работает как "блокнот" для нашей программы
processing_stats = {
    "total_processed": 0,  # Сколько всего файлов мы попытались открыть
    "categories": {},  # Сюда будем записывать счетчики по папкам, например: {"SPAM": 5, "NETWORK": 2}
    "unreadable": 0,  # Файлы, которые вообще не открылись (битые)
    "errors": 0  # Файлы, при перемещении которых случилась системная ошибка
}


def record_success(category_name: str):
    """
    Вызывается, когда файл успешно прочитан и отправлен в папку.
    Прибавляет +1 к общему счетчику и +1 к конкретной категории.
    """
    processing_stats["total_processed"] += 1

    # Если такой категории еще не было в блокноте - создаем её со счетом 0
    if category_name not in processing_stats["categories"]:
        processing_stats["categories"][category_name] = 0

    # Прибавляем единичку
    processing_stats["categories"][category_name] += 1


def record_unreadable():
    """Вызывается парсером, если внутри файла каша или он пустой"""
    processing_stats["total_processed"] += 1
    processing_stats["unreadable"] += 1


def record_error():
    """Вызывается органайзером, если файл не удалось переместить"""
    processing_stats["total_processed"] += 1
    processing_stats["errors"] += 1


def get_stats() -> dict:
    """Выдает итоговый блокнот с результатами (для финального отчета)"""
    return processing_stats