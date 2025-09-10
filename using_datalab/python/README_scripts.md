# EDITO Datalab Demo Scripts

This directory contains a modular set of Python scripts that demonstrate the complete EDITO Datalab workflow. The scripts are designed to be run individually or as a complete pipeline.

## 🚀 Quick Start

### Run Complete Workflow
```bash
python run_full_demo.py
```

### Run Individual Scripts
```bash
python 01_get_stac_collections.py
python 02_search_stac_assets.py
python 03_get_zarr_to_df.py
python 04_get_parquet_data.py
python 05_combine_and_save.py
```

## 📋 Script Overview

### 1. `01_get_stac_collections.py`
**Purpose**: Connect to EDITO STAC API and retrieve available collections
- Connects to `https://api.dive.edito.eu/data/`
- Lists all available data collections
- Saves collections to `stac_collections.json`

**Output**: `stac_collections.json`

### 2. `02_search_stac_assets.py`
**Purpose**: Search STAC collections for parquet and raster (NetCDF/Zarr) assets
- Loads collections from previous step
- Searches biodiversity collections for different data types
- Categorizes items by asset type
- Saves results to separate JSON files

**Outputs**: 
- `stac_parquet_items.json`
- `stac_raster_items.json`

### 3. `03_get_zarr_to_df.py`
**Purpose**: Process raster data and convert to DataFrame/CSV
- Loads raster items from STAC search
- Opens NetCDF/Zarr files using xarray
- Creates spatial subsets of the data
- Converts to pandas DataFrame and saves as CSV

**Output**: `raster_data.csv`

### 4. `04_get_parquet_data.py`
**Purpose**: Process parquet data from STAC search
- Loads parquet items from STAC search
- Reads parquet files using PyArrow
- Handles S3 URLs with s3fs
- Creates sample datasets and saves as CSV

**Output**: `parquet_data.csv`

### 5. `05_combine_and_save.py`
**Purpose**: Combine datasets and save to storage
- Loads processed raster and parquet data
- Standardizes data formats
- Combines into unified dataset
- Saves locally and to personal storage

**Outputs**:
- `combined_marine_data.csv` (local)
- Files uploaded to personal storage

### 6. `run_full_demo.py`
**Purpose**: Master script that runs all steps in sequence
- Checks dependencies
- Runs each script in order
- Provides progress tracking
- Shows summary of results

## 📦 Dependencies

Install required packages:
```bash
pip install requests pandas numpy pyarrow xarray boto3 fsspec s3fs
```

## 🔧 Configuration

### Environment Variables (for personal storage)
When running in EDITO Datalab, these are automatically available:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`
- `AWS_S3_ENDPOINT`
- `AWS_DEFAULT_REGION`

### Customization
- Modify `subset_size` parameters to control data sample sizes
- Adjust `max_items` to process more/fewer items
- Change output file names in each script
- Update bucket names in storage scripts

## 📊 Data Flow

```
STAC API → Collections → Search Assets → Process Raster → Process Parquet → Combine → Save
    ↓           ↓            ↓              ↓              ↓           ↓        ↓
Collections  Parquet     Raster DF     Parquet DF    Combined    Local    Storage
   JSON        JSON        CSV           CSV          CSV        File     Upload
```

## 🎯 Use Cases

### Individual Scripts
- **Research**: Use specific scripts for targeted data processing
- **Debugging**: Run scripts individually to identify issues
- **Customization**: Modify individual scripts for specific needs

### Complete Pipeline
- **Tutorials**: Demonstrate full EDITO Datalab workflow
- **Automation**: Run complete data processing pipeline
- **Testing**: Validate entire workflow end-to-end

## 🔍 Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Run `pip install` for missing packages
   - Check Python version compatibility

2. **STAC API Errors**
   - Verify internet connection
   - Check API endpoint availability
   - Review error messages for specific issues

3. **Data Processing Errors**
   - Check file permissions
   - Verify data format compatibility
   - Review error logs for specific issues

4. **Storage Connection Issues**
   - Ensure running in EDITO Datalab environment
   - Check environment variables
   - Verify bucket permissions

### Debug Mode
Run individual scripts with verbose output:
```bash
python -u 01_get_stac_collections.py
```

## 📈 Performance Tips

- **Smaller Subsets**: Reduce `subset_size` for faster processing
- **Fewer Items**: Lower `max_items` to process fewer files
- **Parallel Processing**: Modify scripts to use multiprocessing
- **Caching**: Add caching for repeated API calls

## 🔄 Extending the Workflow

### Adding New Data Sources
1. Create new search script for additional data types
2. Add processing script for new format
3. Update combine script to include new data
4. Modify master script to include new steps

### Custom Analysis
1. Add analysis functions to individual scripts
2. Create new visualization scripts
3. Implement custom data transformations
4. Add statistical analysis capabilities

## 📚 Related Files

- `01_edito_datalab_demo.ipynb`: Jupyter notebook version
- `01_edito_datalab_demo.py`: Single script version
- `01_stac_search.R`: R script for STAC search

## 🤝 Contributing

To add new features or fix issues:
1. Test individual scripts thoroughly
2. Update documentation
3. Ensure compatibility with existing workflow
4. Add appropriate error handling

## 📞 Support

For issues or questions:
- Check error messages and logs
- Review this documentation
- Test individual components
- Contact EDITO support team
