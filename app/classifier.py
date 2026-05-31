#Определяет к каой категории относится письмо
#если есть urgent, critical, работа остановлена --> critical_incidents
#если есть доступ, права, логин --> access_requests
#если письмо похоже на фишинг -> spam_phishing

from app.models import Category, EmailMessage
#признаки масштаба и серьзености проблемы
CRITICAL_OUTAGE_HINTS = [
    "критический инцидент",
    "работа остановлена",
    "работа полностью остановлена",
    "массовый сбой",
    "по-прежнему недоступен",
    "затронуты",
    "у всех отдела",
    "у всего отдела",
    "нужен статус",
    "срочная помощь",
    "ошибка 500",
]
#Это название важных систем или сервисов, сами по себе не означают критический инцидент
CRITICAL_SERVICE_HINTS = [
    "active directory",
    "корпоративный портал",
    "gitlab",
    "service desk",
    "confluence",
    "bi-система",
]
#Признаки фактической поломки или отказа
CRITICAL_FAILURE_HINTS = [
    "не отвечает",
    "не могу войти",
    "доступ запрещён",
    "недоступен",
    "перестал открываться",
    "ошибка появляется сразу при входе",
]
#только CRITICAL_SERVICE_HINTS не всегда критично
#Только CRITICAL_FAILURE_HINTS это может быть прблема одного пользователя

#Я разделяю критические слоова на 3 категории потому, если есть только CRITICAL_OUTAGE_HINTS, то этого уже достаточно чтобы перемстить в папку к критическим элементам
#Но чтобы определить CRITICAL_SERVICE_HINTS или CRITICAL_FAILURE_HINTS в критические инциденты, нужно чтобы были признаки из обоих списков



MONITORING_CONTENT_KEYWORDS = [ #слова для основного текста
    "[info]",
    "[warning]",
    "[critical]",
    "healthcheck",
    "disk usage",
    "cpu usage",
    "uptime",
    "5xx",
    "автоматическое уведомление",
    "плановый отчёт мониторинга",
    "сгенерировано автоматически",
    "статус: info",
    "статус: warning",
    "статус: critical",
    "метрика:",
]

MONITORING_SENDER_HINTS = [ #слова для отправителя
    "monitoring.internal",
    "grafana.internal",
    "alerts@grafana",
    "no-reply@monitoring",
]


ACCESS_KEYWORDS = [
    "запрос доступа",
    "выдать доступ",
    "предоставить доступ",
    "доступ к",
    "уровень доступа",
    "логин",
    "пароль",
    "учетная запись",
    "учётная запись",
    "сброс пароля",
    "нужны права",
    "выдать права",
    "пропал доступ",
    "восстановить доступ",
    "уровни доступа",
    "подготовить доступ",
    "доступы для нового сотрудника",
    "рабочее место и доступы",
]

TECHNICAL_KEYWORDS = [
    "мышь",
    "гарнитура",
    "принтер",
    "сканер",
    "ноутбук",
    "экран",
    "zoom",
    "adobe",
    "chrome",
    "excel",
    "антивирус",
    "не открывает",
    "не запускается",
    "не включается",
    "зависает",
    "установщик",
    "сломался",
    "ремонт",
    "переустановка не помогла",
    "ошибка при старте",
    "не могу установить",
    "перестал запускаться",
]

SERVICE_KEYWORDS = [
    "личный кабинет",
    "клиент просит",
    "внешнего пользователя",
    "партнёр",
    "партнер",
    "клиент не может",
    "жалоба клиента",
    "подключиться к api",
    "не может зарегистрироваться",
    "кнопка 'подтвердить' не работает",
    "инструкция по работе",
    "не может подключиться",
    "нет ответа на тикет",
    "401 unauthorized",
]

INTERNAL_COMMUNICATION_KEYWORDS = [
    "созвон",
    "статус задач",
    "приглашение на демо",
    "обсудить статус задач",
    "корпоративный дайджест",
    "дайджест",
    "в этом выпуске",
    "обновления корпоративного портала",
    "плановые технические работы",
    "технические работы",
    "профилактические работы",
    "ряд систем будет недоступен",
    "приглашаем на демо",
]

NON_SUPPORT_KEYWORDS = [
    "счёт",
    "счет",
    "акт",
    "договор",
    "больничный",
    "больничный лист",
    "отпуск",
    "изменение графика работы",
    "izmenenie grafika raboty",
    "bolnichnyy list",
    "правки к",
    "новая версия",
    "финальная версия",
    "техническое задание",
    "инструкция",
    "принят в работу",
    "для внесения в систему",
]

SPAM_KEYWORDS = [
    "exclusive offer",
    "банковской карты",
    "верификация аккаунта",
    "перейдите по ссылке",
    "обязательна до конца рабочего дня",
    "эксклюзивная акция",
    "скидка 90%",
    "только сегодня",
]


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords) #возвращает из всего текста(text) любые слова которые есть списке слов определнной группы
#Это реально автоматическое письмо мониторинга, или просто письмо, которое случайно пришло от странного адреса?
def is_critical_incident(content_text: str) -> bool:
    if contains_any(content_text, CRITICAL_OUTAGE_HINTS):
        return True
    if contains_any(content_text, CRITICAL_FAILURE_HINTS) and contains_any(content_text, CRITICAL_SERVICE_HINTS):
        return True
    return False

def is_monitoring_email(content_text: str, sender_text:str) -> bool: #сначала в функции проверим, отправитель мониторинговый
    #потом проверим если и основной текст текст мониторинговый
    if contains_any(content_text, MONITORING_CONTENT_KEYWORDS): #основное сожержание письма
        return True
    if any(hint in sender_text for hint in MONITORING_SENDER_HINTS) and contains_any( #если отправитель похож на мониторинговую систему этого еще недостаточно, чтобы сказать что письмо мониторинговое
            content_text,
            [
                "[info]",
                "[warning]",
                "[critical]",
                "healthcheck",
                "cpu usage",
                "disk usage",
                "uptime",
                "автоматическое уведомление",
                "метрика:",
                "статус:",
            ],
    ):
        return True


def classify_email(message: EmailMessage) -> Category:
    content_text = f"{message.subject} {message.body}".lower() #все категории кроме мониторинга проверяем по контексту
    sender_text = message.sender.lower() #оставили отправителя для мониторинга

    if contains_any(content_text, SPAM_KEYWORDS):
        return Category.SPAM_PHISHING

    if is_monitoring_email(content_text, sender_text): #мониторинг проверяем отдельной функцией
        return Category.MONITORING

    if is_critical_incident(content_text):
        return Category.CRITICAL_INCIDENTS

    if contains_any(content_text, ACCESS_KEYWORDS):
        return Category.ACCESS_REQUESTS

    if contains_any(content_text, SERVICE_KEYWORDS):
        return Category.SERVICE_REQUESTS

    if contains_any(content_text, TECHNICAL_KEYWORDS):
        return Category.TECHNICAL_ISSUES

    if contains_any(content_text, INTERNAL_COMMUNICATION_KEYWORDS):
        return Category.INTERNAL_COMMUNICATION

    if contains_any(content_text, NON_SUPPORT_KEYWORDS):
        return Category.NON_SUPPORT

    return Category.UNKNOWN