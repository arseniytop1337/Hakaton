#Превращает сырой текст файла в структурированные данные
#Например извлекает: отправителя, дату или тему письма
#Здесь же должна быть логика обработки разных форматов заголовков:

import re
from pathlib import Path
from app.models import EmailMessage #импортируем модель письма которую мы заполним после парсинга

#в слова HEADER_PATTERNS держим ключевые паттерны, которые могут попадатся в письмах
HEADER_PATTERNS = {
    # Для темы поддерживаем английский, русский и транслит.
    "subject": [
        r"^Subject:\s*(.*)$",
        r"^Тема:\s*(.*)$",
        r"^Tema:\s*(.*)$",
    ],

    # Для отправителя тоже поддерживаем несколько вариантов.
    "sender": [
        r"^From:\s*(.*)$",
        r"^От кого:\s*(.*)$",
        r"^Ot kogo:\s*(.*)$",
    ],
}

#функция ищет первое совпадение среди списка шаблонов
def extract_field(text: str, patterns: list[str]) -> str:
    for pattern in patterns: #перебираем все возможные шаблоны присущие для одного поля
        match = re.search(pattern, text, re.MULTILINE) #ищем совпадения не только на одной строке но и по всему  тексту
        if match: #если нашли совпадение возвращаем содержимое первой группы без пробелов
            return match.group(1).strip()
    return "" #если ничего не нашли

def extract_body(text: str) -> str: #пытается выделить тело письма
    parts = re.split(r"\n\s*\n", text, maxsplit=1) #делим заголовок и тело по первому пустому абзацу
    if len(parts) == 2:#если удалось поделить текст на 2 части
        return parts[1].strip() #возвращаем вторую часть как тело письма
    return text.strip() #если письмо странное и разделения нет, значит возвращаем текст полностью

def parse_email(path: Path, raw_text: str) -> EmailMessage: #Главная функция парсинга по сути: сделать из сырого текста обьект EmailMassage
    subject = extract_field(raw_text, HEADER_PATTERNS["subject"])#пытаемся вытащить тему письма
    sender = extract_field(raw_text, HEADER_PATTERNS["sender"])#пытаемся вытащить отправителя
    body = extract_body(raw_text)#пытаемся вытащить тело письма

    return EmailMessage( #возвращаем готовую структуру
        path=path,
        subject=subject,
        sender=sender,
        body=body,
        raw_text=raw_text,
    )



