"""
Tests for PII Detector
"""

import pytest
from ai_qa_pipeline.modules.pii_detection import PIIDetector, PIIType


class TestPIIDetector:
    """Test suite for PIIDetector"""

    @pytest.fixture
    def detector(self):
        """Fixture for PIIDetector instance"""
        return PIIDetector(score_threshold=0.5)

    def test_detect_email(self, detector):
        """Test email detection"""
        text = "Contact us at support@example.com"
        entities = detector.detect(text)

        assert len(entities) > 0
        assert any(e.entity_type == PIIType.EMAIL for e in entities)

    def test_detect_phone(self, detector):
        """Test phone number detection"""
        text = "Call us at +1-555-0100 or 555-0200"
        entities = detector.detect(text)

        # Should detect at least one phone number
        phone_entities = [e for e in entities if e.entity_type == PIIType.PHONE]
        assert len(phone_entities) > 0

    def test_detect_person_name(self, detector):
        """Test person name detection"""
        text = "John Doe will contact you tomorrow"
        entities = detector.detect(text)

        person_entities = [e for e in entities if e.entity_type == PIIType.PERSON_NAME]
        assert len(person_entities) > 0

    def test_detect_ip_address(self, detector):
        """Test IP address detection"""
        text = "Server IP: 192.168.1.1"
        entities = detector.detect(text)

        ip_entities = [e for e in entities if e.entity_type == PIIType.IP_ADDRESS]
        assert len(ip_entities) > 0

    def test_detect_api_key(self, detector):
        """Test API key detection with custom patterns"""
        text = "API_KEY=sk_test_1234567890abcdefghijklmnop"
        entities = detector.detect(text)

        # Should detect API key through custom pattern
        api_entities = [e for e in entities if e.entity_type == PIIType.API_KEY]
        assert len(api_entities) > 0

    def test_empty_text(self, detector):
        """Test with empty text"""
        entities = detector.detect("")
        assert len(entities) == 0

    def test_multiple_pii_types(self, detector):
        """Test detection of multiple PII types in one text"""
        text = """
        Contact: John Doe
        Email: john@example.com
        Phone: +1-555-0100
        IP: 192.168.1.1
        """
        entities = detector.detect(text)

        # Should detect multiple different types
        assert len(entities) >= 3
        types_found = set(e.entity_type for e in entities)
        assert len(types_found) >= 3

    def test_score_threshold(self):
        """Test that score threshold works correctly"""
        detector_high = PIIDetector(score_threshold=0.9)
        detector_low = PIIDetector(score_threshold=0.3)

        text = "Contact: john@example.com"

        high_results = detector_high.detect(text)
        low_results = detector_low.detect(text)

        # Lower threshold should find same or more entities
        assert len(low_results) >= len(high_results)

    def test_analyze_file(self, detector, tmp_path):
        """Test file analysis"""
        # Create temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Email: user@test.com\nPhone: +1-555-0100")

        result = detector.analyze_file(str(test_file))

        assert "file_path" in result
        assert "total_entities" in result
        assert result["total_entities"] > 0
        assert "entities_by_type" in result
