# Add Process to EDITO

Learn how to deploy computational models and data processing workflows to EDITO.

> **⚠️ Important Notice**: The example process provided in this tutorial is purely demonstrative and serves as a template for learning. It may need to be adjusted, customized, or completely rewritten to meet your specific data processing needs and requirements.

## 🎯 What You'll Learn

- Identify when your application is a model (input → output transformation)
- Dockerize computational workflows and models
- Configure Helm charts for batch processing jobs
- Handle input data from online sources or personal storage
- Deploy and manage process execution on EDITO infrastructure

## 🚀 Quick Start

1. **Follow the presentation**: [Process Deployment Guide](../presentations/add_edito_process_slidedeck.html)
2. **Explore the example**: Check out `example_process/` for a complete example
3. **Start deploying**: Use the templates and guidelines provided

## 📁 Contents

- `example_process/` - **Demonstrative process template** (see detailed description below)
- `../presentations/add_edito_process_slidedeck.html` - Interactive presentation

## 🔬 Example Process Template

The `example_process/` directory contains a **demonstrative template** that shows how to create a data processing workflow on EDITO. This template follows a simple three-stage pattern:

### Process Flow
1. **Download**: Input data is downloaded from your personal S3 storage to `/data/input`
2. **Process**: Two sequential processing steps run in `/data`:
   - Data preparation (`Rscript /Scripts/01_data_preparation.R`)
   - Model analysis (`Rscript /Scripts/02_model_analysis.R`)
3. **Upload**: Results are uploaded from `/data/output` back to your personal S3 storage

### Key Features
- **Simple S3 Integration**: Downloads from and uploads to your personal storage
- **Configurable Processing**: Commands can be customized in `values.yaml`
- **Tutorial-Friendly**: Clear data flow with `/data` directory structure
- **Error Handling**: Proper timeout and logging mechanisms

### Directory Structure
```
/data/
├── input/     # Downloaded from S3
├── output/    # Generated results (uploaded to S3)
└── ...        # Processing happens here
```

### Configuration Options
- **Input Path**: Where to find your input data in S3
- **Output Path**: Where to store results in S3  
- **Processing Commands**: Customize the R scripts or commands to run
- **Docker Image**: Specify your container image

> **⚠️ Remember**: This is a template for learning purposes. You'll need to adapt the processing commands, data handling, and potentially the entire workflow structure to match your specific use case.

## 🛠️ Requirements

- **Docker** - Containerization
- **GitLab account** - EDITO infrastructure access
- **Container registry** (GitHub Packages, Docker Hub, etc.)

## 🤔 When Is My App a Process?

Your application qualifies as a **process** when it:
- Takes input data and transforms it into output data
- Performs computational analysis, prediction, or simulation
- Runs as a batch job (not interactive)
- Processes data through algorithms or mathematical operations

**Examples:**
- Machine learning models (prediction, classification)
- Statistical analysis workflows
- Simulation models
- Data processing pipelines
- Image processing algorithms

## 🔧 Core Steps

The process of adding a process to EDITO follows these key steps:

### 1. Dockerize Your Process
- Containerize your computational workflow
- Ensure all dependencies are included
- Test locally before deployment

### 2. Configure Helm Charts
- Create Kubernetes Job configurations
- Set up resource requirements
- Configure input/output data handling

### 3. Publish Your Process
- Push Docker image to container registry
- Deploy to EDITO Process Playground for testing
- Submit for production deployment

## 📊 Input Data Sources

Your process can work with data from several sources:

### Personal S3 Storage
- Download data from your personal S3 storage
- Access data through the `/data/input` directory
- Upload results back to your personal storage

### Pre-loaded Data
- Include static data in your Docker image
- Copy data files during container build
- Access data from `/data/` directory

### Generated Data
- Create sample data for demonstration
- Generate synthetic datasets for testing
- Use built-in data generation functions

## ⚙️ Kubernetes Job Configuration

The example process Helm chart demonstrates a simple three-stage workflow with these key features:

- **S3 Download Init Container** - Downloads input data from personal S3 storage
- **Two Processing Containers** - Run sequential data processing steps
- **S3 Upload Container** - Uploads results back to personal S3 storage
- **Simple Volume Mount** - All containers share `/data` directory
- **Resource limits** and proper error handling

### Key Components

1. **S3 Download Init Container** - Downloads data to `/data/input`
2. **Data Preparation Container** - Runs configurable data preparation command
3. **Model Analysis Container** - Runs configurable model analysis command  
4. **S3 Upload Container** - Uploads results from `/data/output` to S3
5. **Shared Volume** - `/data` directory shared between all containers

### Mount Points

- `/data/input` - Downloaded input data from S3
- `/data/output` - Generated results (uploaded to S3)
- `/data` - Working directory for all processing steps

### Configuration

The process is highly configurable through `values.yaml`:
- **Input/Output S3 paths** - Where to find input data and store results
- **Processing commands** - Customize the actual processing steps
- **Docker image** - Specify your container image
- **Resource requirements** - CPU and memory limits

## 📊 Input Data Handling

Your processing scripts can access input data through the `/data/input` directory:

```r
# Get input directory
input_dir <- "/data/input"

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

# Write output to /data/output
output_dir <- "/data/output"
dir.create(output_dir, showWarnings = FALSE)
write_csv(results, file.path(output_dir, "processed_results.csv"))
```

### Simple Directory Structure

The example process uses a straightforward approach:
- Input data: `/data/input`
- Processing: `/data` (working directory)
- Output: `/data/output`

## 📚 Key Files

### Example Process Template (`example_process/`)

- `Chart.yaml` - Helm chart metadata and dependencies
- `values.yaml` - Default configuration values
- `values.schema.json` - UI form schema for configuration
- `templates/` - Kubernetes resource templates
  - `job.yaml` - Main Kubernetes Job configuration
  - `pvc.yaml` - Persistent Volume Claim for data storage
  - `secret-s3.yaml` - S3 credentials secret
  - `serviceaccount.yaml` - Service account for S3 access

### Example Model (`example_model/`)

- `Dockerfile` - Container configuration with R environment
- `Scripts/` - R scripts for data processing and analysis
  - `01_data_preparation.R` - Data preprocessing script
  - `02_model_analysis.R` - Statistical analysis and visualization
- `requirements.txt` - R package dependencies

> **⚠️ Note**: The example model scripts are demonstrative. You'll need to create your own processing logic based on your specific requirements.

## 🎥 Presentation

[View the interactive presentation](../presentations/add_edito_process_slidedeck.html) to get started with deploying processes to EDITO.

## 🤝 Contributing

Found an issue or have suggestions? Please contribute to improve this workshop!

## 📖 Additional Resources

- [EDITO Datalab](https://datalab.dive.edito.eu/)
- [Process Playground](https://gitlab.mercator-ocean.fr/pub/edito-infra/process-playground)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Jobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [EDITO Process Playground](https://pub.pages.mercator-ocean.fr/edito-infra/edito-tutorials-content/#/Contribution/process-playground)

---

> **⚠️ Final Reminder**: This tutorial provides a demonstrative example process template to help you understand the concepts and structure. The actual processing logic, data handling, and workflow steps will need to be customized or completely rewritten to match your specific use case and requirements. Use this as a starting point for learning, not as a production-ready solution.
