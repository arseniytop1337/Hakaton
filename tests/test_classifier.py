#Проверяет, что письма попадают в нужные категории.
#Тест будет проверять 4 проблемные категории
#critical_incidents, access_requests, internal_communication, service_requests
import pytest
from pathlib import Path
from app.classifier import classify_email
from app.models import Category, EmailMessage

#В каждом тесте есть данные. Те данные которые мы передали функции это есть данные на которых проверяется класификатор
#проверим критический инцидент
#функция позволяет запустить один и тот же тест много раз с разными входными данными, т е вместо того чтобы пистаь множество функций и подставлять туда разные значения можно использовать только одну
@pytest.mark.parametrize(
    ("subject", "sender", "body", "expected_category"), #то есть она подставляет под эти 4 категории те данные которые идут ниже
    [
        (
            "Падает корпоративный портал, работа остановлена", #subject
            "user@example.com",#sender
            "У всего отдела проблемы со входом. Нужна срочная помощь.",#body
            Category.CRITICAL_INCIDENTS,#expected_category
        ),
        (
            "Запрос доступа к VPN",
            "user@example.com",
            "Нужны права на VPN для временного сотрудника.",
            Category.ACCESS_REQUESTS,
        ),
        (
            "Ошибка в Adobe Reader после обновления",
            "user@example.com",
            "Не могу установить Adobe Reader — установщик зависает на 80% и выдаёт ошибку. Переустановка не помогла.",
            Category.TECHNICAL_ISSUES,
        ),
        (
            "[INFO] API Gateway не отвечает на healthcheck",
            "alerts@grafana.internal",
            "Автоматическое уведомление от системы мониторинга. Метрика: CPU usage 77%. Статус: INFO.",
            Category.MONITORING,
        ),
        (
            "Запрос от внешнего пользователя",
            "client@example.com",
            "Клиент не может зарегистрироваться на портале. Кнопка 'Подтвердить' не работает.",
            Category.SERVICE_REQUESTS,
        ),
        (
            "Корпоративный дайджест — выпуск #38",
            "user@example.com",
            "В этом выпуске: итоги квартала и изменения в политике ИБ.",
            Category.INTERNAL_COMMUNICATION,
        ),
        (
            "Финальная версия: инструкция",
            "user@example.com",
            "Прошу подтвердить, что инструкция принята в работу.",
            Category.NON_SUPPORT,
        ),
        (
            "Re: Exclusive offer — limited time",
            "spam@example.com",
            "Эксклюзивная акция. Перейдите по ссылке и введите данные банковской карты.",
            Category.SPAM_PHISHING,
        ),
        (
            "Re:",
            "user@example.com",
            "Не работает.",
            Category.UNKNOWN,
        ),
    ],
)

def test_classify_email_by_category(subject, sender, body, expected_category):
    email = EmailMessage(
        path=Path("mail.txt"),
        subject=subject,
        sender=sender,
        body=body,
        raw_text="",
    )

    category = classify_email(email)
    assert category == expected_category
#Все 9 тестов прошли успешно




