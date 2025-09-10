---
marp: true
paginate: true
theme: edito-marp
backgroundImage: url('../static/images/editobackgrounddark.png')
backgroundSize: cover
backgroundPosition: center
footer: '![Funded by the European Union](../static/images/footer-banner.png)'
title: Using EDITO Datalab
description: A Complete Guide for Marine Researchers
class: lead
---

# 🌊 Using EDITO Datalab

## A Complete Guide for Marine Researchers

From RStudio to Jupyter to VSCode - Everything you need to know

**Presented by Samuel Fooks**  
_Flanders Marine Institute (VLIZ)_

**For all the PDFs and code, check out the workshop [GitHub repository](https://github.com/EDITO-Infra/edito-workshops-presentations)**

---

# 🎯 What We'll Cover

✅ **RStudio Service** - Statistical analysis and visualization  
✅ **Jupyter Service** - Machine learning and data exploration  
✅ **VSCode Service** - Larger projects and multi-language development  
✅ **Personal Storage** - Secure, persistent data management  
✅ **ARCO Data** - Analysis Ready Cloud Optimized formats  
✅ **Marine Data Examples** - Real-world applications  

Perfect for researchers with limited cloud/digital systems knowledge!

---

# 🌍 What is EDITO Datalab?

**EDITO** = European Digital Twin of the Ocean

🧭 **A European infrastructure to:**
- Integrate marine data, models, and services
- Support marine policy (e.g. the Green Deal)
- Help connect EU/national initiatives and citizen science

🌐 **Offers:**
- Open API access to curated datasets
- Analysis-ready formats (Zarr, Parquet, COG)
- Tools to publish, process, and visualize ocean data

---

# 🌊 Why This Matters for Marine Research

**Large datasets**: Handle millions of marine records efficiently  
**Environmental data**: Access oceanographic data for analysis  
**Collaboration**: Share code and data with research teams  
**Reproducibility**: Version control and documented workflows  
**Scalability**: Process data that won't fit on your local computer  

> Perfect for marine researchers who know R and some modeling but are new to cloud-optimized data!

---

# 🖥️ EDITO Datalab Services

## Three Main Services for Different Needs

**RStudio Service**  
- Perfect for statistical analysis and visualization
- Familiar R environment
- Great for spatial data analysis

**Jupyter Service**  
- Ideal for machine learning and data exploration
- Interactive notebooks
- Python, R, and other languages

**VSCode Service**  
- Great for larger, multi-language projects
- Full development environment
- Git integration and collaboration

---

# 🚀 Getting Started: RStudio Service

## Launch RStudio

1. Go to [EDITO Datalab](https://datalab.dive.edito.eu/)
2. Select "RStudio" from the service catalog
3. Configure resources (CPU, memory) as needed
4. Launch the service

## What You Get

- Full RStudio environment in your browser
- Pre-installed packages for marine research
- Access to EDITO's data collections
- Personal storage integration

---

# 📊 Working with ARCO Data

## What is ARCO Data?

**ARCO** = Analysis Ready Cloud Optimized

- **Parquet**: Columnar format, perfect for tabular data
- **Zarr**: Chunked arrays, ideal for raster data  
- **COG**: Cloud Optimized GeoTIFF for imagery

## Why ARCO?

✅ **Much faster** than traditional CSV files  
✅ **Smaller file sizes** - more data in less space  
✅ **Cloud-native** - designed for modern computing  
✅ **Perfect for large datasets** - like marine biodiversity data  

---

# 🐠 Marine Biodiversity Example: R

```r
# Load required packages
library(arrow)      # For reading Parquet files
library(sf)         # For spatial data
library(dplyr)      # For data manipulation
library(ggplot2)    # For plotting

# Read marine biodiversity data from EDITO
parquet_url <- "https://s3...biodiversity_data.parquet"
marine_data <- arrow::read_parquet(parquet_url)

# Filter for marine species
marine_data <- marine_data %>%
  filter(grepl("fish|Fish|mollusk|Mollusk|algae|Algae", scientificName, ignore.case = TRUE))

# Create spatial plot
ggplot(marine_sf) +
  geom_sf(aes(color = scientificName)) +
  labs(title = "Marine Biodiversity from EDITO Data")
```

---

# 🐍 Jupyter Service for Python

## Launch Jupyter

1. Go to [EDITO Datalab](https://datalab.dive.edito.eu/)
2. Select "Jupyter" from the service catalog
3. Choose Python environment
4. Launch the service

## Perfect for Machine Learning

- Interactive notebooks
- Data exploration and visualization
- Machine learning for habitat modeling
- Integration with R and other languages

---

# 🐠 Marine Biodiversity Example: Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# Load marine biodiversity data
marine_data = pd.read_parquet("biodiversity_data.parquet")

# Create habitat suitability model
features = ['latitude', 'longitude', 'depth', 'temperature']
X = marine_data[features]
y = marine_data['habitat_suitability']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Visualize results
plt.scatter(marine_data['longitude'], marine_data['latitude'], 
           c=marine_data['habitat_suitability'], cmap='viridis')
plt.title('Marine Habitat Suitability')
```

---

# 🔧 VSCode for Larger Projects

## When to Use VSCode

- **Multi-language projects** (R + Python)
- **Large codebases** with many files
- **Git integration** and version control
- **Collaborative development**
- **Complex data processing pipelines**

## Project Organization

```
marine_research_project/
├── data/raw/           # Original marine data
├── data/processed/     # Cleaned data
├── scripts/analysis/   # Analysis code
├── notebooks/          # Jupyter notebooks
└── outputs/figures/    # Generated plots
```

---

# 💾 Personal Storage Integration

## Access Your Personal Storage

Your personal storage credentials are automatically available in EDITO services!

**Storage URL**: [https://datalab.dive.edito.eu/account/storage](https://datalab.dive.edito.eu/account/storage)

## R Example
```r
# Your credentials are automatically available
library(aws.s3)
aws.s3::s3write_using(marine_data, FUN = write.csv, 
                     bucket = "your-bucket", 
                     object = "marine_data.csv")
```

## Python Example
```python
import boto3
s3 = boto3.client('s3', endpoint_url=f"https://{os.getenv('AWS_S3_ENDPOINT')}")
s3.put_object(Bucket='your-bucket', Key='marine_data.csv', 
              Body=marine_data.to_csv(index=False))
```

---

# 🌊 Accessing Environmental Data

## Perfect for Marine Habitat Modeling

**Available Data:**
- Sea surface temperature
- Salinity
- Currents and ocean circulation
- Sea level
- Bathymetry
- Weather data

**How to Access:**
- Use EDITO STAC API
- Browse data catalog
- Download ARCO format data
- Integrate with your marine data

---

# 🔍 EDITO Data Explorer

## Browse Available Data

**Data Explorer**: [https://datalab.dive.edito.eu/data-explorer](https://datalab.dive.edito.eu/data-explorer)

**STAC Viewer**: [https://viewer.dive.edito.eu/](https://viewer.dive.edito.eu/)

## Example: 38 Million Marine Records

Explore the EUROBIS database with 38 million occurrence records:
- Filter by species, location, time
- Download in Parquet format
- Perfect for marine biodiversity research

---

# 📋 Best Practices for Marine Research

## Data Organization
1. **Use consistent naming conventions**
2. **Organize data in logical folders**
3. **Include metadata files**
4. **Document your data processing steps**

## Code Management
1. **Use version control (Git)**
2. **Write clear comments**
3. **Test your code regularly**
4. **Save intermediate results**

## Collaboration
1. **Share code via GitHub/GitLab**
2. **Use personal storage for data sharing**
3. **Document your methods**
4. **Make your work reproducible**

---

# 🛠️ Troubleshooting Common Issues

## RStudio Issues
- **Package installation**: Use `install.packages()` in console
- **Memory issues**: Increase memory in service configuration
- **Data loading**: Use `arrow::read_parquet()` for large files

## Jupyter Issues
- **Kernel problems**: Restart the kernel
- **Package installation**: Use `!pip install package_name`
- **Memory issues**: Process data in chunks

## VSCode Issues
- **Terminal access**: Use Ctrl+` to open terminal
- **Git integration**: Use Source Control panel
- **Extensions**: Install from Extensions marketplace

---

# 🚀 Next Steps

## Explore More
1. **Try different services**: RStudio, Jupyter, VSCode
2. **Access more data**: Explore EDITO's data collections
3. **Learn about data sharing**: Use personal storage effectively
4. **Join the community**: Connect with other researchers

## Resources
- [EDITO Datalab](https://datalab.dive.edito.eu/)
- [Personal Storage](https://datalab.dive.edito.eu/account/storage)
- [EDITO Tutorials](https://dive.edito.eu/training)
- [Data API Documentation](https://pub.pages.mercator-ocean.fr/edito-infra/edito-tutorials-content/#/interactWithTheDataAPI)

---

# 🐠 Marine Research Workflow Example

## Complete Workflow

1. **Launch RStudio** on EDITO Datalab
2. **Load marine biodiversity data** from your personal storage
3. **Access environmental data** from EDITO's data lake
4. **Analyze species distributions** using R spatial packages
5. **Create habitat models** using machine learning
6. **Visualize results** with interactive maps
7. **Save outputs** to personal storage
8. **Share with collaborators** via Git and storage

## All in the Cloud! ☁️

---

# 💡 Tips for Marine Researchers

## Getting Started
- **Start with RStudio** if you're familiar with R
- **Try Jupyter** for machine learning and exploration
- **Use VSCode** for larger, multi-language projects

## Data Management
- **Use Parquet format** for large datasets
- **Organize your data** in clear folder structures
- **Include metadata** describing your data
- **Save regularly** to personal storage

## Collaboration
- **Use Git** for version control
- **Share code** via GitHub/GitLab
- **Document everything** for reproducibility

---

# 🆘 Support and Help

## Getting Help
- **Email**: edito-infra-dev@mercator-ocean.eu
- **Documentation**: [EDITO Tutorials](https://dive.edito.eu/training)
- **GitHub**: [Workshop Repository](https://github.com/EDITO-Infra/edito-workshops-presentations)

## Available Thursday and Friday
- **Live demo** and Q&A session
- **Detailed discussions** about specific needs
- **Hands-on help** with your projects

---

# 🙌 Summary

## What You Can Now Do

✅ **Launch cloud services** (RStudio, Jupyter, VSCode)  
✅ **Access ARCO data** efficiently  
✅ **Use personal storage** for data persistence  
✅ **Analyze marine biodiversity data** with modern tools  
✅ **Create habitat models** using machine learning  
✅ **Collaborate effectively** with research teams  

## Ready to Explore!

**Start with the service that matches your current workflow, then explore others as your needs grow.**

---

# 🌊 Happy Analyzing!

**EDITO Datalab provides powerful tools for marine research:**

- **RStudio**: Perfect for statistical analysis and visualization
- **Jupyter**: Ideal for machine learning and data exploration  
- **VSCode**: Great for larger, multi-language projects
- **Personal Storage**: Secure, persistent data management
- **ARCO Data**: Fast, efficient access to large datasets

**The cloud-based approach means you can work with datasets that would be impossible to handle on your local computer.**

🐠🌊 **Ready to dive in!**

---

# Questions?

**Available for detailed discussions:**
- Thursday: Live demo and Q&A
- Friday: Hands-on help with your projects

**Contact:**
- Email: edito-infra-dev@mercator-ocean.eu
- GitHub: [Workshop Repository](https://github.com/EDITO-Infra/edito-workshops-presentations)

**Resources:**
- [EDITO Datalab](https://datalab.dive.edito.eu/)
- [Personal Storage](https://datalab.dive.edito.eu/account/storage)
- [EDITO Tutorials](https://dive.edito.eu/training)

---

*This tutorial was created for the EDITO Datalab workshop. Perfect for marine researchers getting started with cloud computing and modern data formats.*
