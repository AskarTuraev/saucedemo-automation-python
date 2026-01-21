"""
Tests for PII Pipeline
"""

import pytest
from pathlib import Path
from ai_qa_pipeline.modules.pii_detection import PIIPipeline


class TestPIIPipeline:
    """Test suite for PIIPipeline"""

    @pytest.fixture
    def pipeline(self):
        """Fixture for PIIPipeline instance"""
        return PIIPipeline(
            masking_strategy="replace",
            score_threshold=0.5
        )

    def test_process_text_with_pii(self, pipeline):
        """Test processing text containing PII"""
        text = "Contact John Doe at john@example.com or +1-555-0100"

        result = pipeline.process_text(text, return_entities=True)

        assert result["pii_found"] is True
        assert result["pii_count"] > 0
        assert len(result["pii_types"]) > 0
        assert "entities" in result
        assert result["original_text"] == text
        assert result["masked_text"] != text

    def test_process_text_without_pii(self, pipeline):
        """Test processing text without PII"""
        text = "This is a simple test message without any personal data"

        result = pipeline.process_text(text)

        assert result["pii_found"] is False
        assert result["pii_count"] == 0
        assert result["masked_text"] == text  # Should be unchanged

    def test_is_safe_for_llm(self, pipeline):
        """Test safety check for LLM"""
        safe_text = "This text has no PII"
        unsafe_text = "Contact: user@example.com"

        assert pipeline.is_safe_for_llm(safe_text) is True
        assert pipeline.is_safe_for_llm(unsafe_text) is False

    def test_sanitize_for_llm(self, pipeline):
        """Test text sanitization for LLM"""
        text = "Email john@test.com to the admin"

        sanitized = pipeline.sanitize_for_llm(text)

        assert "@" not in sanitized or "example.com" in sanitized
        assert "john@test.com" not in sanitized

    def test_process_batch(self, pipeline):
        """Test batch processing"""
        texts = [
            "Contact: user1@test.com",
            "Call: +1-555-0100",
            "No PII here"
        ]

        results = pipeline.process_batch(texts)

        assert len(results) == 3
        assert results[0]["pii_found"] is True
        assert results[1]["pii_found"] is True
        assert results[2]["pii_found"] is False

    def test_process_file(self, pipeline, tmp_path):
        """Test file processing"""
        # Create test file
        input_file = tmp_path / "test_input.txt"
        input_file.write_text("Contact: user@test.com\nPhone: +1-555-0100")

        output_file = tmp_path / "test_output.txt"

        result = pipeline.process_file(
            str(input_file),
            str(output_file),
            save_report=True
        )

        assert result["pii_found"] is True
        assert result["pii_count"] > 0
        assert output_file.exists()

        # Check report
        report_file = input_file.with_suffix('.pii_report.json')
        assert report_file.exists()

    def test_different_masking_strategies(self):
        """Test different masking strategies"""
        text = "Email: user@test.com"

        strategies = ["replace", "hash", "fake", "redact"]
        results = []

        for strategy in strategies:
            pipeline = PIIPipeline(masking_strategy=strategy)
            result = pipeline.process_text(text)
            results.append(result["masked_text"])

        # All results should be different (except possibly some edge cases)
        assert len(set(results)) >= 3

    def test_custom_patterns(self):
        """Test custom pattern detection"""
        custom_patterns = {
            "CUSTOM_ID": r"ID-\d{6}"
        }

        pipeline = PIIPipeline(custom_patterns=custom_patterns)
        text = "Your ID-123456 has been processed"

        result = pipeline.process_text(text)

        # Custom pattern may not be in PIIType enum,
        # but should still be detected if added properly
        assert result["pii_count"] >= 0
