#!/bin/bash

# EDITO Documentation Build Script
# This script builds both the MkDocs documentation and Marp presentations

set -e  # Exit on any error

echo "🚀 Building EDITO Documentation and Presentations..."

# Check if we're in the right directory
if [ ! -f "mkdocs.yml" ]; then
    echo "❌ Error: mkdocs.yml not found. Please run this script from the project root."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
uv sync

# Check if marp is installed
if ! command -v marp &> /dev/null; then
    echo "📦 Installing Marp CLI..."
    npm install -g @marp-team/marp-cli
fi

# Build MkDocs documentation
echo "📖 Building MkDocs documentation..."
mkdocs build --site-dir docs/build/html

# Ensure Pages doesn't run Jekyll
touch docs/build/html/.nojekyll

# Copy static files
echo "📁 Copying static files..."
cp -r docs/source/static/* docs/build/html/static/

# Build presentations
echo "🎯 Building presentations..."
mkdir -p docs/build/html/presentations

marp docs/source/presentations/add_edito_service_slidedeck.md \
    --output docs/build/html/presentations/add_edito_service_slidedeck.html \
    --theme docs/source/static/styles/edito-marp.css \
    --allow-local-files

marp docs/source/presentations/add_edito_tutorial_slidedeck.md \
    --output docs/build/html/presentations/add_edito_tutorial_slidedeck.html \
    --theme docs/source/static/styles/edito-marp.css \
    --allow-local-files

marp docs/source/presentations/explore_data_slidedeck.md \
    --output docs/build/html/presentations/explore_data_slidedeck.html \
    --theme docs/source/static/styles/edito-marp.css \
    --allow-local-files

marp docs/source/presentations/using_datalab_slidedeck.md \
    --output docs/build/html/presentations/using_datalab_slidedeck.html \
    --theme docs/source/static/styles/edito-marp.css \
    --allow-local-files

echo "✅ Build completed successfully!"
echo "📂 Output directory: docs/build/html"
echo "🌐 To preview locally, run: cd docs/build/html && python -m http.server 8000"
