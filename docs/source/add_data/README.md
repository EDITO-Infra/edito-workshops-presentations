# Add Data to EDITO

Learn how to contribute your marine datasets to the EDITO Data Lake using STAC (SpatioTemporal Asset Catalog) standards.

## 🎯 What You'll Learn

- Understand STAC (SpatioTemporal Asset Catalog) and why EDITO uses it
- Read and explore existing STAC catalogs from EDITO
- Create valid STAC items from your data files
- Extract metadata from NetCDF files with CF conventions
- Extract metadata from Parquet files
- Validate STAC items before submission
- Post STAC items to the EDITO Data API (see official docs)

## 🚀 Quick Start

- **Prepare your data**: Ensure your NetCDF or Parquet file is accessible via a URL
- **Follow the presentation**: [Data Contribution Guide](../presentations/add_data_slidedeck.html)
- **Create STAC items**: Use `make_stac_from_data.py` with your data URL
- **Post to EDITO**: Submit your STAC item to the EDITO API

## 📁 Example Scripts

These are demo/example scripts for learning purposes. Actual implementations will vary based on your specific needs.

- `readstac.py` - Read and explore STAC catalogs from EDITO
- `makestac.py` - Create and validate STAC items
- `make_stac_from_data.py` - Example script demonstrating STAC item creation from NetCDF, Zarr, or Parquet files

## 🛠️ Requirements

- **Python** (with packages: `pystac`, `xarray`, `zarr`, `duckdb`, `numpy`)
- **NetCDF, Zarr, or Parquet files** - Your data files to create STAC items from
- **Data URL** - A URL where your data file can be accessed (can be any accessible location)

### Install Python Dependencies

```bash
pip install pystac xarray zarr duckdb numpy
```

**Note:** 
- xarray handles NetCDF and Zarr files with CF conventions
- DuckDB automatically handles Parquet files efficiently, including geometry columns with its spatial extension

## 📚 Key Concepts

### What is STAC?

**STAC** = **SpatioTemporal Asset Catalog**

A standardized way to describe geospatial data:
- JSON-based metadata format
- Describes when, where, and what your data contains
- Links to actual data files (NetCDF, GeoTIFF, Zarr, etc.)
- Searchable and discoverable

**Why EDITO uses STAC:**
- Interoperability across different data sources
- Easy search and discovery of marine datasets
- Standard metadata for automated processing
- Integration with modern cloud-native tools

### EDITO Data Lake Architecture

**EDITO Data Lake** hosts marine datasets using:

📊 **STAC Catalog**: Metadata and discovery
- Collections organized by data type
- Items describe individual datasets
- Searchable by space, time, and properties

🗄️ **Object Storage**: Actual data files
- S3-compatible cloud storage
- Analysis-ready formats (Zarr, Parquet, COG)
- High-performance access

🔗 **API Access**: `api.dive.edito.eu/data`
- RESTful STAC API
- Search and filter capabilities
- Authentication for data contribution

## 🔧 Example Scripts

### Reading STAC Catalogs

**`readstac.py`** - Explore existing data:

```python
import pystac

# Read STAC catalog from EDITO
stac_url = "https://api.dive.edito.eu/data/catalogs/Galicia_CCMM_catalog"
stac = pystac.Catalog.from_file(stac_url)

# Save locally for offline use
stac.normalize_and_save("data/mystac/", catalog_type="SELF_CONTAINED")

print(stac)
```

### Creating STAC Items

**`makestac.py`** - Build valid STAC items:

```python
from pystac.validation import validate_dict
import pystac

metadata = {
    "type": "Feature",
    "stac_version": "1.0.0",
    "id": "example-item-001",
    "properties": {
        "datetime": "2020-01-01T12:00:00Z",
        "start_datetime": "2020-01-01T12:00:00Z",
        "end_datetime": "2020-02-01T12:00:00Z"
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[[5.0, 51.0], [5.1, 51.0], [5.1, 51.1], [5.0, 51.1], [5.0, 51.0]]]
    },
    "bbox": [5.0, 51.0, 5.1, 51.1],
    "assets": {
        "data": {
            "href": "https://example.org/data/example-item-001.tif",
            "type": "image/tiff; application=geotiff",
            "roles": ["data"]
        }
    }
}

# Validate the STAC item
try:
    validate_dict(metadata)
    print("✅ STAC item is valid")
except Exception as e:
    print(f"❌ Validation failed: {e}")
```

### Creating STAC Items from Your Data

**`make_stac_from_data.py`** - Example script demonstrating STAC item creation:

**Note:** This is a demo/example script for learning purposes. Your actual implementation may vary.

```bash
# From NetCDF file (data_url is REQUIRED - can be any accessible URL)
python make_stac_from_data.py netcdf my_ocean_data.nc https://example.com/data/my_ocean_data.nc my_data_stac.json

# From Zarr file (data_url is REQUIRED - can be any accessible URL)
python make_stac_from_data.py zarr my_ocean_data.zarr https://example.com/data/my_ocean_data.zarr my_data_stac.json

# From Parquet file (data_url is REQUIRED - can be any accessible URL)
python make_stac_from_data.py parquet my_observations.parquet https://example.com/data/my_observations.parquet obs_stac.json

# Or use EDITO MinIO storage:
python make_stac_from_data.py zarr my_ocean_data.zarr https://minio.edito.eu/bucket/my_ocean_data.zarr my_data_stac.json
```

**Important:** The `data_url` parameter is REQUIRED and must be a valid URL where your data file can be accessed. This can be any accessible location (cloud storage, MinIO, etc.). For EDITO MinIO storage, see [Personal Storage documentation](https://docs.dive.edito.eu/articles/integration/interactWithYourPersonalStorage.html).

**What the script does:**
- 📖 Reads NetCDF, Zarr, or Parquet file
- 🌍 Extracts spatial bounds (lat/lon)
- ⏰ Extracts temporal range (datetime)
- 📋 Reads metadata (institution, title, license)
- 📦 Creates valid STAC item
- ✅ Validates the output
- 💾 Saves locally as JSON

## 📋 Data File Requirements

### NetCDF Files

Your NetCDF file should follow CF conventions with:

- **Coordinate variables**: `lat`/`latitude`, `lon`/`longitude`, `time`
- **CF global attributes**:
  - `title` - Dataset title
  - `summary` or `comment` - Description
  - `institution` - Provider name
  - `contact` or `creator_email` - Contact information
  - `license` - License information
  - `conventions` - Should include "CF-1.x"

**Note:** Uses xarray for reading, which handles CF conventions automatically.

**Temporal Information:**
- If no `time` coordinate is found, you'll be prompted to enter start and end datetime
- Datetime must be in UTC format (see Datetime Handling section below)

### Zarr Files

Your Zarr file should follow CF conventions (same as NetCDF):

- **Coordinate variables**: `lat`/`latitude`, `lon`/`longitude`, `time`
- **CF global attributes**: Same as NetCDF (title, institution, license, etc.)

**Note:** Uses xarray for reading Zarr stores, supporting both local and cloud storage.

**Temporal Information:**
- If no `time` coordinate is found, you'll be prompted to enter start and end datetime
- Datetime must be in UTC format (see Datetime Handling section below)

### Parquet Files

Your Parquet file should have:

- **A column with datetime type** (any column name) for temporal information
- **Either**:
  - A geometry column, OR
  - `lat` and `lon` columns for spatial bounds
- **Optional**: Provider metadata stored in Parquet file metadata

**Note:** The script uses DuckDB for efficient Parquet reading, which:
- Supports reading directly from S3 URLs (`s3://bucket/file.parquet`)
- Supports geometry columns via its spatial extension
- Handles both local files and cloud storage

**Temporal Information:**
- If no datetime column is found, you'll be prompted to enter start and end datetime
- Datetime must be in UTC format (see Datetime Handling section below)

To add provider metadata when creating Parquet files:

```python
import pyarrow as pa
import pyarrow.parquet as pq
import json

provider_metadata = json.dumps({
    "name": "Marine Research Institute",
    "roles": ["producer"],
    "url": "https://institute.org",
    "license": "CC-BY-4.0"
})

table = pa.Table.from_pandas(df)
custom_metadata = {b'provider': provider_metadata.encode('utf-8')}
pq.write_table(table, 'my_data.parquet', metadata=custom_metadata)
```

## ⏰ Datetime Handling

If your data file doesn't contain temporal information (no time coordinate in NetCDF/Zarr or no datetime column in Parquet), the script will prompt you to enter start and end datetimes.

### Datetime Input Format

**Accepted Formats:**
- **Full datetime**: `2023-01-01T00:00:00Z` (ISO format with UTC timezone)
- **Date only**: `2023-01-01` (will be auto-formatted to `2023-01-01T00:00:00Z`)

### Requirements

- ✅ Must be in UTC timezone (ends with `Z` or `+00:00`)
- ✅ ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- ✅ Both start and end datetime are required

### Examples

**Valid Inputs:**
- `2023-01-01` → Auto-formatted to `2023-01-01T00:00:00Z`
- `2023-01-01T12:00:00Z` → Valid UTC datetime
- `2023-12-31T23:59:59Z` → Valid UTC datetime

**Invalid Inputs (will be rejected):**
- ❌ `2023-01-01T12:00:00` → Missing timezone
- ❌ `2023-01-01T12:00:00+01:00` → Non-UTC timezone
- ❌ `01/01/2023` → Wrong format

### Why UTC?

STAC requires all datetime values to be in UTC to ensure consistency across different timezones and systems. The script validates this requirement and will reject non-UTC datetimes.

## 🎥 Presentation

[View the interactive presentation](../presentations/add_data_slidedeck.html) to get started with contributing data to EDITO.

## 🤝 Contributing

Found an issue or have suggestions? Please contribute to improve this workshop!

## 📖 Additional Resources

- [EDITO Data API](https://api.dive.edito.eu/data/)
- [STAC Specification](https://stacspec.org/)
- [PySTAC Documentation](https://pystac.readthedocs.io/)
- [CF Conventions](https://cfconventions.org/)
- [NetCDF Documentation](https://www.unidata.ucar.edu/software/netcdf/)

---

**Ready to contribute your data?** Follow the presentation and start creating STAC items! 🌊📊

