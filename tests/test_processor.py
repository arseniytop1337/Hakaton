#Проверяет целиком сценарий обработки:
#взяли письмо --> распарсили --> классифицировали; --> переместили --> учли в статистике
#Этот тест будет уже проверять кусок моего пайплайна целиком

from app.reader import read_file
from app.parser import parse_email
from app.classifier import classify_email

def test_full_pipeline(tmp_path):
    file_path = tmp_path / "mail.txt" #создали временый входной файл
    file_path.write_text( #записываем туда письмо похожее на критический инидент
        "Subject: Active Directory не отвечает\n"
        "From: user@example.com\n\n"
        "Работа остановлена, у всего отдела проблемы со входом.",
        encoding="utf-8",
    )
    raw_text = read_file(file_path) #прочитали
    email = parse_email(file_path, raw_text) #наполнили структуру
    category = classify_email(email)#классифицировали
    assert category.value == "critical_incidents" # это должен быть критический инцидент

#тест успешен



