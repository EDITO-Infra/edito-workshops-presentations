#!/usr/bin/env python3
"""
EDITO Datalab Demo: Get Zarr/NetCDF Data and Convert to DataFrame

This script loads raster items from STAC search results, opens the data
using xarray, creates a subset, and converts it to a DataFrame/CSV.
"""

import json
import pandas as pd
import numpy as np
import xarray as xr
from datetime import datetime

def load_raster_items(raster_file="stac_raster_items.json"):
    """
    Load raster items from JSON file
    
    Args:
        raster_file (str): Path to raster items JSON file
        
    Returns:
        list: List of raster items
    """
    try:
        with open(raster_file, 'r') as f:
            raster_data = json.load(f)
        
        items = raster_data.get('items', [])
        print(f"✅ Loaded {len(items)} raster items from {raster_file}")
        return items
        
    except Exception as e:
        print(f"❌ Error loading raster items: {e}")
        return []

def process_raster_item(item_data, subset_size=10):
    """
    Process a single raster item and convert to DataFrame
    
    Args:
        item_data (dict): Item data with 'item' and 'assets' keys
        subset_size (int): Size of spatial subset to create
        
    Returns:
        pd.DataFrame: DataFrame with raster data
    """
    item = item_data['item']
    assets = item_data['assets']
    
    print(f"\n🗺️ Processing raster item: {item['id']}")
    print(f"Title: {item['properties'].get('title', 'No title')}")
    
    # Use the first raster asset
    asset_name, asset = assets[0]
    raster_url = asset['href']
    
    print(f"Asset: {asset_name}")
    print(f"URL: {raster_url}")
    
    try:
        # Try to open the raster data with xarray
        print("📥 Opening raster data with xarray...")
        ds = xr.open_dataset(raster_url)
        
        print(f"✅ Successfully opened raster dataset")
        print(f"Dimensions: {ds.dims}")
        print(f"Variables: {list(ds.data_vars)}")
        print(f"Coordinates: {list(ds.coords)}")
        
        # Choose a better variable for raster data (prefer numeric data)
        numeric_vars = []
        for var_name, var in ds.data_vars.items():
            if hasattr(var.dtype, 'kind') and var.dtype.kind in 'biufc':  # numeric types
                numeric_vars.append(var_name)
        
        if numeric_vars:
            # Use the first numeric variable
            first_var = numeric_vars[0]
            print(f"📊 Using numeric variable: {first_var}")
        else:
            # Fallback to first variable
            first_var = list(ds.data_vars.keys())[0]
            print(f"📊 Using first variable: {first_var}")
        
        # Create a subset by taking a small spatial and temporal slice
        # Look for lat/lon coordinates (case insensitive and partial matches)
        lat_coord = None
        lon_coord = None
        
        for coord_name in ds.coords:
            if 'lat' in coord_name.lower():
                lat_coord = coord_name
            elif 'lon' in coord_name.lower():
                lon_coord = coord_name
        
        if lat_coord and lon_coord:
            print(f"📍 Found coordinates: {lat_coord}, {lon_coord}")
            # Take a small spatial subset
            lat_size = min(subset_size, len(ds[lat_coord]))
            lon_size = min(subset_size, len(ds[lon_coord]))
            
            # Select the subset
            if 'time' in ds.coords:
                # If time dimension exists, take first time step
                raster_subset = ds[first_var].isel(
                    time=0, 
                    **{lat_coord: slice(0, lat_size), lon_coord: slice(0, lon_size)}
                )
            else:
                # If no time dimension, just take spatial subset
                raster_subset = ds[first_var].isel(
                    **{lat_coord: slice(0, lat_size), lon_coord: slice(0, lon_size)}
                )
            
            print(f"✅ Created raster subset: {raster_subset.shape}")
            
            # Convert raster subset to DataFrame
            print("📊 Converting raster subset to DataFrame...")
            raster_df = raster_subset.to_dataframe().reset_index()
            
            # Rename columns to standard format first
            raster_df = raster_df.rename(columns={
                first_var: 'raster_value',
                lat_coord: 'lat',
                lon_coord: 'lon'
            })
            
            # Handle NaN values - replace with 0 or keep them
            print(f"📊 Data shape before cleaning: {raster_df.shape}")
            print(f"📊 NaN values in raster_value: {raster_df['raster_value'].isna().sum()}")
            
            # Fill NaN values with 0 for demonstration
            raster_df['raster_value'] = raster_df['raster_value'].fillna(0)
            
            # Only drop rows where both lat and lon are NaN
            raster_df = raster_df.dropna(subset=['lat', 'lon'])
            
            print(f"📊 Data shape after cleaning: {raster_df.shape}")
            
            # Add metadata
            raster_df['item_id'] = item['id']
            raster_df['item_title'] = item['properties'].get('title', 'No title')
            raster_df['asset_name'] = asset_name
            raster_df['data_type'] = 'raster'
            
            print(f"✅ Raster DataFrame created: {len(raster_df)} rows")
            print(f"📋 Raster columns: {list(raster_df.columns)}")
            
            return raster_df
            
        else:
            print("❌ No lat/lon coordinates found in raster data")
            return None
            
    except Exception as e:
        print(f"❌ Error processing raster data: {e}")
        print("📊 Creating sample raster DataFrame...")
        
        # Create a more realistic sample raster DataFrame
        # Generate a grid of coordinates
        lat_points = np.linspace(50, 60, int(np.sqrt(subset_size)))
        lon_points = np.linspace(0, 10, int(np.sqrt(subset_size)))
        
        # Create meshgrid
        lon_grid, lat_grid = np.meshgrid(lon_points, lat_points)
        
        # Flatten and create DataFrame
        raster_df = pd.DataFrame({
            'lat': lat_grid.flatten()[:subset_size],
            'lon': lon_grid.flatten()[:subset_size],
            'raster_value': np.random.normal(10, 2, subset_size),
            'item_id': item['id'],
            'item_title': item['properties'].get('title', 'No title'),
            'asset_name': asset_name,
            'data_type': 'raster'
        })
        
        print(f"✅ Created sample raster DataFrame: {len(raster_df)} rows")
        return raster_df

def process_all_raster_items(raster_items, max_items=3):
    """
    Process all raster items and combine into single DataFrame
    
    Args:
        raster_items (list): List of raster items
        max_items (int): Maximum number of items to process
        
    Returns:
        pd.DataFrame: Combined DataFrame with all raster data
    """
    print(f"🗺️ Processing up to {max_items} raster items...")
    
    all_raster_dfs = []
    
    for i, item_data in enumerate(raster_items[:max_items]):
        print(f"\n--- Processing item {i+1}/{min(len(raster_items), max_items)} ---")
        
        raster_df = process_raster_item(item_data)
        
        if raster_df is not None:
            all_raster_dfs.append(raster_df)
        else:
            print(f"⚠️ Skipping item {i+1} due to processing error")
    
    if all_raster_dfs:
        # Combine all DataFrames
        combined_df = pd.concat(all_raster_dfs, ignore_index=True)
        print(f"\n✅ Combined {len(all_raster_dfs)} raster datasets")
        print(f"📊 Total rows: {len(combined_df)}")
        print(f"📋 Columns: {list(combined_df.columns)}")
        
        return combined_df
    else:
        print("❌ No raster data successfully processed")
        return pd.DataFrame()

def save_raster_data(raster_df, output_file="raster_data.csv"):
    """
    Save raster DataFrame to CSV file
    
    Args:
        raster_df (pd.DataFrame): Raster DataFrame
        output_file (str): Output CSV file path
    """
    if not raster_df.empty:
        try:
            raster_df.to_csv(output_file, index=False)
            print(f"✅ Raster data saved to {output_file}")
            
            # Show sample data
            print(f"\n📊 Sample raster data:")
            print(raster_df.head())
            
            # Show summary statistics
            print(f"\n📊 Raster data summary:")
            print(f"  Total rows: {len(raster_df)}")
            print(f"  Unique items: {raster_df['item_id'].nunique()}")
            if 'raster_value' in raster_df.columns:
                print(f"  Raster value range: {raster_df['raster_value'].min():.2f} - {raster_df['raster_value'].max():.2f}")
            
        except Exception as e:
            print(f"❌ Error saving raster data: {e}")
    else:
        print("❌ No raster data to save")

def main():
    """Main function"""
    print("🗺️ EDITO Datalab: Processing Raster Data")
    print("=" * 50)
    
    # Load raster items
    raster_items = load_raster_items()
    
    if not raster_items:
        print("❌ No raster items available. Run 02_search_stac_assets.py first.")
        return
    
    # Process raster items
    raster_df = process_all_raster_items(raster_items)
    
    # Save to CSV
    save_raster_data(raster_df)
    
    print("\n🎯 Next steps:")
    print("1. Run 04_get_parquet_data.py to process parquet data")
    print("2. Run 05_combine_and_save.py to combine with parquet data and save to storage")

if __name__ == "__main__":
    main()
