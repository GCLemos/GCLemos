"""Atualiza a idade nos READMEs a partir da data de nascimento.

Procura `idade: <n>` (README.md) e `age: <n>` (README.en.md) e troca o número.
Defina TODAY=AAAA-MM-DD para testar com outra data.
"""
import os
import re
from datetime import date, datetime, timedelta, timezone

BIRTH = date(2001, 9, 6)
FILES = {"README.md": r"(\bidade:\s*)\d+", "README.en.md": r"(\bage:\s*)\d+"}


def today() -> date:
    if os.environ.get("TODAY"):
        return date.fromisoformat(os.environ["TODAY"])
    # Horário de Brasília (UTC-3)
    return datetime.now(timezone(timedelta(hours=-3))).date()


def age_on(d: date) -> int:
    return d.year - BIRTH.year - ((d.month, d.day) < (BIRTH.month, BIRTH.day))


def main() -> None:
    age = age_on(today())
    for path, pattern in FILES.items():
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        new = re.sub(pattern, rf"\g<1>{age}", text, count=1)
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            print(f"{path}: idade -> {age}")
    print(f"Idade atual: {age}")


if __name__ == "__main__":
    main()
