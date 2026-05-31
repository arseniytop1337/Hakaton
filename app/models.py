#Здесь описываются основные сущности проекта: 1)обьект письма 2)результат парсинга 3)категория письма
#4)статус обработки

from dataclasses import dataclass
#испортируем dataclass, чтобы можно было удобно описывать простой обьектс полями
from enum import Enum
from pathlib import Path

#нужно дать категории письма, тогда программа будет по письму понимать в какую категорию его кинуть

class Category(Enum):
    CRITICAL_INCIDENTS = "critical_incidents" #система упала, работа присотановлена
    ACCESS_REQUESTS = "access_requests" #запросы на логины, доступы, права
    SPAM_PHISHING = "spam_phishing" #спам или фишинговые письма
    TECHNICAL_ISSUES = "technical_issues" # Обычные технические проблемы: софт, железо, локальные ошибки.
    MONITORING = "monitoring" #автоматические аллерты и мониторинг
    NON_SUPPORT = "non_support" # Письма не по адресу IT-support: документы, демо, больничные и т.д.
    UNKNOWN = "unknown" # Письмо прочитали, но не смогли разумно отнести ни к одной категории.
    UNREADABLE = "unreadable" # Файл не удалось нормально прочитать или распарсить.
    SERVICE_REQUESTS = "service_requests"
    INTERNAL_COMMUNICATION = "internal_communication" #комуникация между коллегами



#dataclass автоматически создаст удобное предсталение письма

@dataclass
class EmailMessage:
    path: Path #находит путь к файлу
    subject: str #тема письма
    sender: str #отправитель
    body: str #основной текст письма
    raw_text: str #полный тескт письма, чтобы при необходимости можно было бы смотреть его целиком



