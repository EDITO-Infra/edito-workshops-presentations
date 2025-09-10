# VSCode Service on EDITO Datalab

## Overview

VSCode (Visual Studio Code) is a powerful, lightweight code editor that's perfect for larger fish tracking projects. On EDITO Datalab, you get a full VSCode environment with extensions, terminal access, and integrated development tools.

## Why Use VSCode for Fish Tracking Research?

- **Multi-language support**: Work with R, Python, and other languages in one environment
- **Integrated terminal**: Run commands and scripts directly
- **Git integration**: Version control your research code
- **Extensions**: Install specialized tools for data science and marine research
- **File management**: Organize large projects with multiple files and folders
- **Debugging**: Step through your code to find and fix issues

## Getting Started

1. **Launch VSCode Service**:
   - Go to [EDITO Datalab](https://datalab.dive.edito.eu/)
   - Select "VSCode" from the service catalog
   - Configure resources (CPU, memory) as needed
   - Launch the service

2. **First Steps**:
   - Open the integrated terminal (Ctrl+` or Terminal > New Terminal)
   - Clone your research repository or create a new project
   - Install required packages and dependencies

## Example Project Structure

```
fish_tracking_project/
├── data/
│   ├── raw/                 # Original tracking data
│   ├── processed/           # Cleaned and processed data
│   └── environmental/       # Environmental data from EDITO
├── scripts/
│   ├── data_processing/     # Data cleaning and preparation
│   ├── analysis/           # Statistical analysis
│   └── visualization/      # Plotting and mapping
├── notebooks/
│   ├── exploration.ipynb   # Data exploration
│   └── analysis.ipynb      # Main analysis
├── outputs/
│   ├── figures/            # Generated plots
│   ├── tables/             # Results tables
│   └── reports/            # Generated reports
├── config/
│   └── settings.yaml       # Project configuration
└── README.md               # Project documentation
```

## Key Features for Fish Tracking

### 1. Multi-Language Support
- **R**: For statistical analysis and spatial data
- **Python**: For machine learning and data processing
- **Markdown**: For documentation and reports
- **YAML/JSON**: For configuration files

### 2. Integrated Terminal
```bash
# Install R packages
R -e "install.packages(c('sf', 'dplyr', 'ggplot2', 'arrow'))"

# Install Python packages
pip install pandas numpy matplotlib seaborn boto3

# Run R scripts
Rscript scripts/analysis/fish_movement_analysis.R

# Run Python scripts
python scripts/processing/clean_tracking_data.py
```

### 3. Git Integration
- Version control your research code
- Collaborate with team members
- Track changes and maintain project history
- Push to GitHub/GitLab for sharing

### 4. Extensions for Marine Research
- **R Extension**: Syntax highlighting and debugging for R
- **Python Extension**: IntelliSense and debugging for Python
- **GitLens**: Enhanced Git capabilities
- **Markdown All in One**: Better markdown editing
- **YAML**: Configuration file support
- **Docker**: Container management

## Example Workflow

### 1. Data Processing
```r
# scripts/processing/load_edito_data.R
library(arrow)
library(sf)
library(dplyr)

# Load fish tracking data from EDITO
fish_data <- arrow::read_parquet("data/raw/fish_tracking.parquet")

# Process and clean data
processed_data <- fish_data %>%
  filter(!is.na(latitude), !is.na(longitude)) %>%
  mutate(
    date = as.Date(timestamp),
    month = format(date, "%m"),
    season = case_when(
      month %in% c("12", "01", "02") ~ "Winter",
      month %in% c("03", "04", "05") ~ "Spring",
      month %in% c("06", "07", "08") ~ "Summer",
      month %in% c("09", "10", "11") ~ "Autumn"
    )
  )

# Save processed data
arrow::write_parquet(processed_data, "data/processed/fish_tracking_clean.parquet")
```

### 2. Analysis
```python
# scripts/analysis/movement_analysis.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load processed data
df = pd.read_parquet('data/processed/fish_tracking_clean.parquet')

# Calculate movement metrics
df['distance'] = df.groupby('fish_id').apply(
    lambda x: np.sqrt(np.diff(x['longitude'])**2 + np.diff(x['latitude'])**2)
).values

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
# ... plotting code ...

plt.savefig('outputs/figures/movement_analysis.png')
```

### 3. Documentation
```markdown
# Fish Tracking Analysis Report

## Overview
This project analyzes fish movement patterns using data from EDITO.

## Methods
- Data source: EDITO Data Lake
- Processing: R and Python
- Analysis: Statistical modeling and visualization

## Results
[Generated plots and tables]

## Conclusions
[Key findings and implications]
```

## Personal Storage Integration

VSCode integrates seamlessly with EDITO's personal storage:

```python
# Access your personal storage
import boto3
import os

s3 = boto3.client(
    's3',
    endpoint_url=f"https://{os.getenv('AWS_S3_ENDPOINT')}",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

# Save results to personal storage
s3.upload_file('outputs/figures/movement_analysis.png', 
               'your-bucket', 'fish_tracking/figures/movement_analysis.png')
```

## Tips for Fish Tracking Researchers

1. **Organize your project**: Use clear folder structure and naming conventions
2. **Document everything**: Write clear comments and README files
3. **Use version control**: Track changes and collaborate effectively
4. **Test your code**: Use the integrated terminal to test scripts
5. **Save regularly**: Use personal storage for data persistence
6. **Install useful extensions**: Customize VSCode for your workflow

## Next Steps

1. Try the RStudio service for R-focused analysis
2. Use Jupyter notebooks for interactive exploration
3. Explore EDITO's data collections
4. Learn about data sharing and collaboration
5. Check out the other tutorials in this series

## Resources

- [VSCode Documentation](https://code.visualstudio.com/docs)
- [EDITO Datalab](https://datalab.dive.edito.eu/)
- [Personal Storage Guide](https://datalab.dive.edito.eu/account/storage)
- [EDITO Tutorials](https://dive.edito.eu/training)
