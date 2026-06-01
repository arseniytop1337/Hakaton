from pathlib import Path
from app.parser import parse_email

def test_parse_email_extracts_subject_and_sender():
    raw_text = (
        "Subject: Test subject\n"
        "From: test@example.com\n\n"
        "Hello world"
    )

    email = parse_email(Path("test.txt"), raw_text)

    assert email.subject == 'Test subject'
    assert email.sender == 'test@example.com'
    assert email.body == 'Hello world'

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
