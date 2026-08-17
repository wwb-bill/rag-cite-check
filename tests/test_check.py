from rag_cite_check.checker import extract_citations, check_citations, citation_coverage, verify_truncation, hallucination_risk, unused_chunks


class TestExtract:
    def test_extracts_bracket_refs(self):
        refs = extract_citations("According to [1] and [2], the answer is [doc-3].")
        assert "1" in refs
        assert "2" in refs
        assert "doc-3" in refs

    def test_no_citations(self):
        assert extract_citations("No references here.") == []


class TestCheck:
    def test_backed_citations(self):
        chunks = {"1": "source one text", "2": "source two text"}
        results = check_citations("See [1] for details.", chunks)
        assert results[0].referenced is True

    def test_missing_citations(self):
        results = check_citations("See [missing] for details.", {"1": "text"})
        assert results[0].referenced is False


class TestCoverage:
    def test_full_coverage(self):
        cov = citation_coverage("Ref [a] and [b].", {"a": "text a", "b": "text b"})
        assert cov["coverage"] == 1.0

    def test_partial_coverage(self):
        cov = citation_coverage("Ref [a] and [c].", {"a": "text a"})
        assert cov["coverage"] == 0.5


class TestTruncation:
    def test_lost_chunks(self):
        orig = {"1": "a", "2": "b", "3": "c"}
        packed = {"1": "a", "3": "c"}
        result = verify_truncation(orig, packed)
        assert result["lost"] == 1
        assert "2" in result["lost_ids"]


class TestHallucinationRisk:
    def test_no_citations(self):
        r = hallucination_risk("No citations here.", {"1": "x"})
        assert r["risk"] == 0.0
        assert r["grade"] == "none"

    def test_full_risk(self):
        r = hallucination_risk("See [nope] for proof.", {"1": "x"})
        assert r["risk"] == 1.0
        assert r["grade"] == "high"

    def test_partial_risk(self):
        r = hallucination_risk("See [a] and [zz].", {"a": "x"})
        assert r["unbacked"] == 1
        assert r["risk"] == 0.5

    def test_low_grade_when_backed(self):
        r = hallucination_risk("See [1].", {"1": "x"})
        assert r["risk"] == 0.0
        assert r["grade"] == "low"


class TestUnusedChunks:
    def test_unused_ids(self):
        chunks = {"1": "a", "2": "b", "3": "c"}
        unused = unused_chunks("See [1].", chunks)
        assert "2" in unused and "3" in unused
        assert "1" not in unused

    def test_all_used(self):
        chunks = {"1": "a", "2": "b", "3": "c"}
        assert unused_chunks("See [1] [2] [3].", chunks) == []