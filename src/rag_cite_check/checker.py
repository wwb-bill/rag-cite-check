import re

def check_citations(output: str, chunks: list) -> dict:
    refs = re.findall(r'\[(\d+)\]', output)
    refs = [int(r) for r in refs]
    total = len(refs)
    valid = sum(1 for r in refs if 1 <= r <= len(chunks))
    broken = total - valid
    return {"total_citations": total, "valid": valid, "broken": broken, "coverage": valid / total if total > 0 else 0}