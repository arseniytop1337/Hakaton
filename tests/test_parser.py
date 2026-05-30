#Проверяет, что парсер правильно извлекает тему, отправителя, текст.

from pathlib import Path
from app.parser import parse_email

#Тест проверяет умеет ли парсер извлекать тему и отправителя
def test_parse_email_extracts_subject_and_sender():
    #Создаем исскуствнный текст письма для теста
    raw_text = (
        "Subject: Test subject\n"
        "From: test@example.com\n\n"
        "Hello world"
    )

    #Парсим письмо
    email = parse_email(Path("test.txt"), raw_text)

    #проверяем что тема письма
    assert email.subject == 'Test subject'
    assert email.sender == 'test@example.com' #Проверяем, что отправитель извлекся правильно.
    assert email.body == 'Hello world'# Проверяем, что тело письма извлеклось правильно.