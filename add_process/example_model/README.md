# Example Model - R Data Processing Workflow

This is an example model that demonstrates how to deploy a two-script R workflow to EDITO using the process deployment pattern.

## Overview

The model consists of two R scripts that work together:

1. **01_data_preparation.R** - Reads input data from personal storage and prepares it for analysis
2. **02_model_analysis.R** - Performs statistical analysis and creates visualizations

## Input Data

The model handles input data in several ways:

### Option 1: External Data Sources
Download data from APIs, URLs, or external services:
```r
# In your R script
source_data <- read_csv("https://api.example.com/data.csv")
```

### Option 2: Pre-loaded Data
Include static data in your Docker image:
```dockerfile
# In Dockerfile
COPY data/ ./data/
```
Then read in R:
```r
source_data <- read_csv("/app/data/input_data.csv")
```

### Option 3: Generated Data
Create sample data for demonstration (current implementation):
```r
set.seed(42)
sample_data <- data.frame(...)
```

### Option 4: EDITO Data API
Access data through EDITO's data infrastructure:
```r
# Use EDITO data API to fetch marine data
# (requires additional setup and credentials)
```

## Output Data

The model generates several output files in the `/output-data` directory:
- `processed_data.csv` - Cleaned and processed data
- `data_summary.csv` - Summary statistics by category
- `model_results.csv` - Data with predictions and residuals
- `model_summary.csv` - Model performance metrics
- `regression_plot.png` - Scatter plot with regression line
- `residuals_plot.png` - Residuals analysis plot
- `category_comparison.png` - Box plot by category
- `preparation_metadata.json` - Metadata from data preparation
- `model_details.json` - Detailed model information

## File Structure

```
example_model/
├── Dockerfile              # Container configuration
├── requirements.txt        # R package dependencies
├── Scripts/                # R scripts
│   ├── 01_data_preparation.R
│   └── 02_model_analysis.R
├── helm/                   # Kubernetes deployment
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── job.yaml        # Main Kubernetes Job
│       ├── pvc.yaml        # Persistent Volume Claim for input
│       └── _helpers.tpl    # Helm template helpers
└── README.md
```

## Deployment

### 1. Build Docker Image

```bash
# Build the image
docker build -t your-registry/example-model:1.0.0 .

# Push to registry
docker push your-registry/example-model:1.0.0
```

### 2. Deploy with Helm

```bash
# Update values.yaml with your image repository
# Deploy to EDITO playground
helm install my-model ./helm --namespace user-yourname
```

### 3. Monitor Execution

```bash
# Check job status
kubectl get jobs -n user-yourname

# View logs
kubectl logs -f job/my-model -n user-yourname
```

## How Input Data is Used

The R scripts access input data through the `/input-data` directory:

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
  # ... process data
}
```

## Customization

To adapt this example for your own model:

1. **Modify the R scripts** in the `Scripts/` directory
2. **Update the Dockerfile** if you need additional R packages
3. **Adjust resource requirements** in `helm/values.yaml`
4. **Update the image repository** in `helm/values.yaml`

## Environment Variables

The container uses these environment variables:
- `EDITO_INFRA_INPUT` - Path to input data directory (default: `/input-data`)
- `EDITO_INFRA_OUTPUT` - Path to output data directory (default: `/output-data`)
- `USER_NAME` - EDITO username for personalization

## Troubleshooting

- **No input data**: The first script will create sample data if none is found
- **Missing packages**: Add them to the Dockerfile `RUN R -e "install.packages(...)"` line
- **Memory issues**: Increase resource limits in `helm/values.yaml`
- **File permissions**: Ensure the container has write access to `/output-data`
