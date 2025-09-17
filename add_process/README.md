# Add Process to EDITO

Learn how to deploy computational models and data processing workflows to EDITO.

## 🎯 What You'll Learn

- Identify when your application is a model (input → output transformation)
- Dockerize computational workflows and models
- Configure Helm charts for batch processing jobs
- Handle input data from online sources or personal storage
- Deploy and manage process execution on EDITO infrastructure

## 🚀 Quick Start

1. **Follow the presentation**: [Process Deployment Guide](../presentations/add_edito_process_slidedeck.html)
2. **Explore the example**: Check out `example_model/` for a complete example
3. **Start deploying**: Use the templates and guidelines provided

## 📁 Contents

- `example_model/` - Complete example model workflow
- `helm/` - Kubernetes deployment charts for EDITO
- `DEPLOYMENT.md` - Step-by-step deployment guide
- `../presentations/add_edito_process_slidedeck.html` - Interactive presentation

## 🛠️ Requirements

- **Docker** - Containerization
- **GitLab account** - EDITO infrastructure access
- **Container registry** (GitHub Packages, Docker Hub, etc.)

## 🤔 When Is My App a Model?

Your application qualifies as a **model** when it:
- Takes input data and transforms it into output data
- Performs computational analysis, prediction, or simulation
- Processes data through algorithms or mathematical operations
- Generates results that can be used for decision-making or further analysis

**Examples:**
- Machine learning models (prediction, classification)
- Statistical analysis workflows
- Simulation models
- Data processing pipelines
- Image processing algorithms

## 🔧 Core Steps

The process of adding a model to EDITO follows these key steps:

### 1. Dockerize Your Model
- Containerize your computational workflow
- Ensure all dependencies are included
- Test locally before deployment

### 2. Configure Helm Charts
- Create Kubernetes Job configurations
- Set up resource requirements
- Configure input/output data handling

### 3. Publish Your Model
- Push Docker image to container registry
- Deploy to EDITO playground for testing
- Submit for production deployment

## 📊 Input Data Sources

Your model can work with data from several sources:

### External APIs and URLs
- Download data from external services
- Access real-time data streams
- Connect to public datasets and repositories

### Pre-loaded Data
- Include static data in your Docker image
- Copy data files during container build
- Access data from `/app/data/` directory

### Generated Data
- Create sample data for demonstration
- Generate synthetic datasets for testing
- Use built-in R data generation functions

### EDITO Data API (Advanced)
- Access marine data through EDITO's data infrastructure
- Use STAC catalog for geospatial data
- Integrate with EDITO's data services

## ⚙️ Kubernetes Job Configuration

The Helm chart follows the EDITO catch prediction template with these key features:

- **Two init containers** for sequential R script execution
- **Input data** mounted from personal storage via PVC
- **Output data** written to `/Models/Predictions` (matching catch prediction pattern)
- **Automatic S3 upload** of results to personal storage
- **Resource limits** and proper error handling

### Key Components

1. **Data Preparation Container** - Runs `01_data_preparation.R`
2. **Model Analysis Container** - Runs `02_model_analysis.R`  
3. **Output Copy Container** - Uploads results to S3
4. **Input PVC** - Mounts personal storage to `/input-data`
5. **Output Volume** - Shared between containers for data passing

### Mount Points

- `/input-data` - Personal storage input data (PVC)
- `/Models/Predictions` - Output data (emptyDir, shared between containers)

## 📊 Input Data Handling

Your R scripts can access input data from personal storage through the `/input-data` directory:

```r
# Get input directory from environment
input_dir <- Sys.getenv("EDITO_INFRA_INPUT", "/input-data")

# List all data files
input_files <- list.files(input_dir, pattern = "\\.(csv|parquet)$", 
                         full.names = TRUE, recursive = TRUE)

# Process each file
for (file in input_files) {
  if (grepl("\\.csv$", file)) {
    data <- read_csv(file, show_col_types = FALSE)
  } else if (grepl("\\.parquet$", file)) {
    data <- arrow::read_parquet(file)
  }
  # ... process your data
}
```

## 📚 Key Files

- `Dockerfile` - Container configuration with R environment
- `Scripts/` - R scripts for data processing and analysis
  - `01_data_preparation.R` - Data preprocessing script
  - `02_model_analysis.R` - Statistical analysis and visualization
- `requirements.txt` - R package dependencies
- `helm/` - Kubernetes deployment charts
  - `templates/job.yaml` - Main Kubernetes Job configuration
  - `templates/pvc.yaml` - Persistent Volume Claim for input data

## 🎥 Presentation

[View the interactive presentation](../presentations/add_edito_process_slidedeck.html) to get started with deploying processes to EDITO.

## 🤝 Contributing

Found an issue or have suggestions? Please contribute to improve this workshop!

## 📖 Additional Resources

- [EDITO Datalab](https://datalab.dive.edito.eu/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Jobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [EDITO Process Playground](https://pub.pages.mercator-ocean.fr/edito-infra/edito-tutorials-content/#/Contribution/process-playground)
