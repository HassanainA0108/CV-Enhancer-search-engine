import re

HEADINGS = {
    'summary': r'(professional\s+)?summary|profile|objective',
    'skills': r'(technical|core|key)\s+(skills|competenc(?:y|ies))|skills|technologies|tech stack',
    'experience': r'(professional|work|employment)\s+(experience|history)|experience',
    'projects': r'(key|selected|professional)\s+projects|projects',
    'education': r'education|academic background',
    'certifications': r'certifications?|licenses',
}


def split_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {'general': []}
    section = 'general'
    for line in text.splitlines():
        value = line.strip(' :\t-•').strip()
        if len(value) < 65:
            for name, pattern in HEADINGS.items():
                if re.fullmatch(pattern, value, flags=re.I):
                    section = name
                    sections.setdefault(section, [])
                    break
            else:
                sections[section].append(line)
        else:
            sections[section].append(line)
    return {k: '\n'.join(v).strip() for k,v in sections.items() if '\n'.join(v).strip()}


def make_chunks(sections: dict[str,str], max_chars: int = 1000, overlap: int = 120):
    chunks = []
    for section, content in sections.items():
        paragraphs = [p.strip() for p in re.split(r'\n{2,}', content) if p.strip()]
        # Keep paragraph-level boundaries when possible; long paragraphs are split with overlap.
        for para in paragraphs:
            if len(para) <= max_chars:
                chunks.append({'section': section, 'text': para})
            else:
                pos = 0
                while pos < len(para):
                    chunks.append({'section':section,'text':para[pos:pos + max_chars]})
                    if pos + max_chars >= len(para):
                        break
                    pos += max_chars - overlap
    return chunks
