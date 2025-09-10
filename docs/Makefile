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
	@echo "  all          - Build documentation and presentations"
	@echo "  html         - Build MkDocs documentation only"
	@echo "  presentations - Build all presentations"
	@echo "  clean        - Remove build artifacts"
	@echo "  help         - Show this help"

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

# Build presentations (for local use)
presentations: check-marp
	@echo "Building presentations locally..."
	@mkdir -p $(BUILDDIR)/html/presentations
	@cd .. && . .venv/bin/activate && marp docs/$(SOURCEDIR)/presentations/add_edito_service_slidedeck.md --output docs/$(BUILDDIR)/html/presentations/add_edito_service_slidedeck.html --theme docs/$(SOURCEDIR)/static/styles/edito-marp.css --allow-local-files
	@cd .. && . .venv/bin/activate && marp docs/$(SOURCEDIR)/presentations/add_edito_tutorial_slidedeck.md --output docs/$(BUILDDIR)/html/presentations/add_edito_tutorial_slidedeck.html --theme docs/$(SOURCEDIR)/static/styles/edito-marp.css --allow-local-files
	@cd .. && . .venv/bin/activate && marp docs/$(SOURCEDIR)/presentations/explore_data_slidedeck.md --output docs/$(BUILDDIR)/html/presentations/explore_data_slidedeck.html --theme docs/$(SOURCEDIR)/static/styles/edito-marp.css --allow-local-files
	@cd .. && . .venv/bin/activate && marp docs/$(SOURCEDIR)/presentations/using_datalab_slidedeck.md --output docs/$(BUILDDIR)/html/presentations/using_datalab_slidedeck.html --theme docs/$(SOURCEDIR)/static/styles/edito-marp.css --allow-local-files
	@echo "✅ Local presentations built successfully!"

# Build everything (for manual builds)
all: html presentations

# Ensure build/html directory exists
$(BUILDDIR)/html:
	@mkdir -p $@

.PHONY: help html presentations check-marp all clean

clean:
	rm -rf $(BUILDDIR)/*