from app.reader import read_file
from app.parser import parse_email
from app.classifier import classify_email

def test_full_pipeline(tmp_path):
    file_path = tmp_path / "mail.txt"
    file_path.write_text(
        "Subject: Active Directory не отвечает\n"
        "From: user@example.com\n\n"
        "Работа остановлена, у всего отдела проблемы со входом.",
        encoding="utf-8",
    )
    raw_text = read_file(file_path)
    email = parse_email(file_path, raw_text)
    category = classify_email(email)
    assert category.value == "critical_incidents"


