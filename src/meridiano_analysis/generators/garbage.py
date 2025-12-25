"""
Garbage data generators.

Simulates real-world data quality issues from different subsidiaries.
"""
import random
import string


def add_garbage_currency(currency: str) -> str:
    """Introduce currency format garbage."""
    variants = {
        "EUR": ["EUR", "Euro", "EURO", "€", " EUR", "EUR ", "eur", "Eur"],
        "USD": ["USD", "US$", "Dollar", "DOLLAR", "$", "usd", "Usd", " USD"],
        "GBP": ["GBP", "£", "Pound", "POUND", "gbp", "Gbp", "GBP "],
        "BRL": ["BRL", "R$", "Real", "REAL", "brl", "Brl", "BRL "],
        "MXN": ["MXN", "MX$", "Peso", "PESO", "mxn", "Mxn", "MXN "],
    }
    return random.choice(variants.get(currency, [currency]))


def add_garbage_concept(concept: str) -> str:
    """Introduce concept name garbage."""
    garbage_types = [
        lambda c: c.lower(),
        lambda c: c.replace("_", " "),
        lambda c: c.replace("_", "-"),
        lambda c: " " + c,
        lambda c: c + " ",
        lambda c: c + random.choice(["", " 2024", " Q4", " FY23"]),
        lambda c: c.replace("BONUS", "BONU"),
        lambda c: c.replace("DIFERIDO", "DEFERIDO"),
        lambda c: c.replace("Ñ", "N").replace("ñ", "n"),
    ]
    return random.choice(garbage_types)(concept)


def add_garbage_amount(amount: float) -> float:
    """Introduce amount garbage."""
    garbage_types = [
        lambda a: a,
        lambda a: a * 1000,
        lambda a: a / 1000,
        lambda a: -abs(a) if random.random() < 0.1 else a,
        lambda a: round(a, 0),
        lambda a: a * 12 if random.random() < 0.05 else a,
    ]
    return garbage_types[0](amount) if random.random() > 0.3 else random.choice(garbage_types)(amount)


def add_garbage_employee_id(emp_id: str, subsidiary: str) -> str:
    """Introduce employee ID garbage based on subsidiary legacy systems."""
    garbage_by_region = {
        "BR": lambda e: e.replace("-", ""),
        "AR": lambda e: "ARG" + e[-8:],
        "MX": lambda e: e.upper().replace("EMP", "MX-EMP"),
        "CN": lambda e: e + "-" + "".join(random.choices(string.ascii_uppercase, k=2)),
    }
    country = subsidiary.split("-")[0]
    if country in garbage_by_region and random.random() < 0.3:
        return garbage_by_region[country](emp_id)
    return emp_id
