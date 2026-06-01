from app.models import Category, EmailMessage

critical1 = ["критический инцидент", "работа остановлена", "работа полностью остановлена", "массовый сбой", "по-прежнему недоступен", "затронуты", "у всех отдела", "у всего отдела", "нужен статус", "срочная помощь", "ошибка 500",]
critical2 = ["active directory", "корпоративный портал", "gitlab", "service desk", "confluence", "bi-система",]
critical3 = ["не отвечает", "не могу войти", "доступ запрещён", "недоступен", "перестал открываться", "ошибка появляется сразу при входе",]
monitoring_content_keywords = ["[info]", "[warning]", "[critical]", "healthcheck", "disk usage", "cpu usage", "uptime", "5xx", "автоматическое уведомление", "плановый отчёт мониторинга", "сгенерировано автоматически", "статус: info", "статус: warning", "статус: critical", "метрика:",]
monitoring_sender_hints = ["monitoring.internal", "grafana.internal", "alerts@grafana", "no-reply@monitoring",]
access_keywords = ["запрос доступа", "выдать доступ", "предоставить доступ", "доступ к", "уровень доступа", "логин", "пароль", "учетная запись", "учётная запись", "сброс пароля", "нужны права", "выдать права", "пропал доступ", "восстановить доступ", "уровни доступа", "подготовить доступ", "доступы для нового сотрудника", "рабочее место и доступы",]
technical_keywords = ["мышь", "гарнитура", "принтер", "сканер", "ноутбук", "экран", "zoom", "adobe", "chrome", "excel", "антивирус", "не открывает", "не запускается", "не включается", "зависает", "установщик", "сломался", "ремонт", "переустановка не помогла", "ошибка при старте", "не могу установить", "перестал запускаться",]
service_keywords = ["личный кабинет", "клиент просит", "внешнего пользователя", "партнёр", "партнер", "клиент не может", "жалоба клиента", "подключиться к api", "не может зарегистрироваться", "кнопка 'подтвердить' не работает", "инструкция по работе", "не может подключиться", "нет ответа на тикет", "401 unauthorized",]
internal_communication_keywords = ["созвон", "статус задач", "приглашение на демо", "обсудить статус задач", "корпоративный дайджест", "дайджест", "в этом выпуске", "обновления корпоративного портала", "плановые технические работы", "технические работы", "профилактические работы", "ряд систем будет недоступен", "приглашаем на демо",]
non_support_keywords = ["счёт", "счет", "акт", "договор", "больничный", "больничный лист", "отпуск", "изменение графика работы", "izmenenie grafika raboty", "bolnichnyy list", "правки к", "новая версия", "финальная версия", "техническое задание", "инструкция", "принят в работу", "для внесения в систему",]
spam_keywords = ["exclusive offer", "банковской карты", "верификация аккаунта", "перейдите по ссылке", "обязательна до конца рабочего дня", "эксклюзивная акция", "скидка 90%", "только сегодня",]


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def is_critical_incident(content_text: str) -> bool:
    if contains_any(content_text, critical1):
        return True
    if contains_any(content_text, critical3) and contains_any(content_text, critical2):
        return True
    return False


def is_monitoring_email(content_text: str, sender_text: str) -> bool:
    if contains_any(content_text, monitoring_content_keywords):
        return True
    if any(hint in sender_text for hint in monitoring_sender_hints) and contains_any(content_text, ["[info]", "[warning]", "[critical]", "healthcheck", "cpu usage", "disk usage", "uptime", "автоматическое уведомление", "метрика:", "статус:",],):
        return True
    return False


def classify_email(message: EmailMessage) -> Category:
    content_text = f"{message.subject} {message.body}".lower()
    sender_text = message.sender.lower()

    if contains_any(content_text, spam_keywords):
        return Category.spam_phishing
    if is_monitoring_email(content_text, sender_text):
        return Category.monitoring
    if is_critical_incident(content_text):
        return Category.critical_incidents
    if contains_any(content_text, access_keywords):
        return Category.access_requests
    if contains_any(content_text, service_keywords):
        return Category.service_requests
    if contains_any(content_text, technical_keywords):
        return Category.technical_issues
    if contains_any(content_text, internal_communication_keywords):
        return Category.internal_communication
    if contains_any(content_text, non_support_keywords):
        return Category.non_support
    return Category.unknown
