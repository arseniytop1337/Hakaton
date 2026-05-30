#Определяет к каой категории относится письмо
#если есть urgent, critical, работа остановлена --> critical_incidents
#если есть доступ, права, логин --> access_requests
#если письмо похоже на фишинг -> spam_phishing

from app.models import Category, EmailMessage

def classify_email(message: EmailMessage) -> Category:
    text = "{email.subject} {email.body}".lower()
    #так выглядит одно правило
    if any(word in text for word in ["urgent",
                                     "critical",
                                     "работа остановлена",
                                     "не отвечает",
                                     "ошибка 500",
                                     "падает"]):
        return Category.CRITICAL_INCIDENTS #если в тексте встречаются подобные паттерны, то письмо относится к определнной категории

    if any(
        word in text for word in [
            "monitoring",
            "warning",
            "info",
            "disk usage",
            "cpu usage",
            "healthcheck"
        ]
    ):
        return Category.MONITORING #вернули категорию мониторинга

    #проверяем признаки локальных технических проблем
    if any(
        word in text for word in [
            "мышь",
            "гарнитура",
            "принтер",
            "zoom",
            "adobe",
            "chrome",
        ]
    ):
        return Category.TECHNICAL_ISSUES #значит это техническая проблема

    #Также проверяем подозрительные признаки спама или фишинга
    if any(
        word in text for word in [
            "exclusive offer",
            "банковской карты",
            "верификация аккаунта",
        ]
    ):
        return Category.SPAM_PHISHING

    return Category.UNKNOWN #если не под одно правило не подошло возвращаем неизвестную категорию
