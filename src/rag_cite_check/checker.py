"""Citation verification for RAG outputs."""

import re
from dataclasses import dataclass


@dataclass
class Citation:
    id: str
    source_text: str
    referenced: bool  # found in source chunks
    truncated: bool   # reference lost due to truncation


def extract_citations(text: str) -> list[str]:
    """Extract citation references from text (e.g., [1], [src-a], [doc-3])."""
    return list(set(re.findall(r'\[([^\]]+)\]', text)))


def check_citations(output: str, chunks: dict[str, str]) -> list[Citation]:
    """Check which citations in the output are backed by provided chunks."""
    refs = extract_citations(output)
    results = []
    for ref in refs:
        found = any(ref.lower() in cid.lower() for cid in chunks.keys())
        source = chunks.get(ref, "")
        results.append(Citation(id=ref, source_text=source[:100], referenced=found, truncated=not found))
    return results


def citation_coverage(output: str, chunks: dict[str, str]) -> dict:
    """Calculate citation coverage metrics."""
    refs = extract_citations(output)
    if not refs:
        return {"total": 0, "backed": 0, "missing": 0, "coverage": 1.0}
    backed = sum(1 for r in refs if any(r.lower() in cid.lower() for cid in chunks.keys()))
    return {"total": len(refs), "backed": backed, "missing": len(refs) - backed, "coverage": backed / len(refs)}


def verify_truncation(original_chunks: dict[str, str], packed_chunks: dict[str, str]) -> dict:
    """Check which chunks were lost during packing/truncation."""
    lost = set(original_chunks.keys()) - set(packed_chunks.keys())
    return {"original_count": len(original_chunks), "packed_count": len(packed_chunks), "lost": len(lost), "lost_ids": sorted(lost)}


def _is_backed(ref: str, chunks: dict[str, str]) -> bool:
    return any(ref.lower() in cid.lower() for cid in chunks.keys())


def hallucination_risk(output: str, chunks: dict[str, str]) -> dict:
    """Fraction of citations not backed by provided chunks (unverifiable claims)."""
    refs = extract_citations(output)
    if not refs:
        return {"total": 0, "unbacked": 0, "risk": 0.0, "grade": "none"}
    unbacked = sum(1 for r in refs if not _is_backed(r, chunks))
    risk = unbacked / len(refs)
    grade = "high" if risk > 0.5 else ("medium" if risk > 0 else "low")
    return {"total": len(refs), "unbacked": unbacked, "risk": round(risk, 4), "grade": grade}


def unused_chunks(output: str, chunks: dict[str, str]) -> list[str]:
    """Chunk ids never cited in the output — candidate noise to drop when packing."""
    refs = [r.lower() for r in extract_citations(output)]
    unused = []
    for cid in chunks.keys():
        if not any(r in cid.lower() for r in refs):
            unused.append(cid)
    return sorted(unused)