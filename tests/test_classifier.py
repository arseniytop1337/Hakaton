import pytest
from pathlib import Path
from app.classifier import classify_email
from app.models import Category, EmailMessage

@pytest.mark.parametrize(
    ("subject", "sender", "body", "expected_category"),
    [
        (
            "Падает корпоративный портал, работа остановлена",
            "user@example.com",
            "У всего отдела проблемы со входом. Нужна срочная помощь.",
            Category.critical_incidents,
        ),
        (
            "Запрос доступа к VPN",
            "user@example.com",
            "Нужны права на VPN для временного сотрудника.",
            Category.access_requests,
        ),
        (
            "Ошибка в Adobe Reader после обновления",
            "user@example.com",
            "Не могу установить Adobe Reader — установщик зависает на 80% и выдаёт ошибку. Переустановка не помогла.",
            Category.technical_issues,
        ),
        (
            "[INFO] API Gateway не отвечает на healthcheck",
            "alerts@grafana.internal",
            "Автоматическое уведомление от системы мониторинга. Метрика: CPU usage 77%. Статус: INFO.",
            Category.monitoring,
        ),
        (
            "Запрос от внешнего пользователя",
            "client@example.com",
            "Клиент не может зарегистрироваться на портале. Кнопка 'Подтвердить' не работает.",
            Category.service_requests,
        ),
        (
            "Корпоративный дайджест — выпуск #38",
            "user@example.com",
            "В этом выпуске: итоги квартала и изменения в политике ИБ.",
            Category.internal_communication,
        ),
        (
            "Финальная версия: инструкция",
            "user@example.com",
            "Прошу подтвердить, что инструкция принята в работу.",
            Category.non_support,
        ),
        (
            "Re: Exclusive offer — limited time",
            "spam@example.com",
            "Эксклюзивная акция. Перейдите по ссылке и введите данные банковской карты.",
            Category.spam_phishing,
        ),
        (
            "Re:",
            "user@example.com",
            "Не работает.",
            Category.unknown,
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



