import json
import re

text = input()
headings = input()

pairs_pattern = re.compile(r'\s*([^:;]+?)\s*:\s*([^;]*?);')
raw_fields = {k.strip().lower(): v for k, v in pairs_pattern.findall(text)}

needed = [h.strip().lower() for h in headings.split(',') if h.strip()]

def normalize_description(value: str) -> str:
    parts = value.split('. ')
    out = []
    for s in parts:
        s = s.strip()
        if not s:
            continue
        out.append(s[0].upper() + s[1:].lower() if len(s) > 1 else s.upper())
    return '. '.join(out)

def normalize_salary(value: str) -> str:
    return f"{float(value):.2f}"

def normalize_key_phrase(value: str) -> str:
    return value.upper() + '!'

def normalize_addition(value: str) -> str:
    return f"..{value.lower()}.."

def normalize_company_info(value: str) -> str:
    cleaned = value
    paren_pattern = re.compile(r'\([^()]*\)')
    while paren_pattern.search(cleaned):
        cleaned = paren_pattern.sub('', cleaned)
    return cleaned

def normalize_key_skills(value: str) -> str:
    return value.replace('&nbsp', ' ')

handlers = {
    'description': normalize_description,
    'salary': normalize_salary,
    'key_phrase': normalize_key_phrase,
    'addition': normalize_addition,
    'company_info': normalize_company_info,
    'key_skills': normalize_key_skills,
}

result = {}
for field in needed:
    if field in raw_fields:
        handler = handlers.get(field, lambda x: x)
        result[field] = handler(raw_fields[field])

print(json.dumps(result, ensure_ascii=False))
