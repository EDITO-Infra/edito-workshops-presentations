---
marp: true
paginate: true
theme: edito-marp
backgroundImage: url('../static/images/editobackgrounddark.png')
backgroundSize: cover
backgroundPosition: center
footer: '![Funded by the European Union](../static/images/footer-banner.png)'
title: Using EDITO Datalab
description: 15-Minute Tutorial for Marine Researchers
class: lead
---

# 🌊 Using EDITO Datalab
## 15-Minute Tutorial for Marine Researchers

**From finding services to running analysis - everything you need to know!**

**Presented by Samuel Fooks**  
_Flanders Marine Institute (VLIZ)_

**For all the code and examples, check out the workshop [GitHub repository](https://github.com/EDITO-Infra/edito-workshops-presentations)**

---

# 🎯 What We'll Cover (15 minutes!)

✅ **Find Services** - Navigate to datalab.dive.edito.eu  
✅ **Configure & Launch** - Choose RStudio, Jupyter, or VSCode  
✅ **Run Analysis** - STAC search, Parquet reading, Zarr data  
✅ **Personal Storage** - Connect, upload, and manage your data  
✅ **Live Demos** - See it all in action!  

Perfect for researchers who want to get started quickly! 🚀

---

# 🌍 Whats in the EDITO Datalab?

**EDITO** = European Digital Twin of the Ocean

🧭 **A European infrastructure that provides:**
- Cloud computing services for marine research
- Access to curated marine datasets
- Analysis-ready data formats (Zarr, Parquet, COG)
- Personal storage for your data

🌐 **We'll look at 3 kinds of services:**
- **RStudio** - Statistical analysis and visualization
- **Jupyter** - Machine learning and data exploration  
- **VSCode** - Multi-language development

---

# 🚀 Step 1: Find Services

## Go to EDITO Datalab

**Website**: [datalab.dive.edito.eu](https://datalab.dive.edito.eu/)

### What You'll See:
- Service catalog with available options
- Resource configuration options
- Launch buttons for each service
- Creating an autolaunch link (you can use this when you create [tutorials](../add_tutorial/README.md#make-your-deployment-url))
  
---

### 🎥 **Navigating to datalab.dive.edito.eu and browsing services**

<video src="../static/videos/launchingVSCodeserviceEDITO_configuration_saveautolaunchURL.mp4" controls width="900"></video>

---

# ⚙️ Step 2: Configure & Launch

## Choose Your Service

### RStudio Service
- **Perfect for**: Statistical analysis, spatial data, R users
- **Resources**: 2-8 CPU cores, 4-16GB RAM
- **Pre-installed**: R packages for marine research

### Jupyter Service  
- **Perfect for**: Machine learning, data exploration, Python users
- **Resources**: 2-8 CPU cores, 4-16GB RAM
- **Pre-installed**: Python packages (pandas, xarray, etc.)

---

### VSCode Service
- **Perfect for**: Multi-language projects, large codebases
- **Resources**: 2-8 CPU cores, 4-16GB RAM
- **Features**: Git integration, extensions, terminal

### 🎥 **Launching VSCode Service in EDITO Datalab**

<video src="../static/videos/launchingVSCodeserviceEDITO_configuration_saveautolaunchURL.mp4" controls width="900"></video>

---

# 🐠 Step 3: Run Analysis - R Example

## STAC Search for Marine Data

```r
# Load packages
library(rstac)
library(arrow)
library(dplyr)

# Connect to EDITO STAC API
stac_endpoint <- "https://api.dive.edito.eu/data/"
collections <- stac(stac_endpoint) %>%
  rstac::collections() %>%
  get_request()

# Search for biodiversity data
biodiversity_search <- stac(stac_endpoint) %>%
  stac_search(collections = "eurobis-occurrence-data") %>%
  get_request()
```

---

### 🎥 **Running STAC search in RStudio**
*[Video: Running STAC search in RStudio]*

---

# 📊 Reading Parquet Data - R

## EUROBIS Biodiversity Data

```r
# Read biodiversity data from Parquet
parquet_url <- "https://s3.waw3-1.cloudferro.com/emodnet/biology/eurobis_occurrence_data/eurobis_occurrences_geoparquet_2024-10-01.parquet"

# Read sample data
biodiversity_data <- arrow::read_parquet(parquet_url) %>%
  head(1000)

# Filter for marine species
marine_data <- biodiversity_data %>%
  filter(grepl("fish|Fish|mollusk|Mollusk|algae|Algae", 
               scientificName, ignore.case = TRUE))

# Create visualization
ggplot(marine_sf) +
  geom_sf(aes(color = scientificName), size = 0.5) +
  labs(title = "Marine Biodiversity from EDITO Data")
```

---

### 🎥 **Reading parquet data and creating visualizations**
*[Video: Reading parquet data and creating visualizations]*

---

# 🐍 Step 3: Run Analysis - Python Example

## Jupyter Notebook Demo

```python
import requests
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

# STAC Search
stac_endpoint = "https://api.dive.edito.eu/data/"
response = requests.get(f"{stac_endpoint}collections")
collections = response.json()

# Read Parquet Data
parquet_url = "https://s3.waw3-1.cloudferro.com/emodnet/biology/eurobis_occurrence_data/eurobis_occurrences_geoparquet_2024-10-01.parquet"
df = pd.read_parquet(parquet_url)

# Zarr Data Analysis
ds = xr.open_zarr("your-zarr-url")
temperature = ds.temperature.mean(dim=['time'])
```

---

### 🎥 **Running Jupyter notebook with STAC, Parquet, and Zarr**
*[Video: Running Jupyter notebook with STAC, Parquet, and Zarr]*

---

# 💾 Step 4: Personal Storage - Connect

## Your Storage Credentials

Your personal storage credentials are automatically available in EDITO services!

### R Example
```r
# Check if credentials are available
if(Sys.getenv("AWS_ACCESS_KEY_ID") != "") {
  cat("✅ Personal storage credentials found!\n")
  cat("Storage endpoint:", Sys.getenv("AWS_S3_ENDPOINT"), "\n")
} else {
  cat("❌ No storage credentials found.\n")
}
```

---

### Python Example
```python
import boto3
import os

# Connect to EDITO's MinIO storage
s3 = boto3.client(
    "s3",
    endpoint_url='https://minio.dive.edito.eu',
    aws_access_key_id='YOUR_ACCESS_KEY_HERE',
    aws_secret_access_key='YOUR_SECRET_KEY_HERE',
    aws_session_token='YOUR_SESSION_TOKEN_HERE'
)
```

---

### 🎥 **LConnecting to personal storage and checking credentials**
*[Video: Connecting to personal storage and checking credentials]*

---

# 📁 Step 5: Upload & Download Data

## Drag & Drop Interface

### Upload Data
- Use the file browser in your service
- Drag and drop files from your local computer
- Files are automatically uploaded to your personal storage

### Download Data
- Browse your personal storage
- Download files directly to your local computer
- Share files with collaborators

---

# 🔄 Step 6: Data Processing & Transfer

## R Example - Process and Save

```r
# Process your data
processed_data <- marine_data %>%
  group_by(scientificName) %>%
  summarise(
    count = n(),
    mean_lat = mean(decimalLatitude, na.rm = TRUE),
    mean_lon = mean(decimalLongitude, na.rm = TRUE)
  )

# Save to personal storage
library(aws.s3)
aws.s3::s3write_using(
  processed_data, 
  FUN = write.csv, 
  bucket = "your-bucket-name", 
  object = "processed_marine_data.csv"
)
```

---

### 🎥 **LIVE DEMO VIDEO PLACEHOLDER**
*[Video: Processing data and saving to personal storage]*

---

# 🐍 Python Example - Process and Save

## Process and Transfer Data

```python
# Process your data
processed_data = marine_data.groupby('scientificName').agg({
    'decimalLatitude': 'mean',
    'decimalLongitude': 'mean',
    'eventDate': 'count'
}).reset_index()

# Save to personal storage
s3.put_object(
    Bucket='your-bucket-name',
    Key='processed_marine_data.csv',
    Body=processed_data.to_csv(index=False),
    ContentType='text/csv'
)

# Download from storage
response = s3.get_object(Bucket='your-bucket-name', Key='processed_marine_data.csv')
downloaded_data = pd.read_csv(response['Body'])
```

### 🎥 **LIVE DEMO VIDEO PLACEHOLDER**
*[Video: Processing data in Python and transferring to storage]*

---

# 🎯 Complete Workflow Summary

## What We've Covered

  - **Find Services** → Go to datalab.dive.edito.eu
  - **Configure & Launch** → Choose RStudio, Jupyter, or VSCode
  - **Run Analysis** → STAC search, Parquet reading, Zarr data
  - **Connect Storage** → Access your personal storage
  - **Upload/Download** → Drag & drop files
  - **Process & Transfer** → Analyze data and save results

---

# 📊 Data Formats Explained

## ARCO Data (Analysis Ready Cloud Optimized)

### STAC (SpatioTemporal Asset Catalog)
- **Purpose**: Find and discover marine datasets
- **API**: `https://api.dive.edito.eu/data/`
- **Use**: Search for available data collections

### Parquet
- **Purpose**: Efficient tabular data storage
- **Use**: Biodiversity observations, occurrence data
- **Example**: EUROBIS marine species data

### Zarr
- **Purpose**: Cloud-optimized array data
- **Use**: Oceanographic data, climate reanalyses
- **Tools**: xarray, zarr-python

---

# 🚀 Next Steps

## Try It Yourself!

1. **Go to**: [datalab.dive.edito.eu](https://datalab.dive.edito.eu/)
2. **Launch a service** (RStudio, Jupyter, or VSCode)
3. **Run the examples** from the GitHub repository
4. **Connect your storage** and try uploading data
5. **Explore more datasets** in the EDITO STAC catalog

## Resources

- **GitHub**: [Workshop Repository](https://github.com/EDITO-Infra/edito-workshops-presentations)
- **Datalab**: [datalab.dive.edito.eu](https://datalab.dive.edito.eu/)
- **Storage**: [Personal Storage](https://datalab.dive.edito.eu/account/storage)
- **Data Explorer**: [viewer.dive.edito.eu](https://viewer.dive.edito.eu/)

---

# 🆘 Support and Help

## Getting Help

- **Email**: edito-infra-dev@mercator-ocean.eu
- **Documentation**: [EDITO Tutorials](https://dive.edito.eu/training)
- **GitHub**: [Workshop Repository](https://github.com/EDITO-Infra/edito-workshops-presentations)
