"""FastAPI server for SlideDown presentation viewer."""

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from slidedown.parser import SlideParser

app = FastAPI(title="SlideDown", description="Markdown presentation tool")

# Global variable to store the current presentation file
_current_file: Path | None = None


def set_presentation_file(file_path: str | Path | None) -> None:
    """
    Set the current presentation file.

    Args:
        file_path: Path to the markdown file or None to clear
    """
    global _current_file
    _current_file = Path(file_path) if file_path is not None else None


def get_static_dir() -> Path:
    """Get the path to the static directory."""
    return Path(__file__).parent / "static"


# Mount static files
app.mount("/static", StaticFiles(directory=get_static_dir()), name="static")


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """
    Serve the main presentation viewer HTML.

    Returns:
        HTML response with the viewer page
    """
    html_file = get_static_dir() / "index.html"
    if not html_file.exists():
        raise HTTPException(status_code=500, detail="Viewer HTML not found")

    content = html_file.read_text(encoding="utf-8")
    return HTMLResponse(content=content)


@app.get("/api/slides")
async def get_slides(file: str | None = None) -> dict[str, Any]:
    """
    Get parsed slides from the markdown file.

    Args:
        file: Optional file path (uses current file if not provided)

    Returns:
        JSON with slides and metadata
    """
    target_file = Path(file) if file else _current_file

    if not target_file:
        raise HTTPException(status_code=400, detail="No presentation file specified")

    if not target_file.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {target_file}")

    try:
        parser = SlideParser(target_file)
        return parser.to_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")


@app.get("/health")
async def health() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Status message
    """
    return {"status": "ok"}
