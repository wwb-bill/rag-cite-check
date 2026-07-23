# rag-cite-check

Verify RAG citations survive chunk truncation and context packing.

```python
from rag_cite_check import check_citations
report = check_citations("See [1] and [2] for details.", ["chunk about topic 1", "chunk about topic 2"])
```

MIT
