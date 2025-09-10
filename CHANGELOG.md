# Changelog

All notable changes to the EDITO Workshops repository will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive package management with pyproject.toml, requirements.txt, and DESCRIPTION files
- R package structure with renv.lock for reproducible R environments
- Makefile with common development tasks
- .gitignore for Python, R, and general development files
- Setup script for easy installation
- R profile for automatic package loading

### Changed
- Simplified using_datalab structure for 15-minute tutorial focus
- Updated presentation flow to follow logical progression
- Enhanced personal storage examples with automatic credential detection
- Streamlined R scripts for STAC search, Parquet reading, and storage management

### Fixed
- Credential handling in EDITO Datalab services
- Documentation structure and navigation
- Package dependency management

## [0.1.0] - 2024-01-XX

### Added
- Initial release of EDITO Workshops repository
- Add Tutorial section with R Markdown examples
- Add Service section with Shiny application deployment
- Explore Data section with STAC API and Parquet examples
- Using Datalab section with RStudio, Jupyter, and VSCode tutorials
- Comprehensive documentation with MkDocs
- Interactive presentations with Marp
- Example datasets and analysis scripts
- Docker support for containerized applications

### Features
- **Add Tutorial**: Create and publish R Markdown tutorials
- **Add Service**: Deploy containerized web applications
- **Explore Data**: Access marine data via STAC API
- **Using Datalab**: Learn EDITO Datalab environment usage
- **Documentation**: Comprehensive guides and examples
- **Presentations**: Interactive slide decks for workshops

### Technical Details
- Python 3.10+ support
- R 4.0+ support
- Docker containerization
- MkDocs documentation
- Marp presentations
- STAC API integration
- Parquet and Zarr data support
- Personal storage management
