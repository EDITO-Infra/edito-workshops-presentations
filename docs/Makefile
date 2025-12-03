# Minimal makefile for MkDocs documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
MKDOCS        ?= mkdocs
SOURCEDIR     = source
BUILDDIR      = build
DOCS_DIR      = $(shell pwd)

# Put it first so that "make" without argument is like "make help".
help:
	@echo "Available targets:"
	@echo "  all              - Build documentation and presentations (HTML + PDF)"
	@echo "  html             - Build MkDocs documentation only"
	@echo "  presentations    - Build all presentations (HTML + PDF)"
	@echo "  presentations-html - Build HTML presentations only (for CI)"
	@echo "  presentations-pdf  - Build PDF presentations only (for local)"
	@echo "  events           - Build all events (HTML + PDF)"
	@echo "  events-html      - Build HTML events only (for CI)"
	@echo "  events-pdf       - Build PDF events only (for local)"
	@echo "  clean            - Remove build artifacts"
	@echo "  help             - Show this help"

# Build MkDocs HTML documentation only
html:
	@echo "Building MkDocs documentation..."
	cd .. && . .venv/bin/activate && $(MKDOCS) build --site-dir docs/$(BUILDDIR)/html
	@echo "Copying static files to build/html/static..."
	@mkdir -p $(BUILDDIR)/html/static
	@cp -r $(DOCS_DIR)/source/static/* $(BUILDDIR)/html/static/
	@echo "✅ Static files copied to build/html/static"

# Check if marp is installed, install if not
check-marp:
	@if ! command -v marp >/dev/null 2>&1; then \
		echo "❌ marp-cli not found. Installing..."; \
		if command -v npm >/dev/null 2>&1; then \
			npm install -g @marp-team/marp-cli; \
		elif command -v brew >/dev/null 2>&1; then \
			brew install marp-cli; \
		elif command -v apt-get >/dev/null 2>&1; then \
			echo "Please install marp-cli manually: npm install -g @marp-team/marp-cli"; \
			exit 1; \
		else \
			echo "Please install marp-cli manually: npm install -g @marp-team/marp-cli"; \
			exit 1; \
		fi; \
	else \
		echo "✅ marp-cli is available"; \
	fi

# Presentation files - only files with 'slidedeck' in the name
PRESENTATIONS = $(wildcard $(SOURCEDIR)/presentations/*slidedeck*.md)
HTML_PRESENTATIONS = $(PRESENTATIONS:$(SOURCEDIR)/presentations/%.md=$(BUILDDIR)/html/presentations/%.html)
PDF_PRESENTATIONS = $(PRESENTATIONS:$(SOURCEDIR)/presentations/%.md=presentations/%.pdf)

# Build HTML presentations only (for CI/browser)
presentations-html: check-marp $(HTML_PRESENTATIONS)
	@echo "✅ HTML presentations built successfully!"

# Build PDF presentations only (for local use)
presentations-pdf: check-marp $(PDF_PRESENTATIONS)
	@echo "✅ PDF presentations built successfully!"

# Build all presentations (HTML and PDF)
presentations: presentations-html presentations-pdf
	@echo "✅ All presentations (HTML and PDF) built successfully!"

# Event files - only files with 'slidedeck' in the name
EVENTS = $(wildcard $(SOURCEDIR)/presentations/events/*slidedeck*.md)
HTML_EVENTS = $(EVENTS:$(SOURCEDIR)/presentations/events/%.md=$(BUILDDIR)/html/presentations/events/%.html)
PDF_EVENTS = $(EVENTS:$(SOURCEDIR)/presentations/events/%.md=presentations/events/%.pdf)

# Build HTML events only (for CI/browser)
events-html: check-marp $(HTML_EVENTS)
	@echo "✅ HTML events built successfully!"

# Build PDF events only (for local use)
events-pdf: check-marp $(PDF_EVENTS)
	@echo "✅ PDF events built successfully!"

# Build all events (HTML and PDF)
events: events-html events-pdf
	@echo "✅ All events (HTML and PDF) built successfully!"

# Build individual HTML events
$(BUILDDIR)/html/presentations/events/%.html: $(SOURCEDIR)/presentations/events/%.md
	@echo "Building HTML event: $@"
	@mkdir -p $(BUILDDIR)/html/presentations/events
	@cd .. && . .venv/bin/activate && marp docs/$< --output docs/$@ --theme docs/$(SOURCEDIR)/static/styles/edito-marp.css --allow-local-files

# Build individual PDF events
presentations/events/%.pdf: $(SOURCEDIR)/events/%.md
	@echo "Building PDF event: $@"
	@mkdir -p presentations/events
	@cd .. && . .venv/bin/activate && marp docs/$< --pdf --output docs/$@ --theme docs/$(SOURCEDIR)/static/styles/edito-marp.css --allow-local-files

# Build individual HTML presentations
$(BUILDDIR)/html/presentations/%.html: $(SOURCEDIR)/presentations/%.md
	@echo "Building HTML presentation: $@"
	@mkdir -p $(BUILDDIR)/html/presentations
	@cd .. && . .venv/bin/activate && marp docs/$< --output docs/$@ --theme docs/$(SOURCEDIR)/static/styles/edito-marp.css --allow-local-files

# Build individual PDF presentations
presentations/%.pdf: $(SOURCEDIR)/presentations/%.md
	@echo "Building PDF presentation: $@"
	@mkdir -p presentations
	@cd .. && . .venv/bin/activate && marp docs/$< --pdf --output docs/$@ --theme docs/$(SOURCEDIR)/static/styles/edito-marp.css --allow-local-files

# Build everything (for manual builds)
all: html presentations events

# Ensure build/html directory exists
$(BUILDDIR)/html:
	@mkdir -p $@

.PHONY: help html presentations events check-marp all clean

clean:
	rm -rf $(BUILDDIR)/*