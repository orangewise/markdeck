# SlideDown 🎬

A lightweight, markdown-based presentation tool that runs locally.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **📝 Markdown-based**: Write presentations in plain text using familiar Markdown syntax
- **🚀 Fast & Lightweight**: No heavy frameworks, just clean HTML/CSS/JS
- **🔥 Hot Reload**: Automatically refreshes when you edit your markdown file (with `--watch`)
- **🎨 Beautiful Design**: Modern, distraction-free presentation interface
- **⌨️ Keyboard Shortcuts**: Navigate efficiently with keyboard controls
- **💬 Speaker Notes**: Hidden notes visible in speaker view
- **🎯 Syntax Highlighting**: Beautiful code blocks powered by highlight.js
- **📱 Responsive**: Works on different screen sizes
- **🔧 Easy Setup**: Simple CLI interface, no complex configuration

## 🚀 Quick Start

### Installation

#### Install from GitHub (Recommended)

```bash
# Install directly from GitHub using uv
uv pip install git+https://github.com/orangewise/slidedown.git

# Install from a specific branch
uv pip install git+https://github.com/orangewise/slidedown.git@claude/init-slidedown-project-01DJeHxbuthmNtDFjgxToFrP

# Then run it
slidedown present examples/demo.md
```

#### Install from Local Clone

```bash
# Clone the repository
git clone https://github.com/orangewise/slidedown.git
cd slidedown

# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

### Run Without Installing

You can run SlideDown directly without permanent installation:

```bash
# Create a test presentation
echo "# Hello SlideDown

---

## Your First Slide

- Quick
- Easy
- Beautiful

---

## That's It!

Start creating your own presentations!" > test.md

# Run directly from GitHub (no installation needed)
uvx --from git+https://github.com/orangewise/slidedown.git@claude/init-slidedown-project-01DJeHxbuthmNtDFjgxToFrP slidedown present test.md

# Or use the main branch
uvx --from git+https://github.com/orangewise/slidedown.git slidedown present test.md
```

### Create Your First Presentation

```bash
# Create a new presentation from template
slidedown init my-presentation.md

# Start presenting
slidedown present my-presentation.md
```

Your browser will automatically open to `http://127.0.0.1:8000` with your presentation ready!

## 📖 Usage

### Basic Commands

```bash
# Present a markdown file
slidedown present slides.md

# Present with hot reload (auto-refresh on file changes)
slidedown present slides.md --watch

# Present on a custom port
slidedown present slides.md --port 3000

# Present without auto-opening browser
slidedown present slides.md --no-browser

# Combine options
slidedown present slides.md --watch --port 3000

# Create a new presentation
slidedown init my-talk.md

# Create with custom title
slidedown init my-talk.md --title "My Awesome Talk"

# Validate a presentation file
slidedown validate slides.md

# Show version
slidedown --version
```

### Markdown Syntax

Create slides by separating content with `---` on its own line:

```markdown
# My First Slide

This is the content of the first slide.

---

# Second Slide

- Bullet point 1
- Bullet point 2
- Bullet point 3

---

# Code Example

```python
def hello_slidedown():
    print("Hello from SlideDown!")
```

---

# Slide with Speaker Notes

This content is visible to the audience.

<!--NOTES:
These are speaker notes.
Press 'S' to toggle speaker notes view.
-->
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `→` / `Space` / `PageDown` | Next slide |
| `←` / `PageUp` | Previous slide |
| `Home` | First slide |
| `End` | Last slide |
| `F` | Toggle fullscreen |
| `S` | Toggle speaker notes |
| `?` | Show help |
| `Esc` | Exit fullscreen/help |

## 📁 Project Structure

```
slidedown/
├── slidedown/          # Main package
│   ├── __init__.py
│   ├── __main__.py     # Entry point
│   ├── cli.py          # CLI interface
│   ├── server.py       # FastAPI server
│   ├── parser.py       # Markdown parser
│   └── static/         # Frontend files
│       ├── index.html
│       ├── style.css
│       └── slides.js
├── tests/              # Unit tests
├── examples/           # Example presentations
│   ├── demo.md
│   ├── features.md
│   └── code-examples.md
└── pyproject.toml      # Project configuration
```

## 🎨 Features in Detail

### Markdown Support

SlideDown supports standard Markdown features:

- **Headings**: `#` through `######`
- **Bold**: `**bold**` or `__bold__`
- **Italic**: `*italic*` or `_italic_`
- **Code**: `` `inline code` ``
- **Links**: `[text](url)`
- **Images**: `![alt](url)`
- **Lists**: Unordered (`-`, `*`, `+`) and ordered (`1.`, `2.`)
- **Tables**: GitHub-flavored markdown tables
- **Blockquotes**: `> quote`
- **Code blocks**: Fenced with ` ``` `

### Code Syntax Highlighting

SlideDown includes syntax highlighting for many languages:

```python
# Python
def fibonacci(n):
    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)
```

```javascript
// JavaScript
const greet = (name) => console.log(`Hello, ${name}!`);
```

```rust
// Rust
fn main() {
    println!("Hello, SlideDown!");
}
```

### Speaker Notes

Add speaker notes that are hidden from the main view:

```markdown
# My Slide

Visible content here.

<!--NOTES:
These notes are only visible when you press 'S'
- Remember to mention X
- Don't forget Y
- Time: 2 minutes
-->
```

### Hot Reload

SlideDown includes hot reload functionality for a seamless development experience:

```bash
# Start with watch mode enabled
slidedown present my-slides.md --watch
```

**What happens:**
- SlideDown monitors your markdown file for changes
- When you save edits, the presentation automatically refreshes in your browser
- You stay on the current slide (or closest available slide if slides were removed)
- A brief "Presentation reloaded" notification appears

**Perfect for:**
- Iterating on your presentation content
- Live editing during practice sessions
- Quick feedback on formatting and layout changes

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/slidedown.git
cd slidedown

# Install with development dependencies
uv pip install -e ".[dev]"

# Run tests
python -m unittest discover tests/

# Run linter
ruff check .

# Format code
ruff format .
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run with verbose output
python -m unittest discover tests/ -v

# Run specific test file
python -m unittest tests.test_parser
```

### Project Commands

```bash
# Run the server in development mode
python -m slidedown present examples/demo.md

# Run linting
ruff check slidedown/ tests/

# Format code
ruff format slidedown/ tests/
```

## 📚 Examples

Check out the `examples/` directory for sample presentations:

- **demo.md**: Basic introduction to SlideDown
- **features.md**: Comprehensive feature showcase
- **code-examples.md**: Syntax highlighting demo

Try them out:

```bash
slidedown present examples/demo.md
slidedown present examples/features.md
slidedown present examples/code-examples.md
```

## 🗺️ Roadmap

### Phase 2 - Enhanced Features

- [x] Hot reload (watch file for changes) ✓
- [ ] Multiple themes (dark/light mode toggle)
- [ ] Slide overview/grid view
- [ ] Slide transitions
- [ ] Two-column layouts
- [ ] Media embedding improvements

### Phase 3 - Polish & Distribution (Planned)

- [ ] Export to PDF
- [ ] Export to standalone HTML
- [ ] Configuration file support
- [ ] Custom themes
- [ ] PyPI distribution
- [ ] Plugin system

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new features
5. Run tests and linting
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guide
- All tests pass
- New features include tests
- Documentation is updated

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [marked.js](https://marked.js.org/) - Markdown parser
- [highlight.js](https://highlightjs.org/) - Syntax highlighting
- [Python-Markdown](https://python-markdown.github.io/) - Server-side markdown parsing

## 📞 Support

- 🐛 [Report bugs](https://github.com/YOUR_USERNAME/slidedown/issues)
- 💡 [Request features](https://github.com/YOUR_USERNAME/slidedown/issues)
- 📖 [Documentation](https://github.com/YOUR_USERNAME/slidedown)

## ⭐ Show Your Support

If you find SlideDown useful, please consider giving it a star on GitHub!

---

**Made with ❤️ by the SlideDown community**
