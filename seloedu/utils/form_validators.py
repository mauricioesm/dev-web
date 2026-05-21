from datetime import datetime


def clean_text(value):
    return (value or "").strip()


def clean_email(value):
    return clean_text(value).lower()


def require_fields(data, fields, errors):
    for field, label in fields:
        if not clean_text(data.get(field)):
            errors.append(f"{label} e obrigatorio.")


def parse_date(value, label, errors, required=False):
    value = clean_text(value)
    if not value:
        if required:
            errors.append(f"{label} e obrigatorio.")
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        errors.append(f"{label} deve estar no formato AAAA-MM-DD.")
        return None


def parse_positive_int(value, label, errors):
    value = clean_text(value)
    if not value:
        errors.append(f"{label} e obrigatorio.")
        return 0

    try:
        number = int(value)
    except ValueError:
        errors.append(f"{label} deve ser um numero inteiro.")
        return 0

    if number <= 0:
        errors.append(f"{label} deve ser maior que zero.")
    return number
