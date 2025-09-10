# EDITO Technical Workshop Repository

🌊 **Welcome to the EDITO Technical Workshop Repository!**

This repository contains comprehensive resources and hands-on tutorials for contributing to the **European Digital Twin of the Ocean (EDITO)** platform. Whether you want to add tutorials, deploy services, or explore marine data, this workshop will guide you through the entire process.

## 🎯 What You'll Learn

This workshop covers four essential aspects of contributing to EDITO:

- **📚 Add Tutorials**: Create and publish interactive R/Python tutorials on the EDITO platform
- **🔧 Add Services**: Deploy containerized web applications and services to EDITO Datalab  
- **🌊 Explore Data**: Access and analyze marine data through the EDITO Data API and STAC catalog
- **🖥️ Using Datalab**: Learn to use the EDITO Datalab environment effectively

## 🚀 Quick Start Guide

### 1. Choose Your Path

Navigate to the section that matches your interest:

| Section | What You'll Do | Time Required | Prerequisites |
|---------|----------------|---------------|---------------|
| **[📚 Add Tutorial](add_tutorial/README.md)** | Create R Markdown tutorials and publish them | 30-45 min | R, GitHub account |
| **[🔧 Add Service](add_service/README.md)** | Dockerize applications and deploy to EDITO | 45-60 min | Docker, GitLab access |
| **[🌊 Explore Data](explore_data/README.md)** | Access marine data via STAC API | 20-30 min | Python/R basics |
| **[🖥️ Using Datalab](using_datalab/README.md)** | Learn EDITO Datalab environment | 15-30 min | Basic programming |

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
   
# For data exploration
cd explore_data/

# For datalab usage
cd using_datalab/
```

## 📁 Repository Structure

```text
edito-workshops-presentations/
├── 📚 add_tutorial/           # Tutorial creation and publishing
│   ├── README.md
│   ├── my_stac_r_tutorial/    # Example tutorial project
│   └── presentation.html      # Interactive presentation
├── 🔧 add_service/            # Service deployment and containerization  
│   ├── README.md
│   ├── view_parquet_service/  # Example Shiny application
│   └── presentation.html      # Interactive presentation
├── 🌊 explore_data/           # Data access and analysis
│   ├── README.md
│   ├── viewparquet/           # Interactive data viewer
│   └── presentation.html      # Interactive presentation
├── 🖥️ using_datalab/          # EDITO Datalab usage
│   ├── README.md
│   ├── python_scripts/        # Python examples
│   ├── r_scripts/             # R examples
│   └── presentation.html      # Interactive presentation
├── 📖 docs/                   # Documentation (this site)
├── 🎨 assets/                 # Shared media assets
│   ├── images/               # Screenshots and diagrams
│   └── videos/               # Tutorial demonstrations
└── 📊 data/                   # Example datasets and scripts
```

## 🎥 Live Presentations

All presentations are available as interactive HTML slides:

- **[Add Tutorial Presentation](presentations/add_edito_tutorial_slidedeck.html)** - Complete tutorial creation guide
- **[Add Service Presentation](presentations/add_edito_service_slidedeck.html)** - Service deployment walkthrough  
- **[Explore Data Presentation](presentations/explore_data_slidedeck.html)** - Data access and analysis
- **[Using Datalab Presentation](presentations/using_datalab_slidedeck.html)** - Datalab environment guide

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
- **R** (with packages: `rstac`, `arrow`, `sf`)

### For Datalab Usage

- **EDITO Datalab account**
- **Basic programming knowledge** (Python or R)

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
