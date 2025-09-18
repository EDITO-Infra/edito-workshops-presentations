# Using EDITO Datalab - Complete Tutorial

Learn how to use EDITO Datalab for marine data analysis with this comprehensive guide! From finding services to advanced data processing and storage, this tutorial covers everything you need to know.

## 🎯 What You'll Learn

- Navigate to [EDITO Datalab](https://datalab.dive.edito.eu/) and find services
- Configure RStudio, Jupyter, or VSCode services
- Search the STAC catalog for marine data collections
- Process Parquet files (biodiversity data) and Zarr data (oceanographic data)
- Combine different data types spatially
- Save and manage data using personal storage
- Work with both R and Python environments

## 🚀 Quick Start (15 minutes)

### Find Services
- Go to [datalab.dive.edito.eu](https://datalab.dive.edito.eu/)
- Browse the service catalog
- Choose your preferred environment:
  - **RStudio** for R analysis and visualization
  - **Jupyter** for Python notebooks and machine learning
  - **VSCode** for mixed R/Python projects and development

### Configure Service
- Select appropriate CPU/memory resources (2-8 cores, 4-16GB RAM)
- Choose your preferred environment
- Launch the service (credentials are automatically configured)

### Run Analysis
- Use the provided scripts to get started
- Search STAC catalog for data collections
- Process Parquet and Zarr files
- Combine and analyze marine data

## 📁 Complete Workflow Scripts

### R Scripts (Ready to Run)
- **`r/01_stac_search.R`** - Search EDITO STAC catalog for marine data collections
  - Connects to STAC API and lists available collections
  - Filters for biodiversity-related data
  - Shows data access URLs and formats
- **`r/02_read_parquet.R`** - Read and process biodiversity data from Parquet files
  - Direct access to EUROBIS marine species data
  - Data filtering and basic analysis
- **`r/03_personal_storage.R`** - Complete personal storage workflow
  - Connect to EDITO storage (credentials auto-configured)
  - Upload/download data to/from personal storage
  - Process and save marine data in multiple formats

### Python Scripts (Interactive Workflow)
- **`python/01_get_stac_collections.py`** - Get and explore STAC collections
  - Interactive collection discovery
  - Search functionality for specific data types
  - Saves collections metadata for next steps
- **`python/02_search_stac_assets.py`** - Search for specific data assets
  - Filter collections by keywords (biodiversity, ocean, etc.)
  - Find Parquet and Zarr data assets
  - Interactive asset selection
- **`python/03_get_zarr_to_df.py`** - Process oceanographic Zarr data
  - Convert Zarr arrays to DataFrames
  - Handle large datasets with smart sampling
  - Spatial data processing
- **`python/04_get_parquet_data.py`** - Process biodiversity Parquet data
  - Read Parquet files from S3
  - Data exploration and filtering
  - Schema analysis and sample extraction
- **`python/05_combine_and_save.py`** - Complete data combination workflow
  - Select and combine Parquet + Zarr datasets
  - Spatial data integration
  - Save to local files and personal storage
  - Metadata generation and tracking

### Additional Tools
- **`python/check_credentials.py`** - Verify storage credentials
- **`python/run_full_demo.py`** - Run complete workflow automatically

## 🛠️ Services Available

### RStudio Service
**Perfect for:**
- Statistical analysis and spatial data processing
- Data visualization and reporting
- R-based marine research workflows
- Quick data exploration and analysis

**Getting Started:**
- Launch RStudio service in EDITO Datalab
- Run `r/01_stac_search.R` to discover data collections
- Use `r/02_read_parquet.R` to process biodiversity data
- Try `r/03_personal_storage.R` for data management

### Jupyter Service
**Perfect for:**
- Machine learning and data science
- Interactive data exploration
- Python-based analysis and visualization
- Notebook-based research workflows

**Getting Started:**
- Launch Jupyter service in EDITO Datalab
- Run the Python scripts in sequence:
  - `python/01_get_stac_collections.py`
  - `python/02_search_stac_assets.py`
  - `python/03_get_zarr_to_df.py`
  - `python/04_get_parquet_data.py`
  - `python/05_combine_and_save.py`

### VSCode Service
**Perfect for:**
- Mixed R/Python projects
- Large codebases and development
- Collaborative research
- Advanced data processing workflows

**Getting Started:**
- Launch VSCode service in EDITO Datalab
- Open the `using_datalab` folder
- Run either R or Python scripts as needed
- Use integrated terminal for command-line tools

## 📊 Data Formats & Sources

### STAC (SpatioTemporal Asset Catalog)
- **Purpose**: Find and discover marine datasets
- **API**: `https://api.dive.edito.eu/data/`
- **Use**: Search for available data collections
- **Scripts**: `01_stac_search.R`, `01_get_stac_collections.py`

### Parquet (Biodiversity Data)
- **Purpose**: Efficient tabular data storage for occurrence records
- **Use**: Marine species observations, biodiversity data
- **Example**: EUROBIS marine species occurrence data
- **Scripts**: `02_read_parquet.R`, `04_get_parquet_data.py`
- **Features**: Fast querying, columnar storage, schema evolution

### Zarr (Oceanographic Data)
- **Purpose**: Cloud-optimized array data for large datasets
- **Use**: Oceanographic data, climate reanalyses, satellite data
- **Tools**: xarray, zarr-python
- **Scripts**: `03_get_zarr_to_df.py`
- **Features**: Chunked storage, parallel access, compression

### Personal Storage (MyFiles)
- **Purpose**: Your personal cloud storage for data and results
- **Access**: Automatically configured in EDITO services
- **Use**: Save processed data, share results, backup analysis
- **Scripts**: `03_personal_storage.R`, `05_combine_and_save.py`
- **Formats**: CSV, Parquet, JSON, any file type

## 🎥 Video Examples

The tutorial includes video demonstrations of:
- **Service Configuration**: RStudio, Jupyter, and VSCode setup
- **STAC Search**: Finding and exploring marine data collections
- **Data Processing**: Working with Parquet and Zarr data
- **Personal Storage**: Uploading and managing data in MyFiles
- **Complete Workflow**: End-to-end data analysis pipeline

## 🚀 Getting Started

### Quick Start (15 minutes)
- **Launch a service** at [datalab.dive.edito.eu](https://datalab.dive.edito.eu/)
- **Run one script** to get familiar with the workflow
- **Explore the data** and see what's available

### Complete Workflow (1 hour)
- **Start with R**: Run `r/01_stac_search.R` to discover data
- **Process data**: Use `r/02_read_parquet.R` for biodiversity data
- **Manage storage**: Try `r/03_personal_storage.R` for data management
- **Advanced Python**: Run the Python scripts in sequence for full workflow

### Automated Demo
- **Run the complete demo**: `python/run_full_demo.py`
- **Watch the process**: See all steps automated
- **Examine results**: Check the output files and storage

## 📖 Additional Resources

- **EDITO Datalab**: [datalab.dive.edito.eu](https://datalab.dive.edito.eu/)
- **EDITO Data API**: [data.dive.edito.eu](https://data.dive.edito.eu/)
- **STAC Specification**: [stacspec.org](https://stacspec.org/)
- **Personal Storage**: [datalab.dive.edito.eu/account/storage](https://datalab.dive.edito.eu/account/storage)
- **Workshop Repository**: [GitHub](https://github.com/EDITO-Infra/edito-workshops-presentations)

## 🤝 Contributing

Found an issue or have suggestions? Please contribute to improve this workshop!

---

**Ready to start?** Go to [datalab.dive.edito.eu](https://datalab.dive.edito.eu/) and launch your first service! 🌊🐠

---

📄 **Presentation**: [Using the Datalab](../docs/presentations/using_datalab_slidedeck.pdf)