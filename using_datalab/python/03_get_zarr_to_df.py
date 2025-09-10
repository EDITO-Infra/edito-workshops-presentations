#!/usr/bin/env python3
"""
EDITO Datalab Demo: Get Zarr/NetCDF Data and Convert to DataFrame

Simple script to load ARCO raster data (NetCDF, Zarr) from local storage or S3
and convert to DataFrame for analysis.
"""

import json
import pandas as pd
import numpy as np
import xarray as xr
import os
from datetime import datetime
import fsspec
import s3fs
import boto3

def load_search_results(search_file="stac_search_results.json"):
    """Load search results from JSON file"""
    try:
        with open(search_file, 'r') as f:
            search_data = json.load(f)
        
        items = search_data.get('items', [])
        print(f"✅ Loaded {len(items)} items from {search_file}")
        return items
        
    except Exception as e:
        print(f"❌ Error loading search results: {e}")
        return []

def find_raster_assets(items):
    """Find items with raster assets (NetCDF, Zarr)"""
    raster_items = []
    
    for item in items:
        item_raster_assets = []
        
        for asset_name, asset in item['assets'].items():
            asset_url = asset['href'].lower()
            
            # Check for raster files (NetCDF, Zarr)
            if any(ext in asset_url for ext in ['.nc', '.zarr', '.netcdf']):
                item_raster_assets.append((asset_name, asset))
        
        if item_raster_assets:
            raster_items.append({
                'item': item,
                'assets': item_raster_assets
            })
    
    print(f"🔍 Found {len(raster_items)} items with raster assets")
    return raster_items

def load_raster_data(asset_url, storage_type="auto"):
    """
    Load raster data from URL (local file, S3, MinIO, or HTTP)
    
    Args:
        asset_url (str): URL or path to raster data
        storage_type (str): 'local', 's3', 'minio', or 'auto'
    
    Returns:
        xarray.Dataset: Loaded raster dataset
    """
    print(f"📥 Loading raster data from: {asset_url}")
    
    try:
        if storage_type == "auto":
            # Auto-detect storage type
            if asset_url.startswith('s3://'):
                storage_type = "s3"
            elif os.path.exists(asset_url):
                storage_type = "local"
            else:
                storage_type = "http"
        
        if storage_type == "s3":
            # Load from S3 using s3fs
            print("☁️ Loading from S3...")
            fs = s3fs.S3FileSystem()
            ds = xr.open_dataset(fs.open(asset_url), engine='zarr' if asset_url.endswith('.zarr') else 'netcdf4')
        
        
        elif storage_type == "local":
            # Load from local file
            print("💾 Loading from local storage...")
            if asset_url.endswith('.zarr'):
                ds = xr.open_dataset(asset_url, engine='zarr')
            else:
                ds = xr.open_dataset(asset_url, engine='netcdf4')
        
        else:
            # Load from HTTP URL
            print("🌐 Loading from HTTP...")
            ds = xr.open_dataset(asset_url)
        
        print(f"✅ Successfully loaded dataset")
        print(f"   Dimensions: {ds.dims}")
        print(f"   Variables: {list(ds.data_vars)}")
        print(f"   Coordinates: {list(ds.coords)}")
        
        return ds
        
    except Exception as e:
        print(f"❌ Error loading raster data: {e}")
        return None

def process_raster_to_dataframe(ds, item_info, subset_size=100):
    """
    Process raster dataset and convert to DataFrame
    
    Args:
        ds (xarray.Dataset): Raster dataset
        item_info (dict): Item information
        subset_size (int): Maximum number of points to extract
    
    Returns:
        pd.DataFrame: Processed raster data
    """
    print(f"📊 Processing raster data...")
    
    # Find the best variable to use
    numeric_vars = []
    for var_name, var in ds.data_vars.items():
        if hasattr(var.dtype, 'kind') and var.dtype.kind in 'biufc':  # numeric types
            numeric_vars.append(var_name)
    
    if not numeric_vars:
        print("❌ No numeric variables found in dataset")
        return None
    
    # Use the first numeric variable
    var_name = numeric_vars[0]
    print(f"📊 Using variable: {var_name}")
    
    # Find coordinate variables
    lat_coord = None
    lon_coord = None
    
    for coord_name in ds.coords:
        if 'lat' in coord_name.lower():
            lat_coord = coord_name
        elif 'lon' in coord_name.lower():
            lon_coord = coord_name
    
    if not (lat_coord and lon_coord):
        print("❌ No lat/lon coordinates found")
        return None
    
    print(f"📍 Found coordinates: {lat_coord}, {lon_coord}")
    
    # Create subset
    var_data = ds[var_name]
    
    # Handle time dimension if present
    if 'time' in var_data.dims:
        var_data = var_data.isel(time=0)
        print("⏰ Using first time step")
    
    # Create spatial subset
    lat_size = min(subset_size, len(ds[lat_coord]))
    lon_size = min(subset_size, len(ds[lon_coord]))
    
    # Take a subset
    subset = var_data.isel(
        **{lat_coord: slice(0, lat_size), lon_coord: slice(0, lon_size)}
    )
    
    print(f"📊 Created subset: {subset.shape}")
    
    # Convert to DataFrame
    df = subset.to_dataframe().reset_index()
    
    # Rename columns
    df = df.rename(columns={
        var_name: 'raster_value',
        lat_coord: 'lat',
        lon_coord: 'lon'
    })
    
    # Clean data
    df = df.dropna(subset=['lat', 'lon'])
    df['raster_value'] = df['raster_value'].fillna(0)
    
    # Add metadata
    df['item_id'] = item_info['id']
    df['item_title'] = item_info['properties'].get('title', 'No title')
    df['variable_name'] = var_name
    df['data_type'] = 'raster'
    
    print(f"✅ Created DataFrame with {len(df)} rows")
    return df

def create_sample_data():
    """Create sample raster data for demonstration"""
    print("📊 Creating sample raster data...")
    
    np.random.seed(42)
    n_points = 50
    
    sample_data = pd.DataFrame({
        'lat': np.random.uniform(50, 60, n_points),
        'lon': np.random.uniform(0, 10, n_points),
        'raster_value': np.random.normal(10, 2, n_points),
        'item_id': 'sample-arco-raster',
        'item_title': 'Sample ARCO Raster Data',
        'variable_name': 'temperature',
        'data_type': 'raster'
    })
    
    print(f"✅ Created {len(sample_data)} sample points")
    return sample_data

def save_raster_data(df, output_file="raster_data.csv"):
    """Save raster DataFrame to CSV"""
    if not df.empty:
        try:
            df.to_csv(output_file, index=False)
            print(f"✅ Raster data saved to {output_file}")
            
            # Show summary
            print(f"\n📊 Data summary:")
            print(f"   Total rows: {len(df)}")
            print(f"   Unique items: {df['item_id'].nunique()}")
            if 'raster_value' in df.columns:
                print(f"   Value range: {df['raster_value'].min():.2f} - {df['raster_value'].max():.2f}")
            
            print(f"\n📋 Sample data:")
            print(df.head())
            
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    else:
        print("❌ No data to save")

def main():
    """Simple demo to process raster data"""
    print("🌊 EDITO Datalab: Process ARCO Raster Data")
    print("=" * 50)
    
    print("\n🎯 Data Source Options:")
    print("1. Use STAC search results")
    print("2. Input custom URL (MinIO, S3, local, HTTP)")
    print("3. Create sample data")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "2":
        # Custom URL input
        print("\n📝 Enter custom raster data URL:")
        print("Examples:")
        print("  - S3: s3://bucket/path/data.nc")
        print("  - Local: /path/to/local/data.zarr")
        print("  - HTTP: https://example.com/data.nc")
        
        custom_url = input("URL: ").strip()
        
        if custom_url:
            print(f"\n🗺️ Processing custom URL...")
            print(f"URL: {custom_url}")
            
            # Load raster data
            ds = load_raster_data(custom_url)
            
            if ds is not None:
                # Create dummy item info for processing
                item_info = {
                    'id': 'custom-raster-data',
                    'properties': {'title': 'Custom Raster Data'}
                }
                
                # Process to DataFrame
                df = process_raster_to_dataframe(ds, item_info)
                
                if df is not None:
                    save_raster_data(df)
                else:
                    print("❌ Failed to process raster data. Creating sample data.")
                    df = create_sample_data()
                    save_raster_data(df)
            else:
                print("❌ Failed to load raster data. Creating sample data.")
                df = create_sample_data()
                save_raster_data(df)
        else:
            print("❌ No URL provided. Creating sample data.")
            df = create_sample_data()
            save_raster_data(df)
    
    elif choice == "1":
        # Use STAC search results
        items = load_search_results()
        
        if not items:
            print("❌ No search results found. Run 02_search_stac_assets.py first.")
            print("💡 Creating sample data instead.")
            df = create_sample_data()
            save_raster_data(df)
            return
        
        # Find raster assets
        raster_items = find_raster_assets(items)
        
        if not raster_items:
            print("ℹ️ No raster assets found in search results.")
            print("💡 Creating sample data instead.")
            df = create_sample_data()
            save_raster_data(df)
            return
        
        # Process first raster item
        print(f"\n🗺️ Processing first raster item...")
        item_data = raster_items[0]
        item = item_data['item']
        asset_name, asset = item_data['assets'][0]
        
        print(f"Item: {item['id']}")
        print(f"Asset: {asset_name}")
        print(f"URL: {asset['href']}")
        
        # Load raster data
        ds = load_raster_data(asset['href'])
        
        if ds is not None:
            # Process to DataFrame
            df = process_raster_to_dataframe(ds, item)
            
            if df is not None:
                save_raster_data(df)
            else:
                print("❌ Failed to process raster data. Creating sample data.")
                df = create_sample_data()
                save_raster_data(df)
        else:
            print("❌ Failed to load raster data. Creating sample data.")
            df = create_sample_data()
            save_raster_data(df)
    
    else:
        # Create sample data
        print("📊 Creating sample data...")
        df = create_sample_data()
        save_raster_data(df)
    
    print(f"\n💡 Next: Run 'python 04_get_parquet_data.py' to process parquet data")

if __name__ == "__main__":
    main()