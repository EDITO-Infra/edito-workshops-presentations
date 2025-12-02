#!/usr/bin/env python3
"""
Example Script: Creating STAC Items from NetCDF, Zarr, and Parquet Files

This is a DEMO/EXAMPLE script for learning purposes. It demonstrates one approach
to creating STAC items from different data formats. Actual implementations will
vary based on your specific needs and requirements.

This script demonstrates:
- NetCDF files with CF-compliant metadata (using xarray)
- Zarr files with CF-compliant metadata (using xarray)
- Parquet files with datetime columns and metadata (using DuckDB)

Usage:
    python make_stac_from_data.py netcdf <file.nc> <data_url> [output.json]
    python make_stac_from_data.py zarr <file.zarr> <data_url> [output.json]
    python make_stac_from_data.py parquet <file.parquet> <data_url> [output.json]

Note: data_url is REQUIRED and must be a valid URL where your data file can be accessed.
      This can be any accessible URL (cloud storage, MinIO, etc.)
"""

import sys
import json
import xarray as xr
import duckdb
import numpy as np
from datetime import datetime, timezone
from pathlib import Path
from pystac.validation import validate_dict
import re


def format_and_validate_datetime(dt_input, field_name="datetime"):
    """
    Format and validate datetime input.

    Args:
        dt_input: User input string (date or datetime)
        field_name: Name of the field for error messages

    Returns:
        str: ISO format datetime string in UTC (ends with Z)

    Raises:
        ValueError: If datetime format is invalid or not UTC
    """
    dt_input = dt_input.strip()

    # If just a date (YYYY-MM-DD), add default time
    if re.match(r'^\d{4}-\d{2}-\d{2}$', dt_input):
        dt_input = f"{dt_input}T00:00:00Z"
        print(f"   Added default time: {dt_input}")

    # Validate ISO format
    # Should be: YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS+00:00
    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[\+\-]\d{2}:\d{2})$'

    if not re.match(iso_pattern, dt_input):
        raise ValueError(
            f"Invalid {field_name} format. Expected ISO format: "
            "YYYY-MM-DDTHH:MM:SSZ (e.g., 2023-01-01T00:00:00Z)"
        )

    # Check if it's UTC (ends with Z or +00:00)
    if not (dt_input.endswith('Z') or dt_input.endswith('+00:00')):
        raise ValueError(
            f"Invalid {field_name}: Must be in UTC timezone. "
            "Use 'Z' suffix (e.g., 2023-01-01T00:00:00Z) or '+00:00'"
        )

    # Convert +00:00 to Z for consistency
    if dt_input.endswith('+00:00'):
        dt_input = dt_input.replace('+00:00', 'Z')

    # Try to parse to validate
    try:
        if dt_input.endswith('Z'):
            dt = datetime.fromisoformat(dt_input.replace('Z', '+00:00'))
        else:
            dt = datetime.fromisoformat(dt_input)
    except ValueError as e:
        raise ValueError(f"Invalid {field_name} format: {e}")

    return dt_input


def create_stac_from_netcdf_zarr(data_file, data_url, output_file=None, engine='netcdf4'):
    """
    Create a STAC item from a NetCDF or Zarr file using xarray.

    Args:
        data_file: Path to NetCDF or Zarr file
        data_url: URL where the data file can be accessed (required)
        output_file: Path to save the STAC item JSON (optional)
        engine: 'netcdf4' or 'zarr' - xarray engine to use

    Returns:
        dict: STAC item as a dictionary
    """
    print(f"📖 Reading {engine} file: {data_file}")

    # Open with xarray using the specified engine
    if engine == 'zarr':
        ds = xr.open_zarr(data_file, decode_times=True)
    else:
        ds = xr.open_dataset(data_file, engine='netcdf4', decode_times=True)

    try:
        # Find coordinate variables
        lat_names = ['lat', 'latitude', 'y', 'lat_rho']
        lon_names = ['lon', 'longitude', 'x', 'lon_rho']
        time_names = ['time', 'time_counter', 't']

        lat_coord = None
        lon_coord = None
        time_coord = None

        for name in lat_names:
            if name in ds.coords or name in ds.dims:
                lat_coord = name
                break

        for name in lon_names:
            if name in ds.coords or name in ds.dims:
                lon_coord = name
                break

        for name in time_names:
            if name in ds.coords or name in ds.dims:
                time_coord = name
                break

        if not lat_coord or not lon_coord:
            raise ValueError("Could not find latitude/longitude coordinates")

        # Calculate bounding box
        lat_data = ds[lat_coord].values
        lon_data = ds[lon_coord].values
        bbox = [
            float(np.min(lon_data)),  # min_lon
            float(np.min(lat_data)),  # min_lat
            float(np.max(lon_data)),  # max_lon
            float(np.max(lat_data))   # max_lat
        ]

        # Extract temporal information
        if time_coord and time_coord in ds.coords:
            try:
                time_data = ds[time_coord]
                if len(time_data) > 0:
                    time_pd = time_data.to_pandas()
                    start_datetime = time_pd.min().strftime("%Y-%m-%dT%H:%M:%SZ")
                    end_datetime = time_pd.max().strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    print("⚠️  Time coordinate found but empty")
                    start_input = input(
                        "Enter start datetime (ISO format UTC, e.g., 2023-01-01T00:00:00Z or 2023-01-01): ").strip()
                    end_input = input(
                        "Enter end datetime (ISO format UTC, e.g., 2023-12-31T23:59:59Z or 2023-12-31): ").strip()
                    if not start_input or not end_input:
                        raise ValueError("Start and end datetime are required")
                    start_datetime = format_and_validate_datetime(
                        start_input, "start_datetime")
                    end_datetime = format_and_validate_datetime(
                        end_input, "end_datetime")
            except Exception as e:
                print(f"Error extracting temporal information: {e}")
                start_input = input(
                    "Enter start datetime (ISO format UTC, e.g., 2023-01-01T00:00:00Z or 2023-01-01): ").strip()
                end_input = input(
                    "Enter end datetime (ISO format UTC, e.g., 2023-12-31T23:59:59Z or 2023-12-31): ").strip()
                if not start_input or not end_input:
                    raise ValueError("Start and end datetime are required")
                start_datetime = format_and_validate_datetime(
                    start_input, "start_datetime")
                end_datetime = format_and_validate_datetime(
                    end_input, "end_datetime")
        else:
            print("⚠️  No time coordinate found in dataset")
            start_input = input(
                "Enter start datetime (ISO format UTC, e.g., 2023-01-01T00:00:00Z or 2023-01-01): ").strip()
            end_input = input(
                "Enter end datetime (ISO format UTC, e.g., 2023-12-31T23:59:59Z or 2023-12-31): ").strip()
            if not start_input or not end_input:
                raise ValueError("Start and end datetime are required")
            start_datetime = format_and_validate_datetime(
                start_input, "start_datetime")
            end_datetime = format_and_validate_datetime(
                end_input, "end_datetime")

        # Extract CF metadata from attributes
        attrs = ds.attrs

        institution = attrs.get(
            'institution', attrs.get('source', 'Unknown Institution'))
        institution_url = attrs.get(
            'institution_url', attrs.get('references', ''))
        title = attrs.get('title', f"Data from {Path(data_file).name}")
        description = attrs.get(
            'summary', attrs.get('comment', f'{engine.upper()} dataset'))
        license_info = attrs.get('license', 'proprietary')

        # Create providers list
        providers = []
        if institution != 'Unknown Institution' or institution_url:
            providers.append({
                "name": str(institution),
                "roles": ["producer"],
                "url": str(institution_url) if institution_url else None
            })

        # Contact information
        contact = attrs.get('contact', attrs.get('creator_email', ''))
        if contact:
            providers.append({
                "name": str(contact),
                "roles": ["processor"],
                "url": None
            })

        # Generate item ID
        item_id = f"{Path(data_file).stem}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

        # Create geometry
        min_lon, min_lat, max_lon, max_lat = bbox
        geometry = {
            "type": "Polygon",
            "coordinates": [[
                [min_lon, min_lat],
                [min_lon, max_lat],
                [max_lon, max_lat],
                [max_lon, min_lat],
                [min_lon, min_lat]
            ]]
        }

        # Require data_url
        if not data_url:
            raise ValueError(
                "data_url is required. Provide a URL where your data file can be accessed.\n"
                "This can be any accessible URL, including EDITO MinIO storage or other cloud storage."
            )

        # Determine asset type
        asset_type = "application/x-netcdf" if engine == 'netcdf4' else "application/zarr"

        # Create STAC item
        stac_item = {
            "id": item_id,
            "type": "Feature",
            "stac_version": "1.0.0",
            "properties": {
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "datetime": start_datetime,
                "title": str(title),
                "description": str(description),
                "license": str(license_info),
                "providers": providers
            },
            "geometry": geometry,
            "bbox": bbox,
            "assets": {
                "data": {
                    "href": data_url,
                    "type": asset_type,
                    "roles": ["data"],
                    "title": f"{engine.upper()} data file"
                }
            },
            "links": []
        }

        # Add CF-specific attributes if present
        cf_attrs = ['conventions', 'history',
                    'source', 'project', 'experiment_id']
        for attr in cf_attrs:
            if attr in attrs:
                stac_item["properties"][f"cf:{attr}"] = str(attrs[attr])

        # Validate
        try:
            validate_dict(stac_item)
            print("✅ STAC item is valid")
        except Exception as e:
            print(f"⚠️  Validation warning: {e}")

        # Save if output file specified
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(stac_item, f, indent=2)
            print(f"💾 Saved STAC item to: {output_file}")

        return stac_item
    finally:
        ds.close()


def create_stac_from_parquet(parquet_file, data_url=None, output_file=None):
    """
    Create a STAC item from a Parquet file.

    Args:
        parquet_file: Path to Parquet file or S3 URL (e.g., 's3://bucket/file.parquet')
        data_url: URL where the Parquet file can be accessed (required).
                  Can point to any accessible location (e.g., cloud storage, MinIO, etc.)
        output_file: Path to save the STAC item JSON (optional)

    Returns:
        dict: STAC item as a dictionary

    Note:
        The Parquet file must have:
        - A column with datetime type (any column name)
        - Either a geometry column OR 'lat' and 'lon' columns for spatial bounds

    Uses DuckDB for efficient Parquet file reading (supports local files and S3 URLs).
    """
    print(f"📖 Reading Parquet file: {parquet_file}")

    # Connect to DuckDB
    conn = duckdb.connect()

    # Get column information
    columns_info = conn.execute(
        f"DESCRIBE SELECT * FROM '{parquet_file}'").fetchall()
    column_names = [col[0] for col in columns_info]
    column_types = {col[0]: col[1] for col in columns_info}

    # Find datetime column (check for datetime type, not column name)
    datetime_col_name = None
    for col_name, col_type in column_types.items():
        if 'TIMESTAMP' in col_type.upper() or 'DATE' in col_type.upper():
            datetime_col_name = col_name
            break

    # Datetime is required - prompt user if not found
    if datetime_col_name is None:
        print("⚠️  No datetime column found in Parquet file")
        start_input = input(
            "Enter start datetime (ISO format UTC, e.g., 2023-01-01T00:00:00Z or 2023-01-01): ").strip()
        end_input = input(
            "Enter end datetime (ISO format UTC, e.g., 2023-12-31T23:59:59Z or 2023-12-31): ").strip()
        if not start_input or not end_input:
            raise ValueError(
                "Start and end datetime are required when no datetime column is present")
        start_datetime = format_and_validate_datetime(
            start_input, "start_datetime")
        end_datetime = format_and_validate_datetime(end_input, "end_datetime")
    else:
        # Extract datetime range
        datetime_query = f"""
            SELECT 
                MIN({datetime_col_name}) as min_datetime,
                MAX({datetime_col_name}) as max_datetime
            FROM '{parquet_file}'
        """
        datetime_result = conn.execute(datetime_query).fetchone()
        start_datetime = datetime_result[0].strftime("%Y-%m-%dT%H:%M:%SZ")
        end_datetime = datetime_result[1].strftime("%Y-%m-%dT%H:%M:%SZ")

    # Extract provider from Parquet metadata (DuckDB can read metadata)
    provider = {"name": "Unknown Provider"}
    try:
        # Try to read metadata from Parquet file
        metadata_query = f"SELECT * FROM parquet_metadata('{parquet_file}')"
        metadata_result = conn.execute(metadata_query).fetchall()
        # Look for provider in metadata
        for row in metadata_result:
            if 'provider' in str(row).lower():
                try:
                    provider_info = str(row)
                    provider = json.loads(
                        provider_info) if provider_info else provider
                    break
                except Exception as e:
                    print(f"Error loading provider metadata: {e}")
    except Exception as e:
        print(f"Error reading provider metadata: {e}")

    # Calculate spatial bounds - check for geometry column first, then lat/lon
    bbox = None

    # Check for geometry column (DuckDB spatial extension)
    geometry_col_name = None
    for col_name in column_names:
        if 'geometry' in col_name.lower():
            geometry_col_name = col_name
            break

    if geometry_col_name:
        try:
            # Try to use DuckDB spatial extension for geometry bounds
            conn.execute("INSTALL spatial;")
            conn.execute("LOAD spatial;")
            bounds_query = f"""
                SELECT
                    ST_XMin(ST_Extent({geometry_col_name})) as min_lon,
                    ST_YMin(ST_Extent({geometry_col_name})) as min_lat,
                    ST_XMax(ST_Extent({geometry_col_name})) as max_lon,
                    ST_YMax(ST_Extent({geometry_col_name})) as max_lat
                FROM '{parquet_file}'
            """
            bounds_result = conn.execute(bounds_query).fetchone()
            if bounds_result and all(x is not None for x in bounds_result):
                bbox = [float(x) for x in bounds_result]
        except Exception:
            # Spatial extension not available or geometry not supported
            pass

    # Fall back to lat/lon columns if no geometry column found
    if bbox is None:
        if 'lat' not in column_names or 'lon' not in column_names:
            raise ValueError(
                "Parquet file must have either:\n"
                "  - A geometry column, OR\n"
                "  - 'lat' and 'lon' columns for spatial bounds"
            )

        bounds_query = f"""
            SELECT
                MIN(lon) as min_lon,
                MIN(lat) as min_lat,
                MAX(lon) as max_lon,
                MAX(lat) as max_lat
            FROM '{parquet_file}'
        """
        bounds_result = conn.execute(bounds_query).fetchone()
        bbox = [
            float(bounds_result[0]),  # min_lon
            float(bounds_result[1]),  # min_lat
            float(bounds_result[2]),  # max_lon
            float(bounds_result[3])   # max_lat
        ]

    conn.close()

    # Generate item ID
    if parquet_file.startswith(('s3://', 'http://', 'https://')):
        # Extract filename from URL
        file_name = Path(parquet_file.split('/')[-1]).stem
    else:
        file_name = Path(parquet_file).stem
    item_id = f"{file_name}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

    # Create geometry
    min_lon, min_lat, max_lon, max_lat = bbox
    geometry = {
        "type": "Polygon",
        "coordinates": [[
            [min_lon, min_lat],
            [min_lon, max_lat],
            [max_lon, max_lat],
            [max_lon, min_lat],
            [min_lon, min_lat]
        ]]
    }

    # Require data_url
    if not data_url:
        raise ValueError(
            "data_url is required. Provide a URL where your data file can be accessed.\n"
            "This can be any accessible URL, including EDITO MinIO storage or other cloud storage."
        )

    # Create providers list
    providers = []
    if provider.get("name") != "Unknown Provider":
        providers.append({
            "name": provider.get("name", "Unknown Provider"),
            "roles": provider.get("roles", ["producer"]),
            "url": provider.get("url", None)
        })

    # Create STAC item
    stac_item = {
        "id": item_id,
        "type": "Feature",
        "stac_version": "1.0.0",
        "properties": {
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "datetime": start_datetime,
            "title": f"Data from {Path(parquet_file.split('/')[-1]).name if '/' in parquet_file else Path(parquet_file).name}",
            "description": "Marine observations in Parquet format",
            "providers": providers,
            "license": provider.get("license", "proprietary")
        },
        "geometry": geometry,
        "bbox": bbox,
        "assets": {
            "data": {
                "href": data_url,
                "type": "application/x-parquet",
                "roles": ["data"],
                "title": "Parquet data file"
            }
        },
        "links": []
    }

    # Validate
    try:
        validate_dict(stac_item)
        print("✅ STAC item is valid")
    except Exception as e:
        print(f"⚠️  Validation warning: {e}")

    # Save if output file specified
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(stac_item, f, indent=2)
        print(f"💾 Saved STAC item to: {output_file}")

    return stac_item


def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print(
            "  python make_stac_from_data.py netcdf <file.nc> <data_url> [output.json]")
        print(
            "  python make_stac_from_data.py zarr <file.zarr> <data_url> [output.json]")
        print(
            "  python make_stac_from_data.py parquet <file.parquet> <data_url> [output.json]")
        print()
        print("Arguments:")
        print("  format_type  : 'netcdf', 'zarr', or 'parquet'")
        print("  file         : Path to your data file")
        print("  data_url     : REQUIRED - URL where your data file can be accessed")
        print("  output.json  : Optional - Output file path (default: auto-generated)")
        print()
        print("Examples:")
        print("  python make_stac_from_data.py netcdf ocean_data.nc https://example.com/data/ocean_data.nc")
        print("  python make_stac_from_data.py zarr ocean_data.zarr https://example.com/data/ocean_data.zarr")
        print("  python make_stac_from_data.py parquet obs.parquet https://minio.edito.eu/bucket/obs.parquet obs_stac.json")
        print()
        print("Note: data_url can point to any accessible location (cloud storage, MinIO, etc.)")
        sys.exit(1)

    format_type = sys.argv[1].lower()
    input_file = sys.argv[2]
    data_url = sys.argv[3]  # Required
    output_file = sys.argv[4] if len(sys.argv) > 4 else None

    # Check if file exists (skip check for S3 URLs)
    if not input_file.startswith(('s3://', 'http://', 'https://')):
        if not Path(input_file).exists():
            print(f"❌ File not found: {input_file}")
            sys.exit(1)

    try:
        if format_type == 'netcdf':
            stac_item = create_stac_from_netcdf_zarr(
                input_file, data_url, output_file, engine='netcdf4')
        elif format_type == 'zarr':
            stac_item = create_stac_from_netcdf_zarr(
                input_file, data_url, output_file, engine='zarr')
        elif format_type == 'parquet':
            stac_item = create_stac_from_parquet(
                input_file, data_url, output_file)
        else:
            print(f"❌ Unknown format: {format_type}")
            print("Supported formats: netcdf, zarr, parquet")
            sys.exit(1)

        print("\n📦 Created STAC item:")
        print(json.dumps(stac_item, indent=2))

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
