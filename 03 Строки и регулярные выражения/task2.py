import re

file = input().strip()
new_file = input().strip()
highlight = input().strip()
keywords = [kw.strip() for kw in highlight.split(',') if kw.strip()]

def normalize_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)

def normalize_time(s: str) -> str:
    return re.sub(r'(?<!\d)((?:[01]?\d|2[0-3]))\.([0-5]\d)(?!\d)', r'\1:\2', s)

def normalize_date(s: str) -> str:
    return re.sub(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:Z|[+-]\d{2}:?\d{2})', r'\4:\5:\6 \3/\2/\1', s)

def find_highlights(highlights, text: str) -> str:
    for h in highlights:
        pat = re.compile(rf'(?i)\b\w*(?:{re.escape(h)})\w*\b')
        text = pat.sub(lambda m: m.group(0).upper(), text)
    return text

with open(file, 'r', encoding='utf-8') as f:
    data = f.read()

data = normalize_time(data)
data = normalize_html(data)
data = normalize_date(data)
data = find_highlights(keywords, data)

with open(new_file, 'w', encoding='utf-8') as f:
    f.write(data)
