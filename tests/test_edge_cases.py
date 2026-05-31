#Проверяет проблемные случаи
#Например: пустой файл, неизвестный формат, письмо без темы, письмо без подходящей категории.


from pathlib import Path
from app.classifier import classify_email
from app.models import Category, EmailMessage


def unknown_email_goes_to_unknown():
    email = EmailMessage( #Создаем писбмо без явных признаков известных категорий
        path=Path('mail.txt'),
        subject='Приглашение на демо',
        sender='user@example.com',
        body="Нужно обсудить статус задач",
        raw_text="",
    )

    category = classify_email(email)
    assert category == category.UNKNOWN #проверяем что письмо ушло в UNKNOWN

