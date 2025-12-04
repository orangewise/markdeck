"""Tests for the markdown parser."""

from pathlib import Path

import pytest

from slidedown.parser import Slide, SlideParser


class TestSlide:
    """Test the Slide class."""

    def test_slide_creation(self):
        """Test basic slide creation."""
        content = "# Test Slide\n\nThis is content."
        slide = Slide(content, 0)

        assert slide.content == content
        assert slide.index == 0
        assert slide.notes == ""

    def test_slide_with_notes(self):
        """Test slide with speaker notes."""
        content = """# Test Slide

Content here

<!--NOTES:
These are notes
-->"""
        slide = Slide(content, 0)

        assert "NOTES" not in slide.content
        assert slide.notes == "These are notes"

    def test_slide_to_dict(self):
        """Test converting slide to dictionary."""
        slide = Slide("# Test", 0)
        result = slide.to_dict()

        assert result["id"] == 0
        assert result["content"] == "# Test"
        assert "notes" in result

    def test_empty_slide(self):
        """Test handling of empty slide."""
        slide = Slide("   \n\n   ", 0)
        assert slide.content == ""


class TestSlideParser:
    """Test the SlideParser class."""

    def test_parse_content_single_slide(self):
        """Test parsing content with a single slide."""
        content = "# Single Slide\n\nContent here."
        slides = SlideParser.parse_content(content)

        assert len(slides) == 1
        assert slides[0].content == content

    def test_parse_content_multiple_slides(self):
        """Test parsing content with multiple slides."""
        content = """# Slide 1

Content 1

---

# Slide 2

Content 2

---

# Slide 3

Content 3"""
        slides = SlideParser.parse_content(content)

        assert len(slides) == 3
        assert "# Slide 1" in slides[0].content
        assert "# Slide 2" in slides[1].content
        assert "# Slide 3" in slides[2].content

    def test_parse_content_with_empty_slides(self):
        """Test parsing content with empty slides filtered out."""
        content = """# Slide 1

---

---

# Slide 2"""
        slides = SlideParser.parse_content(content)

        # Empty slides should be filtered out
        assert all(slide.content for slide in slides)

    def test_parse_content_edge_cases(self):
        """Test edge cases in parsing."""
        # Delimiter at start
        content = "---\n# Slide 1"
        slides = SlideParser.parse_content(content)
        assert len(slides) >= 1

        # Delimiter at end
        content = "# Slide 1\n---"
        slides = SlideParser.parse_content(content)
        assert len(slides) >= 1

    def test_get_title_from_h1(self):
        """Test extracting title from first H1."""
        content = "# My Presentation\n\nContent\n---\n# Slide 2"
        slides = SlideParser.parse_content(content)
        parser = SlideParser.__new__(SlideParser)
        parser.file_path = Path("test.md")

        # Mock parse method
        def mock_parse():
            return slides
        parser.parse = mock_parse

        title = parser.get_title()
        assert title == "My Presentation"

    def test_to_json(self):
        """Test converting parser output to JSON format."""
        content = "# Slide 1\n---\n# Slide 2"
        parser = SlideParser.__new__(SlideParser)
        parser.file_path = Path("test.md")

        slides = SlideParser.parse_content(content)

        def mock_parse():
            return slides
        parser.parse = mock_parse

        result = parser.to_json()

        assert "slides" in result
        assert "total" in result
        assert "title" in result
        assert result["total"] == 2
        assert len(result["slides"]) == 2


class TestSlideParserWithFiles:
    """Test SlideParser with actual files."""

    def test_file_not_found(self):
        """Test handling of missing file."""
        with pytest.raises(FileNotFoundError):
            SlideParser("nonexistent.md")

    def test_parse_real_file(self, tmp_path):
        """Test parsing a real markdown file."""
        test_file = tmp_path / "test.md"
        content = """# Test Presentation

Intro slide

---

# Second Slide

Content here

<!--NOTES:
Speaker notes for testing
-->

---

# Final Slide

Conclusion"""
        test_file.write_text(content, encoding="utf-8")

        parser = SlideParser(test_file)
        slides = parser.parse()

        assert len(slides) == 3
        assert slides[0].index == 0
        assert slides[1].notes == "Speaker notes for testing"
        assert slides[2].index == 2

    def test_get_title_fallback_to_filename(self, tmp_path):
        """Test title fallback to filename when no H1 present."""
        test_file = tmp_path / "my-presentation.md"
        test_file.write_text("Content without H1", encoding="utf-8")

        parser = SlideParser(test_file)
        title = parser.get_title()

        assert title == "my-presentation"
