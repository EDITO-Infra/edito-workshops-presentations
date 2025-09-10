# EDITO Workshops - Makefile
# Build system for documentation, presentations, and package management

# Virtual environment detection and activation
# You can override this by setting VENV_DIR environment variable
VENV_DIR ?= .venv
VENV_PYTHON = $(VENV_DIR)/bin/python
VENV_ACTIVATE = $(VENV_DIR)/bin/activate

# Check if uv is available
check-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "❌ uv not found. Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		echo "✅ uv installed"; \
	else \
		echo "✅ uv is available"; \
	fi

# Check if virtual environment exists, create if not
$(VENV_DIR): check-uv
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "🐍 Creating virtual environment with uv..."; \
		uv venv $(VENV_DIR); \
		echo "✅ Virtual environment created at $(VENV_DIR)"; \
	else \
		echo "✅ Virtual environment already exists at $(VENV_DIR)"; \
	fi

# Install dependencies in virtual environment
$(VENV_PYTHON): $(VENV_DIR)
	@echo "📦 Installing/updating dependencies with uv..."
	@if [ -f "uv.lock" ]; then \
		echo "Using uv sync for fast installation..."; \
		uv sync; \
	else \
		echo "Installing with uv pip..."; \
		uv pip install -e .; \
	fi
	@echo "✅ Dependencies installed"

.PHONY: help install install-dev clean build docs serve test lint format check-credentials

# Default target
help:
	@echo "🌊 EDITO Workshops - Available Commands:"
	@echo ""
	@echo "📦 Package Management:"
	@echo "  setup-fast    Fast setup with uv sync (recommended)"
	@echo "  setup         Complete setup (creates venv, installs deps)"
	@echo "  use-venv      Use existing virtual environment"
	@echo "  install-r     Install R dependencies"
	@echo "  clean         Clean build artifacts and virtual environment"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  docs          Build documentation (auto-creates venv if needed)"
	@echo "  serve         Serve documentation locally"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  test          Run tests"
	@echo "  lint          Run linting"
	@echo "  format        Format code"
	@echo "  check         Run all checks"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "  check-credentials  Check EDITO Datalab credentials"
	@echo "  build         Build package"

# Package management (now handled by virtual environment)

# Use existing virtual environment (if you have one elsewhere)
use-venv: check-uv
	@echo "🔍 Checking for existing virtual environment..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "✅ Using existing virtual environment: $$VIRTUAL_ENV"; \
		uv pip install --python $$VIRTUAL_ENV/bin/python -e .; \
		echo "✅ Dependencies installed in existing environment"; \
	else \
		echo "❌ No virtual environment detected. Run 'make setup' to create one."; \
	fi

install-r:
	@echo "📦 Installing R dependencies..."
	@if command -v R >/dev/null 2>&1; then \
		Rscript -e "if (!require('renv')) install.packages('renv'); renv::restore()"; \
	else \
		echo "❌ R not found. Please install R first."; \
	fi

# Documentation
docs: $(VENV_PYTHON)
	@echo "📚 Building documentation..."
	cd docs && . ../$(VENV_ACTIVATE) && make all

serve: $(VENV_PYTHON)
	@echo "🌐 Serving documentation locally..."
	cd docs && . ../$(VENV_ACTIVATE) && python -m http.server 8000

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf docs/build/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf $(VENV_DIR)/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Testing and quality
test: $(VENV_PYTHON)
	@echo "🧪 Running tests..."
	. $(VENV_ACTIVATE) && pytest tests/ -v --cov=edito_workshops --cov-report=html --cov-report=term-missing

lint: $(VENV_PYTHON)
	@echo "🔍 Running linting..."
	. $(VENV_ACTIVATE) && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	. $(VENV_ACTIVATE) && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
	. $(VENV_ACTIVATE) && mypy . --ignore-missing-imports

format: $(VENV_PYTHON)
	@echo "🎨 Formatting code..."
	. $(VENV_ACTIVATE) && black . --line-length 88
	. $(VENV_ACTIVATE) && isort . --profile black

check: lint test
	@echo "✅ All checks passed!"

# Utilities
check-credentials: $(VENV_PYTHON)
	@echo "🔑 Checking EDITO Datalab credentials..."
	. $(VENV_ACTIVATE) && python using_datalab/check_credentials.py

build: $(VENV_PYTHON)
	@echo "📦 Building package..."
	. $(VENV_ACTIVATE) && python -m build

# R-specific targets
r-check:
	@echo "🔍 Checking R package..."
	@if command -v R >/dev/null 2>&1; then \
		Rscript -e "devtools::check()"; \
	else \
		echo "❌ R not found. Please install R first."; \
	fi

r-install:
	@echo "📦 Installing R package..."
	@if command -v R >/dev/null 2>&1; then \
		Rscript -e "devtools::install()"; \
	else \
		echo "❌ R not found. Please install R first."; \
	fi

# Docker targets
docker-build:
	@echo "🐳 Building Docker images..."
	docker build -t edito-workshops .

docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 8000:8000 edito-workshops

# Git hooks
install-hooks:
	@echo "🔗 Installing git hooks..."
	@if [ -d .git ]; then \
		cp .githooks/pre-commit .git/hooks/; \
		chmod +x .git/hooks/pre-commit; \
		echo "✅ Git hooks installed!"; \
	else \
		echo "❌ Not a git repository"; \
	fi

# Fast setup using uv sync (recommended)
setup-fast: check-uv
	@echo "🚀 Fast setup with uv sync..."
	uv sync
	@echo "✅ Fast setup complete!"
	@echo "🌊 Ready to explore marine data with EDITO!"

# Complete setup (fallback)
setup: $(VENV_PYTHON) install-r
	@echo "✅ Setup complete!"
	@echo "🌊 Ready to explore marine data with EDITO!"

# Quick start
quickstart: setup-fast check-credentials
	@echo "🚀 Quick start complete!"
	@echo "📚 Run 'make serve' to view documentation"
	@echo "🔧 Run 'make check-credentials' to test EDITO Datalab connection"
