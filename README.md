# rag-cite-check

Verify that RAG citations survive chunk truncation and context packing. Zero-dependency Python.

## Features

- **`extract_citations`** — pull `[n]` / `[doc-3]` references out of an output
- **`check_citations`** — which refs are backed by provided chunks
- **`citation_coverage`** — backed / total ratio
- **`verify_truncation`** — chunks lost during packing
- **`hallucination_risk`** — fraction of unverifiable citations (0-1 + grade)
- **`unused_chunks`** — chunks never cited → noise candidates for packing

## Install

```bash
pip install rag-cite-check
```

## Usage

```python
from rag_cite_check.checker import hallucination_risk, unused_chunks

risk = hallucination_risk(answer, chunks)   # {total, unbacked, risk, grade}
noise = unused_chunks(answer, chunks)       # ["2", "3"] — drop these when packing
```

## API

| Function | Description |
|----------|-------------|
| `extract_citations(text)` | Extract bracket refs |
| `check_citations(output, chunks)` | Backed / missing citations |
| `citation_coverage(output, chunks)` | Coverage metrics |
| `verify_truncation(original, packed)` | Chunks lost during packing |
| `hallucination_risk(output, chunks)` | Risk score + grade (none/low/medium/high) |
| `unused_chunks(output, chunks)` | Never-cited chunk ids (noise) |

## Test

```bash
pip install -e ".[dev]"
pytest
```

MIT