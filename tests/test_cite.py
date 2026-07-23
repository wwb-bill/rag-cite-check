from rag_cite_check import check_citations

def test_valid():
    r = check_citations("See [1] and [2].", ["chunk1", "chunk2"])
    assert r["valid"] == 2
    assert r["broken"] == 0

def test_broken():
    r = check_citations("See [5].", ["chunk1"])
    assert r["broken"] == 1

def test_coverage():
    r = check_citations("[1] [2] [3]", ["a", "b", "c"])
    assert r["coverage"] == 1.0

def test_no_citations():
    r = check_citations("No refs here.", [])
    assert r["total_citations"] == 0