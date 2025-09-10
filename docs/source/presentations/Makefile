# Makefile for building Marp presentations
# Builds HTML presentations from Markdown files using Marp

# Variables
MARP = marp
OUTPUT_DIR = ../../presentations
CSS_FILE = ../static/styles/edito-marp.css

# Source files
SOURCES = $(wildcard *.md)
HTML_TARGETS = $(SOURCES:.md=.html)
PDF_TARGETS = $(SOURCES:.md=.pdf)

# Default target
all: html

# Build HTML presentations
html: $(HTML_TARGETS)
	@echo "Copying static assets..."
	@mkdir -p $(OUTPUT_DIR)/static/images
	@mkdir -p $(OUTPUT_DIR)/static/styles
	@mkdir -p $(OUTPUT_DIR)/static/videos
	@cp -r ../static/images/* $(OUTPUT_DIR)/static/images/ 2>/dev/null || true
	@cp -r ../static/styles/* $(OUTPUT_DIR)/static/styles/ 2>/dev/null || true
	@cp -r ../static/videos/* $(OUTPUT_DIR)/static/videos/ 2>/dev/null || true
	@echo "HTML presentations built successfully"

# Build PDF presentations  
pdf: $(PDF_TARGETS)
	@echo "PDF presentations built successfully"

# Build individual HTML files
%.html: %.md
	@echo "Building $@ from $<"
	@echo "CSS file path: $(CSS_FILE)"
	@ls -la $(CSS_FILE) || echo "CSS file not found"
	@mkdir -p $(OUTPUT_DIR)
	$(MARP) $< --html --output $(OUTPUT_DIR)/$@ --theme-set $(CSS_FILE)

# Build individual PDF files
%.pdf: %.md
	@echo "Building $@ from $<"
	@mkdir -p $(OUTPUT_DIR)
	$(MARP) $< --pdf --output $(OUTPUT_DIR)/$@ --theme-set $(CSS_FILE)

# Clean build artifacts
clean:
	@echo "Cleaning presentation build artifacts..."
	rm -f $(OUTPUT_DIR)/*.html $(OUTPUT_DIR)/*.pdf

# Help
help:
	@echo "Available targets:"
	@echo "  all     - Build all HTML presentations"
	@echo "  html    - Build all HTML presentations"
	@echo "  pdf     - Build all PDF presentations"
	@echo "  clean   - Remove build artifacts"
	@echo "  help    - Show this help"

.PHONY: all html pdf clean help
