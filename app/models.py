from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Category(Enum):
    critical_incidents = "critical_incidents"
    access_requests = "access_requests"
    spam_phishing = "spam_phishing"
    technical_issues = "technical_issues"
    monitoring = "monitoring"
    non_support = "non_support"
    unknown = "unknown"
    unreadable = "unreadable"
    service_requests = "service_requests"
    internal_communication = "internal_communication"


@dataclass
class EmailMessage:
    path: Path
    subject: str
    sender: str
    body: str
    raw_text: str
