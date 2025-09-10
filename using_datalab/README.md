# Using EDITO Datalab - 15 Minute Tutorial

Learn how to use EDITO Datalab for marine data analysis in just 15 minutes! This simplified guide focuses on the core workflow: **find services → configure → run analysis**.

## 🎯 What You'll Learn

- Navigate to [EDITO Datalab](https://datalab.dive.edito.eu/) and find services
- Configure RStudio, Jupyter, or VSCode services
- Search the STAC catalog for marine data
- Read Parquet files (biodiversity data)
- Work with Zarr data (oceanographic data)

## 🚀 Quick Start (15 minutes)

### Step 1: Find Services
1. Go to [datalab.dive.edito.eu](https://datalab.dive.edito.eu/)
2. Browse the service catalog
3. Choose your preferred environment:
   - **RStudio** for R analysis
   - **Jupyter** for Python notebooks
   - **VSCode** for mixed R/Python projects

### Step 2: Configure Service
- Select appropriate CPU/memory resources
- Choose your preferred environment
- Launch the service

### Step 3: Run Analysis
- Use the provided examples to get started
- Search STAC catalog for data
- Read Parquet and Zarr files
- Create visualizations

## 📁 Examples

### R Scripts
- `r/01_stac_search.R` - Search EDITO STAC catalog
- `r/02_read_parquet.R` - Read biodiversity data from Parquet
- `r/03_personal_storage.R` - Work with personal storage

### Python Workflow
- `edito_interactive_workshop.ipynb` - **NEW!** Complete modular workflow
- `python/edito_modules/` - Modular Python packages for data processing
- `python/requirements.txt` - Python dependencies

### Legacy Python Scripts
- `python/01_get_stac_collections.py` - Get STAC collections (interactive)
- `python/02_search_stac_assets.py` - Search for data assets (interactive)
- `python/03_get_zarr_to_df.py` - Process raster data (interactive)
- `python/04_get_parquet_data.py` - Process parquet data (interactive)
- `python/05_combine_and_save.py` - Combine and save data (interactive)

## 🛠️ Services Available

### RStudio Service
Perfect for:
- Statistical analysis
- Data visualization
- R-based marine research

**Example**: Run `01_stac_search.R` to search for marine data

### Jupyter Service
Perfect for:
- Machine learning
- Data exploration
- Python-based analysis

**Example**: Open `edito_interactive_workshop.ipynb` for a complete modular workflow

### VSCode Service
Perfect for:
- Mixed R/Python projects
- Large codebases
- Collaborative development

## 📊 Data Formats

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

## 🎥 Video Examples

The tutorial includes video demonstrations of:
- RStudio service configuration and usage
- Jupyter service setup and analysis
- VSCode service for mixed R/Python projects

## 🚀 Next Steps

1. **Try the examples**: Run the provided R scripts and Jupyter notebook
2. **Explore more data**: Use STAC search to find additional datasets
3. **Save your work**: Use personal storage to persist your results
4. **Share your analysis**: Export and share your findings

## 📖 Additional Resources

- [EDITO Datalab](https://datalab.dive.edito.eu/)
- [EDITO Data API](https://data.dive.edito.eu/)
- [STAC Specification](https://stacspec.org/)
- [Personal Storage](https://datalab.dive.edito.eu/account/storage)

## 🤝 Contributing

Found an issue or have suggestions? Please contribute to improve this workshop!

---

**Ready to start?** Go to [datalab.dive.edito.eu](https://datalab.dive.edito.eu/) and launch your first service! 🌊🐠