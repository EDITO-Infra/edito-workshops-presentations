# Creating STAC Items for EDITO

This directory contains examples and scripts for creating STAC (SpatioTemporal Asset Catalog) items from your data files.

## Example Scripts

These are demo/example scripts for learning purposes. Actual implementations will vary based on your specific needs.

- **`readstac.py`** - Read and explore STAC catalogs from EDITO
- **`makestac.py`** - Basic example of creating and validating a STAC item
- **`make_stac_from_data.py`** - Example script demonstrating how to create STAC items from NetCDF, Zarr, or Parquet files

## Quick Start

### Creating STAC Items from NetCDF

```bash
# Provide a URL where your data file can be accessed:
python make_stac_from_data.py netcdf my_ocean_data.nc https://example.com/data/my_ocean_data.nc my_data_stac.json

# Or use EDITO MinIO storage:
python make_stac_from_data.py netcdf my_ocean_data.nc https://minio.edito.eu/bucket/my_ocean_data.nc my_data_stac.json
```

### Creating STAC Items from Zarr

```bash
# Provide a URL where your data file can be accessed:
python make_stac_from_data.py zarr my_ocean_data.zarr https://example.com/data/my_ocean_data.zarr my_data_stac.json

# Or use EDITO MinIO storage:
python make_stac_from_data.py zarr my_ocean_data.zarr https://minio.edito.eu/bucket/my_ocean_data.zarr my_data_stac.json
```

### Creating STAC Items from Parquet

```bash
# Read from local file:
python make_stac_from_data.py parquet my_observations.parquet https://example.com/data/my_observations.parquet obs_stac.json

# Read directly from S3:
python make_stac_from_data.py parquet s3://my-bucket/data/my_observations.parquet https://example.com/data/my_observations.parquet obs_stac.json

# Or use EDITO MinIO storage:
python make_stac_from_data.py parquet s3://minio-bucket/my_observations.parquet https://minio.edito.eu/bucket/my_observations.parquet obs_stac.json
```

**Note:** DuckDB can read Parquet files directly from S3 URLs (supports `s3://` URLs).

**Important:** The `data_url` parameter is REQUIRED and must be a valid URL where your data file can be accessed. This can be any accessible location (cloud storage, MinIO, etc.). For EDITO MinIO storage, see [Personal Storage documentation](https://docs.dive.edito.eu/articles/integration/interactWithYourPersonalStorage.html).

### Reading STAC Catalogs

```python
import pystac

# Read STAC catalog from EDITO
stac_url = "https://api.dive.edito.eu/data/catalogs/Galicia_CCMM_catalog"
stac = pystac.Catalog.from_file(stac_url)

# Save locally
stac.normalize_and_save("data/mystac/", catalog_type="SELF_CONTAINED")
```

## Data URL Requirements

**The `data_url` parameter is required** and must point to a URL where your data file can be accessed. This can be:

- Any cloud storage URL (S3, Azure Blob, Google Cloud Storage, etc.)
- EDITO MinIO storage (see [Personal Storage documentation](https://docs.dive.edito.eu/articles/integration/interactWithYourPersonalStorage.html))
- Any publicly accessible URL
- Any URL accessible to the EDITO platform

The URL will be included in the STAC item's `assets` section, allowing users to access your data.



## Requirements

```bash
pip install xarray zarr duckdb pystac requests numpy
```

## Getting an Access Token

To post items to EDITO, you need an access token. See the [EDITO documentation on getting tokens](https://docs.dive.edito.eu/articles/integration/getTokensAndAccessTokens.html).

**Note:** When requesting a token, set `client_id` to `edito`.

## Data Format Requirements

### NetCDF Files

Your NetCDF files should follow CF conventions:
- Coordinate variables: `lat`/`latitude`, `lon`/`longitude`, `time`
- Global attributes: `title`, `institution`, `license`, `summary`
- Standard variable names and units

**Note:** Uses xarray for reading, which handles CF conventions automatically.

**Temporal Information:**
- If no `time` coordinate is found, you'll be prompted to enter start and end datetime
- Datetime must be in UTC format (see Datetime Handling section below)

### Zarr Files

Your Zarr files should follow CF conventions (same as NetCDF):
- Coordinate variables: `lat`/`latitude`, `lon`/`longitude`, `time`
- Global attributes: `title`, `institution`, `license`, `summary`
- Standard variable names and units

**Note:** Uses xarray for reading Zarr stores, supporting both local and cloud storage.

**Temporal Information:**
- If no `time` coordinate is found, you'll be prompted to enter start and end datetime
- Datetime must be in UTC format (see Datetime Handling section below)

### Parquet Files

Your Parquet files should have:
- A column with datetime type (any column name) for temporal information
- **Either**:
  - A geometry column, OR
  - `lat` and `lon` columns for spatial bounds
- Optional: Provider metadata stored in Parquet file metadata

**Note:** The script uses DuckDB for efficient Parquet reading, which automatically handles geometry columns via its spatial extension.

### Datetime Handling

If your data file doesn't contain temporal information (no time coordinate in NetCDF/Zarr or no datetime column in Parquet), the script will prompt you to enter start and end datetimes.

**Datetime Input Format:**
- **Full datetime**: `2023-01-01T00:00:00Z` (ISO format with UTC timezone)
- **Date only**: `2023-01-01` (will be auto-formatted to `2023-01-01T00:00:00Z`)

**Requirements:**
- Must be in UTC timezone (ends with `Z` or `+00:00`)
- ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- Both start and end datetime are required

**Examples:**
- ✅ `2023-01-01` → Auto-formatted to `2023-01-01T00:00:00Z`
- ✅ `2023-01-01T12:00:00Z` → Valid UTC datetime
- ❌ `2023-01-01T12:00:00` → Missing timezone (will be rejected)
- ❌ `2023-01-01T12:00:00+01:00` → Non-UTC timezone (will be rejected)

## STAC Item Structure

A minimal STAC item requires:

- `id` - Unique identifier
- `type` - Must be `"Feature"`
- `stac_version` - STAC version (e.g., `"1.0.0"`)
- `geometry` - GeoJSON geometry
- `properties` - At least `datetime` or `start_datetime`/`end_datetime`
- `assets` - Links to data files

See the [STAC specification](https://stacspec.org/) for complete details.

## Posting STAC Items to EDITO

Once you have created a STAC item with the correct data URL, you can post it to the EDITO API. For complete documentation, see:

- **Interactive API Docs**: [rest.wiki - EDITO Data API](https://rest.wiki/?https://api.dive.edito.eu/data/api#)
- **Integration Guide**: [docs.dive.edito.eu - Interact with the Data API](https://docs.dive.edito.eu/articles/integration/interactWithTheDataAPI.html)

## Resources

- **EDITO Platform**: [dive.edito.eu](https://dive.edito.eu)
- **STAC Specification**: [stacspec.org](https://stacspec.org/)
- **EDITO API Documentation**: [docs.dive.edito.eu](https://docs.dive.edito.eu/articles/integration/interactWithTheDataAPI.html)
