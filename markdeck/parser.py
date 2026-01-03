"""Markdown slide parser for MarkDeck."""

import re
from pathlib import Path
from typing import Any

import markdown


class Slide:
    """Represents a single slide in a presentation."""

    def __init__(self, content: str, index: int):
        """
        Initialize a slide.

        Args:
            content: Raw markdown content of the slide
            index: Zero-based index of the slide
        """
        self.content = content.strip()
        self.index = index
        self.notes = self._extract_notes()
        self._transform_columns()

    def _extract_notes(self) -> str:
        """
        Extract speaker notes from HTML comments.

        Returns:
            Extracted notes or empty string
        """
        notes_pattern = r"<!--\s*NOTES:\s*(.*?)\s*-->"
        match = re.search(notes_pattern, self.content, re.DOTALL | re.IGNORECASE)
        if match:
            # Remove the notes from content
            self.content = re.sub(notes_pattern, "", self.content, flags=re.DOTALL | re.IGNORECASE)
            self.content = self.content.strip()
            return match.group(1).strip()
        return ""

    def _transform_columns(self) -> None:
        """
        Transform column syntax into HTML div structure.

        Converts:
            :::columns
            Left content
            |||
            Right content
            :::

        Into HTML divs with pre-rendered markdown content
        """
        # Pattern to match column blocks (more forgiving with whitespace)
        column_pattern = r":::columns\s*\n(.*?)\s*\n:::"

        # Create markdown renderer with extensions
        md = markdown.Markdown(extensions=["extra", "codehilite", "fenced_code"])

        def replace_columns(match):
            content = match.group(1)
            # Split on ||| separator (more forgiving with whitespace)
            parts = re.split(r"\s*\|\|\|\s*", content, maxsplit=1)

            if len(parts) == 2:
                left_content = parts[0].strip()
                right_content = parts[1].strip()

                # Render each column's markdown to HTML
                # Reset the markdown instance for each column to avoid state issues
                md.reset()
                left_html = md.convert(left_content)
                md.reset()
                right_html = md.convert(right_content)

                # Create HTML structure that marked.js will pass through
                return (
                    '<div class="columns-container">\n'
                    f'<div class="column-left">\n{left_html}\n</div>\n'
                    f'<div class="column-right">\n{right_html}\n</div>\n'
                    '</div>'
                )
            else:
                # If no separator found, return original content
                return match.group(0)

        self.content = re.sub(column_pattern, replace_columns, self.content, flags=re.DOTALL)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert slide to dictionary format.

        Returns:
            Dictionary representation of the slide
        """
        return {
            "id": self.index,
            "content": self.content,
            "notes": self.notes,
        }


class SlideParser:
    """Parser for markdown files containing slides."""

    SLIDE_DELIMITER = "---"

    def __init__(self, file_path: str | Path):
        """
        Initialize the parser.

        Args:
            file_path: Path to the markdown file
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def parse(self) -> list[Slide]:
        """
        Parse the markdown file into slides.

        Returns:
            List of Slide objects
        """
        content = self.file_path.read_text(encoding="utf-8")
        return self.parse_content(content)

    @classmethod
    def parse_content(cls, content: str) -> list[Slide]:
        """
        Parse markdown content into slides.

        Args:
            content: Raw markdown content

        Returns:
            List of Slide objects
        """
        # Split on delimiter with proper handling of edge cases
        raw_slides = content.split(f"\n{cls.SLIDE_DELIMITER}\n")

        # Also handle delimiter at start or end of lines
        slides = []
        for raw_slide in raw_slides:
            # Remove leading/trailing delimiters if present
            raw_slide = raw_slide.strip()
            if raw_slide and raw_slide != cls.SLIDE_DELIMITER:
                slides.append(raw_slide)

        # Create Slide objects
        return [Slide(content, idx) for idx, content in enumerate(slides)]

    def get_title(self) -> str:
        """
        Extract the presentation title from the first slide.

        Returns:
            Title of the presentation or filename
        """
        slides = self.parse()
        if not slides:
            return self.file_path.stem

        # Try to find first H1 heading
        first_slide = slides[0].content
        h1_match = re.search(r"^#\s+(.+)$", first_slide, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()

        return self.file_path.stem

    def to_json(self) -> dict[str, Any]:
        """
        Convert parsed slides to JSON-serializable format.

        Returns:
            Dictionary with slides and metadata
        """
        slides = self.parse()
        return {
            "slides": [slide.to_dict() for slide in slides],
            "total": len(slides),
            "title": self.get_title(),
        }
