#Проверяет проблемные случаи
#Например: пустой файл, неизвестный формат, письмо без темы, письмо без подходящей категории.
#Проверяем на пограничные случаи

from pathlib import Path
import pytest #pytest для проверки исключений
from app.classifier import classify_email
from app.models import Category, EmailMessage
from app.exceptions import UnsupportedFileFormatError, EmptyEmailError
from app.reader import read_file
from app.parser import parse_email


def test_unknown_email_goes_to_unknown():
    email = EmailMessage( #проверяем что не информативное письмо уходит в unknown
        path=Path("mail.txt"),
        subject="Re:",
        sender="user@example.com",
        body="Не работает.",
        raw_text="",
    )

    category = classify_email(email)
    assert category == category.UNKNOWN #проверяем что письмо ушло в UNKNOWN

def test_empty_file_raises_error(tmp_path): #tmp_path - это временнеая папка, которую pytest создает сам
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8") #создаем файл файл но внутрь не кладем никакого содержимого
    with pytest.raises(EmptyEmailError): #если видит что файл пустой, выбрасывает EmptyEmailError
        read_file(file_path)

def test_unsupported_file_extension_raises_error(tmp_path):
    file_path = tmp_path / "broken.bin" #файл с неподдерживаемым расширением
    file_path.write_text("Поставьте 8, пожалуйста", encoding="utf-8")
    with pytest.raises(UnsupportedFileFormatError):
        read_file(file_path)

def test_whitespace_only_file_raises_error(tmp_path): #тестируем если в файле только пробелы
    file_path = tmp_path / "spaces.txt"
    file_path.write_text("   \n\t  ", encoding="utf-8")

    with pytest.raises(EmptyEmailError):
        read_file(file_path)
def test_file_without_extension_is_supported(tmp_path): #файл без расширения все равно должен читаться номрально
    file_path = tmp_path / "mail_0106"
    file_path.write_text(
        "From: test@example.com\n"
        "Subject: Test\n\n"
        "Body text",
        encoding="utf-8",
    )
    text = read_file(file_path)
    assert "Body text" in text

def test_parse_email_without_subject_returns_empty_subject(): #письма без темы не должны ломать парсер
    raw_text = (
        "From: test@example.com\n\n"
        "Body without subject"
    )

    email = parse_email(Path("mail.txt"), raw_text)
    assert email.subject == ""
    assert email.sender == "test@example.com"
    assert email.body == "Body without subject" #должен просто вернуть пустую тему "", а остальные поля извлечь нормально.

#Все тесты прошли успешно







