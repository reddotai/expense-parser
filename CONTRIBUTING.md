# Contributing to Expense Parser

Thank you for your interest in improving this tool! This guide is for both technical and non-technical contributors.

## Ways to Contribute

### For Non-Technical Users

1. **Report bugs** — Found an issue? Open a GitHub issue with:
   - What you were trying to do
   - What happened instead
   - Your receipt (or a similar example)
   - Your config.yaml (remove API keys!)

2. **Suggest features** — What would make this more useful for you?

3. **Share examples** — How are you using this? Share your config!

4. **Improve documentation** — Found something unclear? Suggest edits.

5. **Test with your receipts** — Try different receipt types and report results.

### For Developers

1. **Code contributions** — Pull requests welcome!
2. **Add integrations** — QuickBooks, Xero, SAP, etc.
3. **Improve OCR** — Better local processing without API calls
4. **Add tests** — Help make this more reliable

## Development Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/expense-parser.git
cd expense-parser

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .
flake8
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## Code Style

- Python: Follow PEP 8
- Use type hints where possible
- Document functions with docstrings
- Keep functions small and focused

## Feature Ideas

- [ ] PDF support (receipts from email)
- [ ] QuickBooks/Xero integration
- [ ] Multi-language receipt support
- [ ] Local OCR without API (Tesseract improvements)
- [ ] Web interface (no command line)
- [ ] Mobile app
- [ ] Automatic categorization learning
- [ ] Duplicate detection
- [ ] Receipt image enhancement
- [ ] Cloud storage integration (Google Drive, Dropbox)

## Questions?

Open an issue or reach out: [your-email@example.com]
