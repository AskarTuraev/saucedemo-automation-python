"""
Tests for PII Masker
"""

import pytest
from ai_qa_pipeline.modules.pii_detection import PIIMasker, PIIEntity, PIIType


class TestPIIMasker:
    """Test suite for PIIMasker"""

    @pytest.fixture
    def sample_entities(self):
        """Fixture with sample PII entities"""
        return [
            PIIEntity(
                entity_type=PIIType.EMAIL,
                start=10,
                end=25,
                score=0.95,
                text="user@example.com"
            ),
            PIIEntity(
                entity_type=PIIType.PHONE,
                start=35,
                end=47,
                score=0.90,
                text="+1-555-0100"
            )
        ]

    def test_mask_with_replace_strategy(self, sample_entities):
        """Test replace masking strategy"""
        masker = PIIMasker(masking_strategy="replace")
        text = "Contact: user@example.com or call +1-555-0100"

        masked = masker.mask(text, sample_entities)

        assert "<EMAIL>" in masked
        assert "<PHONE_NUMBER>" in masked
        assert "user@example.com" not in masked
        assert "+1-555-0100" not in masked

    def test_mask_with_hash_strategy(self, sample_entities):
        """Test hash masking strategy"""
        masker = PIIMasker(masking_strategy="hash")
        text = "Contact: user@example.com or call +1-555-0100"

        masked = masker.mask(text, sample_entities)

        assert "<EMAIL_" in masked
        assert "<PHONE_NUMBER_" in masked
        # Original values should be gone
        assert "user@example.com" not in masked

    def test_mask_with_fake_strategy(self, sample_entities):
        """Test fake data masking strategy"""
        masker = PIIMasker(masking_strategy="fake")
        text = "Contact: user@example.com or call +1-555-0100"

        masked = masker.mask(text, sample_entities)

        # Should contain fake email
        assert "@" in masked
        assert "user@example.com" not in masked

    def test_mask_with_redact_strategy(self, sample_entities):
        """Test redact masking strategy"""
        masker = PIIMasker(masking_strategy="redact")
        text = "Contact: user@example.com or call +1-555-0100"

        masked = masker.mask(text, sample_entities)

        assert "[REDACTED]" in masked
        assert "user@example.com" not in masked

    def test_empty_entities_list(self):
        """Test masking with no entities"""
        masker = PIIMasker()
        text = "No PII here"

        masked = masker.mask(text, [])

        assert masked == text

    def test_unmask(self, sample_entities):
        """Test unmasking functionality"""
        masker = PIIMasker(masking_strategy="replace")
        original = "Contact: user@example.com or call +1-555-0100"

        masked = masker.mask(original, sample_entities)
        unmasked = masker.unmask(masked)

        # Should restore original (approximately)
        assert "user@example.com" in unmasked or "<EMAIL>" in unmasked

    def test_clear_mapping(self, sample_entities):
        """Test clearing PII mapping for security"""
        masker = PIIMasker()
        text = "Contact: user@example.com"

        masker.mask(text, sample_entities[:1])
        assert len(masker.pii_mapping) > 0

        masker.clear_mapping()
        assert len(masker.pii_mapping) == 0

    def test_mask_file(self, sample_entities, tmp_path):
        """Test file masking"""
        masker = PIIMasker(masking_strategy="replace")

        # Create input file
        input_file = tmp_path / "input.txt"
        input_file.write_text("Contact: user@example.com or call +1-555-0100")

        output_file = tmp_path / "output.txt"

        result = masker.mask_file(
            str(input_file),
            str(output_file),
            sample_entities
        )

        assert output_file.exists()
        masked_content = output_file.read_text()
        assert "<EMAIL>" in masked_content

        assert result["total_masked"] == len(sample_entities)
