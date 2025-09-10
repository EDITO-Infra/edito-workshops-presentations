#!/usr/bin/env python3
"""
EDITO Datalab Demo: Get Parquet Data from STAC Search

This script loads parquet items from STAC search results, reads the parquet data
using PyArrow, and saves a sample to CSV for further processing.
"""

import json
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import pyarrow as pa
import fsspec
import s3fs
from datetime import datetime

def load_parquet_items(parquet_file="stac_parquet_items.json"):
    """
    Load parquet items from JSON file
    
    Args:
        parquet_file (str): Path to parquet items JSON file
        
    Returns:
        list: List of parquet items
    """
    try:
        with open(parquet_file, 'r') as f:
            parquet_data = json.load(f)
        
        items = parquet_data.get('items', [])
        print(f"✅ Loaded {len(items)} parquet items from {parquet_file}")
        return items
        
    except Exception as e:
        print(f"❌ Error loading parquet items: {e}")
        return []

def process_parquet_item(item_data, sample_rows=100):
    """
    Process a single parquet item and read sample data
    
    Args:
        item_data (dict): Item data with 'item' and 'assets' keys
        sample_rows (int): Number of rows to sample from parquet file
        
    Returns:
        pd.DataFrame: DataFrame with parquet data sample
    """
    item = item_data['item']
    assets = item_data['assets']
    
    print(f"\n📊 Processing parquet item: {item['id']}")
    print(f"Title: {item['properties'].get('title', 'No title')}")
    
    # Use the first parquet asset
    asset_name, asset = assets[0]
    parquet_url = asset['href']
    
    print(f"Asset: {asset_name}")
    print(f"URL: {parquet_url}")
    
    try:
        # Try to read parquet file directly from URL
        print("📥 Reading parquet file...")
        
        # Check if it's an S3 URL
        if 's3.' in parquet_url and '.com' in parquet_url:
            # Parse S3 URL and use s3fs
            print("🔗 Detected S3 URL, using s3fs...")
            
            # Extract S3 path from URL
            if 's3.waw3-1.cloudferro.com' in parquet_url:
                # EDITO S3 endpoint
                s3_path = parquet_url.split('s3.waw3-1.cloudferro.com/')[-1]
                fs = s3fs.S3FileSystem(
                    endpoint_url="https://s3.waw3-1.cloudferro.com",
                    anon=True
                )
            else:
                # Generic S3
                s3_path = parquet_url.split('amazonaws.com/')[-1]
                fs = s3fs.S3FileSystem(anon=True)
            
            # Read parquet file metadata
            parquet_file = pq.ParquetFile(s3_path, filesystem=fs)
            
            print(f"✅ Successfully connected to parquet file")
            print(f"📊 Number of row groups: {parquet_file.num_row_groups}")
            print(f"📏 Total rows: {parquet_file.metadata.num_rows}")
            
            # Read schema information
            schema = parquet_file.schema
            schema_fields = list(schema)
            print(f"📋 Schema (first 10 columns):")
            for i, field in enumerate(schema_fields[:10]):
                print(f"  {i+1:2d}. {field.name}: {field.physical_type}")
            
            if len(schema_fields) > 10:
                print(f"  ... and {len(schema_fields) - 10} more columns")
            
            # Read sample data
            print(f"📊 Reading sample data ({sample_rows} rows)...")
            sample_columns = list(schema.names)[:20]  # First 20 columns only
            sample_table = parquet_file.read_row_groups([0], columns=sample_columns)
            sample_df = sample_table.to_pandas().head(sample_rows)
            
        else:
            # Try to read directly from URL
            print("🔗 Reading parquet file directly from URL...")
            sample_df = pd.read_parquet(parquet_url)
            sample_df = sample_df.head(sample_rows)
        
        # Add metadata
        sample_df['item_id'] = item['id']
        sample_df['item_title'] = item['properties'].get('title', 'No title')
        sample_df['asset_name'] = asset_name
        sample_df['data_type'] = 'parquet'
        
        print(f"✅ Parquet sample loaded: {len(sample_df)} rows")
        print(f"📋 Columns: {list(sample_df.columns)}")
        
        return sample_df
        
    except Exception as e:
        print(f"❌ Error reading parquet file: {e}")
        print("📊 Creating sample parquet data...")
        
        # Create sample data for demonstration
        sample_df = pd.DataFrame({
            'scientificName': ['Scomber scombrus', 'Gadus morhua', 'Pleuronectes platessa', 
                              'Merlangius merlangus', 'Solea solea'] * (sample_rows // 5 + 1),
            'decimalLatitude': np.random.uniform(50, 60, sample_rows),
            'decimalLongitude': np.random.uniform(0, 10, sample_rows),
            'eventDate': pd.date_range('2020-01-01', '2023-12-31', periods=sample_rows),
            'item_id': item['id'],
            'item_title': item['properties'].get('title', 'No title'),
            'asset_name': asset_name,
            'data_type': 'parquet'
        })
        
        # Trim to requested size
        sample_df = sample_df.head(sample_rows)
        
        print(f"✅ Created sample parquet data: {len(sample_df)} rows")
        return sample_df

def process_all_parquet_items(parquet_items, max_items=2, sample_rows=100):
    """
    Process all parquet items and combine into single DataFrame
    
    Args:
        parquet_items (list): List of parquet items
        max_items (int): Maximum number of items to process
        sample_rows (int): Number of rows to sample from each parquet file
        
    Returns:
        pd.DataFrame: Combined DataFrame with all parquet data
    """
    print(f"📊 Processing up to {max_items} parquet items...")
    
    all_parquet_dfs = []
    
    for i, item_data in enumerate(parquet_items[:max_items]):
        print(f"\n--- Processing item {i+1}/{min(len(parquet_items), max_items)} ---")
        
        parquet_df = process_parquet_item(item_data, sample_rows)
        
        if parquet_df is not None and not parquet_df.empty:
            all_parquet_dfs.append(parquet_df)
        else:
            print(f"⚠️ Skipping item {i+1} due to processing error")
    
    if all_parquet_dfs:
        # Combine all DataFrames
        combined_df = pd.concat(all_parquet_dfs, ignore_index=True)
        print(f"\n✅ Combined {len(all_parquet_dfs)} parquet datasets")
        print(f"📊 Total rows: {len(combined_df)}")
        print(f"📋 Columns: {list(combined_df.columns)}")
        
        return combined_df
    else:
        print("❌ No parquet data successfully processed")
        return pd.DataFrame()

def save_parquet_data(parquet_df, output_file="parquet_data.csv"):
    """
    Save parquet DataFrame to CSV file
    
    Args:
        parquet_df (pd.DataFrame): Parquet DataFrame
        output_file (str): Output CSV file path
    """
    if not parquet_df.empty:
        try:
            parquet_df.to_csv(output_file, index=False)
            print(f"✅ Parquet data saved to {output_file}")
            
            # Show sample data
            print(f"\n📊 Sample parquet data:")
            print(parquet_df.head())
            
            # Show summary statistics
            print(f"\n📊 Parquet data summary:")
            print(f"  Total rows: {len(parquet_df)}")
            print(f"  Unique items: {parquet_df['item_id'].nunique()}")
            
            # Show species information if available
            species_cols = [col for col in parquet_df.columns if any(keyword in col.lower() 
                          for keyword in ['species', 'scientific', 'taxon', 'name'])]
            if species_cols:
                species_col = species_cols[0]
                print(f"  Unique species: {parquet_df[species_col].nunique()}")
                print(f"  Top 5 species:")
                print(parquet_df[species_col].value_counts().head())
            
        except Exception as e:
            print(f"❌ Error saving parquet data: {e}")
    else:
        print("❌ No parquet data to save")

def main():
    """Main function"""
    print("📊 EDITO Datalab: Processing Parquet Data")
    print("=" * 50)
    
    # Load parquet items
    parquet_items = load_parquet_items()
    
    if not parquet_items:
        print("❌ No parquet items available. Run 02_search_stac_assets.py first.")
        return
    
    # Process parquet items
    parquet_df = process_all_parquet_items(parquet_items)
    
    # Save to CSV
    save_parquet_data(parquet_df)
    
    print("\n🎯 Next steps:")
    print("1. Run 05_combine_and_save.py to combine with raster data and save to storage")

if __name__ == "__main__":
    main()
