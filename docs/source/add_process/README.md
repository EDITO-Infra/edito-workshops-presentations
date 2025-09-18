# Add Process to EDITO

Learn how to deploy computational models and data processing workflows to EDITO.

> **⚠️ Important Notice**: The example process provided in this tutorial is purely demonstrative and serves as a template for learning. It may need to be adjusted, customized, or completely rewritten to meet your specific data processing needs and requirements.

## 🎯 What You'll Learn

- Identify when your application is a model (input → output transformation)
- Dockerize computational workflows and models
- Deploy processes to EDITO using the process playground
- Configure Helm charts for batch processing jobs
- Handle input data from online sources or personal storage

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

## 📁 Tutorial examples

- `example_model/` - Complete example model workflow with R scripts
- `example_process/` - **Demonstrative process template** (Helm chart for deployment)

## 🔬 Example Model

The `example_model/` directory contains a complete R-based model that demonstrates the typical workflow:

### Model Components

- **`Dockerfile`** - Container configuration with R environment
- **`Scripts/`** - R scripts for data processing and analysis
  - `01_data_preparation.R` - Data preprocessing script
  - `02_model_analysis.R` - Statistical analysis and visualization
- **`requirements.txt`** - R package dependencies

### Model Workflow

```r
# 01_data_preparation.R
# Load and clean input data
data <- read.csv("/data/input/sample_data.csv")
processed_data <- data %>%
  filter(!is.na(value)) %>%
  mutate(processed_value = value * 2)

# 02_model_analysis.R  
# Run analysis and generate results
model <- lm(processed_value ~ category, data = processed_data)
results <- summary(model)

# Save outputs
write.csv(results, "/data/output/analysis_results.csv")
```

## 🐳 Dockerize and Push

### 1. Build Your Docker Image

```bash
cd example_model/
docker build -t your-registry/your-model:latest .
```

### 2. Push to Container Registry

```bash
# Tag for your registry
docker tag your-registry/your-model:latest your-registry.com/your-model:latest

# Push to registry
docker push your-registry.com/your-model:latest
```

**Supported Registries:**
- GitHub Packages
- Docker Hub
- GitLab Container Registry
- Any OCI-compatible registry

## 🚀 Deploy to EDITO

### 1. Clone EDITO Process Playground

```bash
git clone https://gitlab.mercator-ocean.fr/pub/edito-infra/process-playground.git
cd process-playground
```

### README!

Follow the [EDITO Process Playground README](https://gitlab.mercator-ocean.fr/pub/edito-infra/process-playground)


### Deploy Your Process

Use the process playground interface to deploy your containerized model with the Helm chart template.

## 📋 Example Process Template

The `example_process/` directory contains a complete Helm chart that demonstrates how to deploy your model as a Kubernetes job.

### Process Flow

- **Download**: Input data is downloaded from your personal S3 storage to `/data/input`
- **Process**: Two sequential processing steps run in `/data`:
  - Data preparation (`Rscript /Scripts/01_data_preparation.R`)
  - Model analysis (`Rscript /Scripts/02_model_analysis.R`)
- **Upload**: Results are uploaded from `/data/output` back to your personal S3 storage

### Key Features

- **Simple S3 Integration**: Downloads from and uploads to your personal storage
- **Configurable Processing**: Commands can be customized in `values.yaml`
- **Tutorial-Friendly**: Clear data flow with `/data` directory structure
- **Error Handling**: Proper timeout and logging mechanisms

## 🔧 Important Components

### Job YAML (`templates/job.yaml`)

The main Kubernetes Job configuration that orchestrates your process:

```yaml
# Init container downloads data
initContainers:
- name: s3-download
  command: ["aws", "s3", "sync", "s3://your-bucket/input/", "/data/input/"]

# Your processing containers run sequentially  
containers:
- name: data-prep
  command: ["Rscript", "/Scripts/01_data_preparation.R"]
- name: model-analysis  
  command: ["Rscript", "/Scripts/02_model_analysis.R"]

# Final container uploads results
- name: s3-upload
  command: ["aws", "s3", "sync", "/data/output/", "s3://your-bucket/output/"]
```

**Key Features:**
- **Init Container**: Downloads input data from S3
- **Processing Containers**: Run your model scripts sequentially
- **Upload Container**: Uploads results back to S3
- **Shared Volume**: All containers share `/data` directory

### Values Schema (`values.schema.json`)

Defines the configuration form in the EDITO playground:

```json
{
  "type": "object",
  "properties": {
    "image.repository": {
      "title": "Docker Image Repository",
      "description": "Your container registry URL"
    },
    "s3.inputPath": {
      "title": "Input S3 Path", 
      "description": "S3 path to your input data"
    },
    "s3.outputPath": {
      "title": "Output S3 Path",
      "description": "S3 path for results"
    }
  }
}
```

**Purpose:**
- **UI Form Generation**: Creates input fields in the playground
- **Validation**: Ensures required values are provided
- **Documentation**: Describes each configuration option

### Chart Metadata (`Chart.yaml`)

Helm chart information and dependencies:

```yaml
apiVersion: v2
name: example-process
description: Example data processing workflow
version: 0.1.0
dependencies:
- name: s3-secret
  version: "1.0.0"
  repository: "file://../s3-secret"
```

**Components:**
- **Chart Identity**: Name, version, description
- **Dependencies**: Required sub-charts (S3 secrets, etc.)
- **Metadata**: For chart management and discovery

### Configuration Values (`values.yaml`)

Default configuration for your process:

```yaml
# Docker image configuration
image:
  repository: "your-registry.com/your-model"
  tag: "latest"

# S3 configuration
s3:
  inputPath: "your-bucket/input/"
  outputPath: "your-bucket/output/"

# Processing commands
processing:
  dataPrep: "Rscript /Scripts/01_data_preparation.R"
  modelAnalysis: "Rscript /Scripts/02_model_analysis.R"

```

**Configuration Options:**
- **Docker Image**: Your containerized model
- **S3 Paths**: Input and output data locations
- **Processing Commands**: Customizable R/Python scripts

## 🔄 Input/Output Handling

The Kubernetes Job YAML orchestrates data flow through a simple three-stage process:

**Input Stage**: An init container downloads your data from S3 storage to `/data/input`

**Processing Stage**: Your containers run sequentially, processing data in the shared `/data` directory

**Output Stage**: A final container uploads results from `/data/output` back to your S3 storage

**Learn More:**
- [Kubernetes Jobs Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [EDITO Process Examples](https://gitlab.mercator-ocean.fr/pub/edito-infra/process-playground)


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

📄 **Presentation**: [Process Deployment Guide](../presentations/add_edito_process_slidedeck.html)