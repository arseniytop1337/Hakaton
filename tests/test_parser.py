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

#Проверим также транслитные заголовки
def test_parse_email_with_translit():
    raw_text = (
        "Tema: Izmenenie grafika raboty\n"
        "Ot kogo: a.fedorova@company.ru\n\n"
        "Napravlyayu bolnichnyy list"
    )

    email = parse_email(Path("mail.txt"), raw_text)
    assert email.subject == "Izmenenie grafika raboty"
    assert email.sender == "a.fedorova@company.ru"
    assert email.body == "Napravlyayu bolnichnyy list"
#этот проверяет понимает ли парсер грязные данные из текста

#РАБОТАЕТ КОРЕКТНО

