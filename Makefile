# EDITO Workshops - Makefile
# Build system for documentation, presentations, and package management

.PHONY: help install install-dev clean build docs serve test lint format check-credentials

# Default target
help:
	@echo "🌊 EDITO Workshops - Available Commands:"
	@echo ""
	@echo "📦 Package Management:"
	@echo "  install       Install Python dependencies"
	@echo "  install-dev   Install development dependencies"
	@echo "  install-r     Install R dependencies"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  docs          Build documentation"
	@echo "  serve         Serve documentation locally"
	@echo "  clean         Clean build artifacts"
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

# Package management
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt

install-dev:
	@echo "📦 Installing development dependencies..."
	pip install -r requirements-dev.txt

install-r:
	@echo "📦 Installing R dependencies..."
	@if command -v R >/dev/null 2>&1; then \
		Rscript -e "if (!require('renv')) install.packages('renv'); renv::restore()"; \
	else \
		echo "❌ R not found. Please install R first."; \
	fi

# Documentation
docs:
	@echo "📚 Building documentation..."
	cd docs && make all

serve:
	@echo "🌐 Serving documentation locally..."
	cd docs && python -m http.server 8000

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf docs/build/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Testing and quality
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --cov=edito_workshops --cov-report=html --cov-report=term-missing

lint:
	@echo "🔍 Running linting..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
	mypy . --ignore-missing-imports

format:
	@echo "🎨 Formatting code..."
	black . --line-length 88
	isort . --profile black

check: lint test
	@echo "✅ All checks passed!"

# Utilities
check-credentials:
	@echo "🔑 Checking EDITO Datalab credentials..."
	python using_datalab/check_credentials.py

build:
	@echo "📦 Building package..."
	python -m build

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

# Complete setup
setup: install install-dev install-r
	@echo "✅ Setup complete!"
	@echo "🌊 Ready to explore marine data with EDITO!"

# Quick start
quickstart: setup check-credentials
	@echo "🚀 Quick start complete!"
	@echo "📚 Run 'make serve' to view documentation"
	@echo "🔧 Run 'make check-credentials' to test EDITO Datalab connection"
