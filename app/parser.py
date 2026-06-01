import re
from pathlib import Path
from app.models import EmailMessage

header_patterns = {
    "subject": [
        r"^Subject:\s*(.*)$",
        r"^Тема:\s*(.*)$",
        r"^Tema:\s*(.*)$",
    ],
    "sender": [
        r"^From:\s*(.*)$",
        r"^От кого:\s*(.*)$",
        r"^Ot kogo:\s*(.*)$",
    ],
}


def extract_field(text: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            return match.group(1).strip()
    return ""


def extract_body(text: str) -> str:
    parts = re.split(r"\n\s*\n", text, maxsplit=1)
    if len(parts) == 2:
        return parts[1].strip()
    return text.strip()


def parse_email(path: Path, raw_text: str) -> EmailMessage:
    subject = extract_field(raw_text, header_patterns["subject"])
    sender = extract_field(raw_text, header_patterns["sender"])
    body = extract_body(raw_text)

    return EmailMessage(
        path=path,
        subject=subject,
        sender=sender,
        body=body,
        raw_text=raw_text,
    )
