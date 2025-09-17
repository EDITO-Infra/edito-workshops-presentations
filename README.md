# EDITO Technical Workshop Repository

🌊 **Welcome to the EDITO Technical Workshop Repository!**

This repository contains comprehensive resources and hands-on tutorials for contributing to the **European Digital Twin of the Ocean (EDITO)** platform. Whether you want to add tutorials, deploy services, or explore marine data, this workshop will guide you through the entire process.

## 🎯 What You'll Learn

This workshop covers four essential aspects of contributing to EDITO:

- **📚 Add Tutorials**: Create and publish interactive R/Python tutorials on the EDITO platform
- **🔧 Add Services**: Deploy containerized web applications and services to EDITO Datalab  
- **⚙️ Add Process**: Deploy computational models and data processing workflows to EDITO
- **🌊 Explore Data**: Access and analyze marine data through the EDITO Data API and STAC catalog

## 🚀 Quick Start Guide

### 1. Choose Your Path

Navigate to the section that matches your interest:

| Section | What You'll Do | Time Required | Prerequisites |
|---------|----------------|---------------|---------------|
| **[📚 Add Tutorial](#-add-tutorial)** | Create R Markdown tutorials and publish them | 30-45 min | R, GitHub account |
| **[🔧 Add Service](#-add-service)** | Dockerize applications and deploy to EDITO | 45-60 min | Docker, GitLab access |
| **[⚙️ Add Process](#-add-process)** | Deploy computational models and workflows | 45-60 min | Docker, GitLab access |
| **[🌊 Explore Data](#-explore-data)** | Access marine data via STAC API | 20-30 min | Python/R basics |

### 2. Get Started

**Clone this repository**:

   ```bash
   git clone https://github.com/EDITO-Infra/edito-workshops-presentations.git
   cd edito-workshops-presentations
   ```

**Choose your path** and navigate to the relevant section:

   ```bash
   # For tutorials
   cd add_tutorial/
   
   # For services  
   cd add_service/
   
   # For processes
   cd add_process/
   
   # For data exploration
   cd explore_data/
   ```

## 📚 Add Tutorial

**Goal**: Create and publish interactive tutorials on the EDITO platform

**What you'll learn**:

- Create R Markdown tutorials with interactive content
- Set up GitHub repositories for your tutorials
- Configure EDITO services to run your tutorials
- Submit tutorials to the official EDITO tutorial catalog

**Getting started**:

```bash
cd add_tutorial/
# Follow the step-by-step guide in add_edito_tutorial_slidedeck.md
```

**Key files**:

- `add_edito_tutorial_slidedeck.md` - Complete tutorial guide
- `my_stac_r_tutorial/` - Example tutorial project
- `docs/add_tutorial/` - Generated presentations

## 🔧 Add Service

**Goal**: Deploy containerized web applications to EDITO Datalab

**What you'll learn**:

- Dockerize R Shiny applications
- Push images to container registries
- Create Helm charts for Kubernetes deployment
- Deploy services to EDITO playground and production

**Getting started**:

```bash
cd add_service/
# Follow the step-by-step guide in add_edito_service_slidedeck.md
```

**Key files**:

- `add_edito_service_slidedeck.md` - Complete service deployment guide
- `view_parquet_service/` - Example Shiny application
- `docs/add_service/` - Generated presentations

## ⚙️ Add Process

**Goal**: Deploy computational models and data processing workflows to EDITO

**What you'll learn**:

- Identify when your application is a model (input → output transformation)
- Dockerize computational workflows and models
- Configure Helm charts for batch processing jobs
- Handle input data from online sources or personal storage
- Deploy and manage process execution on EDITO infrastructure

**Getting started**:

```bash
cd add_process/
# Follow the step-by-step guide in add_edito_process_slidedeck.md
```

**Key files**:

- `add_edito_process_slidedeck.md` - Complete process deployment guide
- `example_model/` - Example model workflow
- `docs/add_process/` - Generated presentations

## 🌊 Explore Data

**Goal**: Access and analyze marine data through EDITO's data infrastructure

**What you'll learn**:

- Navigate the EDITO STAC (SpatioTemporal Asset Catalog)
- Access data in modern formats (Zarr, Parquet, GeoParquet)
- Use Python and R to query and analyze marine datasets
- Work with ARCO (Analysis Ready Cloud Optimized) data

**Getting started**:

```bash
cd explore_data/
# Follow the step-by-step guide in explore_data_slidedeck.md
```

**Key files**:

- `explore_data_slidedeck.md` - Complete data exploration guide
- `viewparquet/` - Interactive Parquet data viewer
- `docs/explore_data/` - Generated presentations

## 📁 Repository Structure

```text
edito-workshops-presentations/
├── 📚 add_tutorial/           # Tutorial creation and publishing
│   ├── add_edito_tutorial_slidedeck.md
│   └── my_stac_r_tutorial/    # Example tutorial project
├── 🔧 add_service/            # Service deployment and containerization  
│   ├── add_edito_service_slidedeck.md
│   └── view_parquet_service/  # Example Shiny application
├── ⚙️ add_process/            # Process deployment and model workflows
│   ├── add_edito_process_slidedeck.md
│   └── example_model/         # Example model workflow
├── 🌊 explore_data/           # Data access and analysis
│   ├── explore_data_slidedeck.md
│   └── viewparquet/           # Interactive data viewer
├── 📖 docs/                   # Generated presentations (HTML/PDF)
├── 🎨 assets/                 # Shared media assets
│   ├── images/               # Screenshots and diagrams
│   └── videos/               # Tutorial demonstrations
├── 📊 data/                   # Example datasets and scripts
├── 🛠️ using_datalab/         # R package and Jupyter notebooks
│   ├── r_scripts/            # R analysis scripts
│   ├── jupyter_notebooks/    # Python/R notebooks
│   └── check_credentials.py  # Credential validation
├── 📋 DESCRIPTION            # R package metadata
├── 🔒 renv.lock             # R package lock file
├── 🐍 pyproject.toml        # Python package configuration
└── 🛠️ Makefile              # Build system for presentations
```

## 📖 Live Documentation

The complete documentation and presentations are automatically rendered and hosted at:
**[https://edito-infra.github.io/edito-workshops-presentations/](https://edito-infra.github.io/edito-workshops-presentations/)**

This includes:
- Interactive tutorials and guides for each section
- Step-by-step instructions with code examples
- Live presentations and slide decks
- Complete reference documentation

## 🛠️ Requirements

### For All Sections

- **Git** - Version control
- **Web browser** - Access to EDITO platform

### For Tutorial Creation

- **R** with RStudio
- **GitHub account** (public repository)
- **EDITO account** (beta tester access)

### For Service Deployment

- **Docker** - Containerization
- **GitLab account** - EDITO infrastructure access
- **Container registry** (GitHub Packages, Docker Hub, etc.)

### For Data Exploration

- **Python** (with packages: `pystac-client`, `xarray`, `pyarrow`)
- **R** (with packages: `rstac`, `arrow`, `sf`, `dplyr`, `ggplot2`, `terra`)

### For R Development

- **R 4.0+** with RStudio or VS Code
- **R packages** (see `DESCRIPTION` file for complete list)
- **renv** for reproducible R environments

### For Rebuilding Documentation and Presentations (Optional)

If you want to regenerate the documentation and presentations locally:

**Prerequisites:**
- **Python 3.10+** with `uv` package manager
- **Node.js** and **npm** (for Marp presentations)

**Quick build:**
```bash
# Run the automated build script
./build_docs.sh
```

**Manual build:**
```bash
# Install dependencies
uv sync

# Build everything
cd docs && make all
```

**Output:**
- Documentation: `docs/build/html/`
- Presentations: `docs/build/html/presentations/`

## 📦 R Package Setup

This repository includes an R package (`edito.workshops`) with marine data analysis functions:

**Install R dependencies:**
```r
# Install the package and its dependencies
install.packages("devtools")
devtools::install_deps()

# Or use renv for reproducible environments
renv::restore()
```

**Key R scripts:**
- `using_datalab/r_scripts/01_stac_search.R` - STAC catalog search
- `using_datalab/r_scripts/02_read_parquet.R` - Parquet data reading
- `using_datalab/r_scripts/03_personal_storage.R` - Personal storage management

**R package structure:**
- `DESCRIPTION` - R package metadata and dependencies
- `renv.lock` - Locked R package versions for reproducibility

## 🤝 Contributing

We welcome contributions to improve this workshop! Here's how you can help:

1. **Report issues** - Found a bug or unclear instruction?
2. **Suggest improvements** - Have ideas for better examples or clearer explanations?
3. **Add examples** - Created a great tutorial or service? Share it!
4. **Update documentation** - Help keep the guides current with platform changes

**Getting help**:

- 📧 **Email**: [edito-infra-dev@mercator-ocean.eu](mailto:edito-infra-dev@mercator-ocean.eu)
- 📖 **Documentation**: [EDITO Tutorials Documentation](https://pub.pages.mercator-ocean.fr/edito-infra/edito-tutorials-content/#/)
- 🌐 **Platform**: [EDITO Datalab](https://datalab.dive.edito.eu/)

## 📄 License

This workshop content is provided under an open license to support the marine data community. Please check individual files for specific licensing terms.

---

**Ready to dive in?** Choose your path above and start contributing to the European Digital Twin of the Ocean! 🌊
