"""Tests for the FastAPI server."""


import pytest
from fastapi.testclient import TestClient

from slidedown.server import app, set_presentation_file


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_markdown_file(tmp_path):
    """Create a sample markdown file for testing."""
    test_file = tmp_path / "test.md"
    content = """# Test Presentation

First slide

---

# Second Slide

Second slide content

<!--NOTES:
Test notes
-->

---

# Third Slide

Final slide"""
    test_file.write_text(content, encoding="utf-8")
    return test_file


class TestHealthEndpoint:
    """Test the health check endpoint."""

    def test_health_check(self, client):
        """Test health endpoint returns OK."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestSlidesEndpoint:
    """Test the slides API endpoint."""

    def test_get_slides_no_file(self, client):
        """Test getting slides without setting a file."""
        set_presentation_file(None)
        response = client.get("/api/slides")
        assert response.status_code == 400

    def test_get_slides_with_current_file(self, client, sample_markdown_file):
        """Test getting slides with current file set."""
        set_presentation_file(sample_markdown_file)
        response = client.get("/api/slides")

        assert response.status_code == 200
        data = response.json()

        assert "slides" in data
        assert "total" in data
        assert "title" in data
        assert data["total"] == 3
        assert len(data["slides"]) == 3

    def test_get_slides_with_query_param(self, client, sample_markdown_file):
        """Test getting slides with file query parameter."""
        response = client.get(f"/api/slides?file={sample_markdown_file}")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3

    def test_get_slides_file_not_found(self, client):
        """Test getting slides with non-existent file."""
        response = client.get("/api/slides?file=/nonexistent/file.md")
        assert response.status_code == 404

    def test_slide_structure(self, client, sample_markdown_file):
        """Test the structure of returned slides."""
        set_presentation_file(sample_markdown_file)
        response = client.get("/api/slides")
        data = response.json()

        slide = data["slides"][0]
        assert "id" in slide
        assert "content" in slide
        assert "notes" in slide
        assert slide["id"] == 0

    def test_speaker_notes_extraction(self, client, sample_markdown_file):
        """Test that speaker notes are properly extracted."""
        set_presentation_file(sample_markdown_file)
        response = client.get("/api/slides")
        data = response.json()

        # Second slide has notes
        slide_with_notes = data["slides"][1]
        assert slide_with_notes["notes"] == "Test notes"
        assert "NOTES" not in slide_with_notes["content"]


class TestRootEndpoint:
    """Test the root HTML endpoint."""

    def test_root_returns_html(self, client):
        """Test that root endpoint returns HTML."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "SlideDown" in response.text


class TestStaticFiles:
    """Test static file serving."""

    def test_css_file_served(self, client):
        """Test that CSS file is served."""
        response = client.get("/static/style.css")
        assert response.status_code == 200
        assert "text/css" in response.headers["content-type"]

    def test_js_file_served(self, client):
        """Test that JavaScript file is served."""
        response = client.get("/static/slides.js")
        assert response.status_code == 200
