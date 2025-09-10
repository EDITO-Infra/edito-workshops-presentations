#!/usr/bin/env python3
"""
EDITO Datalab Demo: Simple Data Combination and Storage

This script allows you to:
1. Select a parquet asset (biodiversity data)
2. Select a zarr asset (ocean data) 
3. Combine them spatially
4. Save the result to your EDITO storage
"""

import pandas as pd
import numpy as np
import boto3
import os
import json
import requests
import logging
from datetime import datetime
import xarray as xr
import s3fs
import pyarrow.parquet as pq

def load_parquet_items(parquet_file="stac_parquet_items.json"):
    """Load parquet items from JSON file"""
    try:
        with open(parquet_file, 'r') as f:
            parquet_data = json.load(f)
        
        items = parquet_data.get('items', [])
        print(f"✅ Loaded {len(items)} parquet items from {parquet_file}")
        return items
        
    except Exception as e:
        print(f"❌ Error loading parquet items: {e}")
        return []

def load_zarr_items(zarr_file="stac_search_results.json"):
    """Load zarr items from JSON file"""
    try:
        with open(zarr_file, 'r') as f:
            zarr_data = json.load(f)
        
        items = zarr_data.get('items', [])
        print(f"✅ Loaded {len(items)} zarr items from {zarr_file}")
        return items
        
    except Exception as e:
        print(f"❌ Error loading zarr items: {e}")
        return []

def select_parquet_asset(parquet_items):
    """Let user select a parquet asset"""
    if not parquet_items:
        print("❌ No parquet items available")
        return None, None
    
    print(f"\n📊 Available Parquet Assets ({len(parquet_items)} items):")
    for i, item_data in enumerate(parquet_items):
        item = item_data['item']
        print(f"{i+1:2d}. {item['id']} - {item['properties'].get('title', 'No title')}")
        print(f"     Collection: {item['collection']}")
    
    while True:
        try:
            choice = input(f"\nSelect parquet asset (1-{len(parquet_items)}): ").strip()
            if not choice:
                return None, None
            
            idx = int(choice) - 1
            if 0 <= idx < len(parquet_items):
                selected_item = parquet_items[idx]
                item = selected_item['item']
                assets = selected_item['assets']
                
                print(f"✅ Selected: {item['id']}")
                print(f"   Title: {item['properties'].get('title', 'No title')}")
                print(f"   Collection: {item['collection']}")
                
                return selected_item, assets
            else:
                print(f"❌ Please enter a number between 1 and {len(parquet_items)}")
        except ValueError:
            print("❌ Please enter a valid number")

def select_zarr_asset(zarr_items):
    """Let user select a zarr asset"""
    if not zarr_items:
        print("❌ No zarr items available")
        return None, None
    
    # Filter for zarr assets only
    zarr_only = []
    for item in zarr_items:
        for asset_name, asset in item.get('assets', {}).items():
            if '.zarr' in asset['href'].lower():
                zarr_only.append((item, asset_name, asset))
                break
    
    if not zarr_only:
        print("❌ No zarr assets found in the items")
        return None, None
    
    print(f"\n🌊 Available Zarr Assets ({len(zarr_only)} items):")
    for i, (item, asset_name, asset) in enumerate(zarr_only):
        print(f"{i+1:2d}. {item['id']} - {item['properties'].get('title', 'No title')}")
        print(f"     Collection: {item['collection']}")
        print(f"     Asset: {asset_name}")
    
    while True:
        try:
            choice = input(f"\nSelect zarr asset (1-{len(zarr_only)}): ").strip()
            if not choice:
                return None, None
            
            idx = int(choice) - 1
            if 0 <= idx < len(zarr_only):
                selected_item, asset_name, asset = zarr_only[idx]
                print(f"✅ Selected: {selected_item['id']}")
                print(f"   Title: {selected_item['properties'].get('title', 'No title')}")
                print(f"   Collection: {selected_item['collection']}")
                print(f"   Asset: {asset_name}")
                
                return selected_item, asset
            else:
                print(f"❌ Please enter a number between 1 and {len(zarr_only)}")
        except ValueError:
            print("❌ Please enter a valid number")

def process_parquet_asset(parquet_item, assets, sample_rows=1000):
    """Process parquet asset and return DataFrame"""
    print(f"\n📊 Processing parquet asset...")
    
    # Get the first parquet asset
    asset_name, asset = assets[0]
    parquet_url = asset['href']
    
    print(f"Asset: {asset_name}")
    print(f"URL: {parquet_url}")
    
    try:
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
        sample_df['asset_name'] = asset_name
        sample_df['data_type'] = 'parquet'
        
        print(f"✅ Parquet sample loaded: {len(sample_df)} rows")
        print(f"📋 Columns: {list(sample_df.columns)}")
        
        # Add metadata
        sample_df['data_source'] = 'parquet'
        sample_df['asset_id'] = parquet_item['item']['id']
        sample_df['collection'] = parquet_item['item']['collection']
        
        return sample_df

    except Exception as e:
        print(f"❌ Error processing parquet asset: {e}")
        return pd.DataFrame()

def process_zarr_asset(zarr_item, asset, sample_points=1000):
    """Process zarr asset and return DataFrame"""
    print(f"\n🌊 Processing zarr asset...")
    
    zarr_url = asset['href']
    print(f"URL: {zarr_url}")
    
    try:
        # Read zarr file
        print("📥 Reading zarr file...")
        ds = xr.open_zarr(zarr_url)
        
        print(f"✅ Loaded dataset with dimensions: {dict(ds.dims)}")
        print(f"Variables: {list(ds.data_vars)}")
        
        # Convert to DataFrame
        df = ds.to_dataframe().reset_index()
        
        # Sample the data if it's too large
        if len(df) > sample_points:
            print(f"📊 Sampling {sample_points} points from {len(df)} total points")
            df = df.sample(n=sample_points, random_state=42)
        
        # Add metadata
        df['data_source'] = 'zarr'
        df['asset_id'] = zarr_item['id']
        df['collection'] = zarr_item['collection']
        
        return df
        
    except Exception as e:
        print(f"❌ Error processing zarr asset: {e}")
        return pd.DataFrame()

def combine_datasets(parquet_df, zarr_df):
    """Combine parquet and zarr datasets spatially"""
    print(f"\n🔗 Combining datasets...")
    print(f"Parquet data: {len(parquet_df)} rows")
    print(f"Zarr data: {len(zarr_df)} rows")
    
    if parquet_df.empty or zarr_df.empty:
        print("❌ One or both datasets are empty")
        return pd.DataFrame()
    
    # Check for spatial columns in both datasets
    parquet_spatial = []
    zarr_spatial = []
    
    # Check parquet for spatial columns
    for col in ['latitude', 'lat', 'y', 'decimalLatitude', 'decimal_latitude']:
        if col in parquet_df.columns:
            parquet_spatial.append(col)
            break
    
    for col in ['longitude', 'lon', 'x', 'decimalLongitude', 'decimal_longitude']:
        if col in parquet_df.columns:
            parquet_spatial.append(col)
            break
    
    # Check zarr for spatial columns
    for col in ['latitude', 'lat', 'y', 'decimalLatitude', 'decimal_latitude']:
        if col in zarr_df.columns:
            zarr_spatial.append(col)
            break
    
    for col in ['longitude', 'lon', 'x', 'decimalLongitude', 'decimal_longitude']:
        if col in zarr_df.columns:
            zarr_spatial.append(col)
            break
    
    print(f"Parquet spatial columns: {parquet_spatial}")
    print(f"Zarr spatial columns: {zarr_spatial}")
    
    # If both have spatial columns, we can do spatial joining
    if parquet_spatial and zarr_spatial:
        print("✅ Both datasets have spatial columns - performing spatial combination")
        
        # Rename columns to standard names for joining
        if len(parquet_spatial) >= 2:
            parquet_df = parquet_df.rename(columns={
                parquet_spatial[0]: 'latitude',
                parquet_spatial[1]: 'longitude'
            })
        
        if len(zarr_spatial) >= 2:
            zarr_df = zarr_df.rename(columns={
                zarr_spatial[0]: 'latitude', 
                zarr_spatial[1]: 'longitude'
            })
        
        # Simple concatenation for now (could be improved with spatial joining)
        combined_df = pd.concat([parquet_df, zarr_df], ignore_index=True)
        
    else:
        print("ℹ️ No common spatial columns found - performing simple concatenation")
        print("This will create a combined dataset with both data types")
        
        # Simple concatenation without spatial joining
        combined_df = pd.concat([parquet_df, zarr_df], ignore_index=True)
    
    print(f"✅ Combined dataset: {len(combined_df)} rows, {len(combined_df.columns)} columns")
    
    # Show data source distribution
    if 'data_source' in combined_df.columns:
        source_counts = combined_df['data_source'].value_counts()
        print(f"📊 Data sources: {dict(source_counts)}")
    
    return combined_df

def connect_to_storage():
    """Connect to EDITO storage"""
    print("\n💾 Connecting to EDITO storage...")
    
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        print("❌ No storage credentials found. Set AWS_ACCESS_KEY_ID and related environment variables.")
        return None
    
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=f"https://{os.getenv('AWS_S3_ENDPOINT')}",
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
        )
        
        print("✅ Connected to EDITO storage!")
        return s3
        
    except Exception as e:
        print(f"❌ Error connecting to storage: {e}")
        return None

def save_to_storage(combined_df, s3_client, bucket_name, folder_name):
    """Save combined dataset to EDITO storage"""
    print(f"\n💾 Saving to EDITO storage...")
    print(f"Bucket: {bucket_name}")
    print(f"Folder: {folder_name}")
    
    try:
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as CSV
        csv_key = f"{folder_name}/combined_marine_data_{timestamp}.csv"
        csv_buffer = combined_df.to_csv(index=False)
        s3_client.put_object(
            Bucket=bucket_name,
            Key=csv_key,
            Body=csv_buffer,
            ContentType='text/csv'
        )
        print(f"✅ CSV saved: s3://{bucket_name}/{csv_key}")
        
        # Save as Parquet
        parquet_key = f"{folder_name}/combined_marine_data_{timestamp}.parquet"
        try:
            parquet_buffer = combined_df.to_parquet(index=False)
            s3_client.put_object(
                Bucket=bucket_name,
                Key=parquet_key,
                Body=parquet_buffer,
                ContentType='application/octet-stream'
            )
            print(f"✅ Parquet saved: s3://{bucket_name}/{parquet_key}")
        except Exception as e:
            print(f"⚠️ Could not save parquet to storage: {e}")
            print("ℹ️ CSV file saved to storage successfully")
        
        # Save metadata
        metadata = {
            'created_at': datetime.now().isoformat(),
            'total_rows': len(combined_df),
            'total_columns': len(combined_df.columns),
            'data_sources': combined_df['data_source'].value_counts().to_dict(),
            'collections': combined_df['collection'].value_counts().to_dict()
        }
        
        metadata_key = f"{folder_name}/metadata_{timestamp}.json"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=metadata_key,
            Body=json.dumps(metadata, indent=2),
            ContentType='application/json'
        )
        print(f"✅ Metadata saved: s3://{bucket_name}/{metadata_key}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving to storage: {e}")
        return False

def main():
    """Main function"""
    print("🌊 EDITO Datalab: Simple Data Combination and Storage")
    print("=" * 60)
    
    # Load available assets
    parquet_items = load_parquet_items()
    zarr_items = load_zarr_items()
    
    if not parquet_items and not zarr_items:
        print("❌ No assets available. Run the search scripts first.")
        return
    
    # Select parquet asset
    parquet_item, parquet_assets = select_parquet_asset(parquet_items)
    if not parquet_item:
        print("❌ No parquet asset selected")
        return
    
    # Select zarr asset
    zarr_item, zarr_asset = select_zarr_asset(zarr_items)
    if not zarr_item:
        print("❌ No zarr asset selected")
        return
    
    # Process assets
    parquet_df = process_parquet_asset(parquet_item, parquet_assets)
    zarr_df = process_zarr_asset(zarr_item, zarr_asset)
    
    if parquet_df.empty or zarr_df.empty:
        print("❌ Failed to process one or both assets")
        return
    
    # Combine datasets
    combined_df = combine_datasets(parquet_df, zarr_df)
    if combined_df.empty:
        print("❌ Failed to combine datasets")
        return
    
    # Save locally first
    print(f"\n💾 Saving locally...")
    os.makedirs('output', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Clean data for parquet compatibility
    print("🧹 Cleaning data for parquet compatibility...")
    cleaned_df = combined_df.copy()
    
    # Convert object columns to string to avoid parquet conversion issues
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            # Convert to string, handling NaN values
            cleaned_df[col] = cleaned_df[col].astype(str).replace('nan', '')
    
    # Save CSV (no issues with mixed types)
    cleaned_df.to_csv(f'output/combined_marine_data_{timestamp}.csv', index=False)
    print(f"✅ CSV saved: output/combined_marine_data_{timestamp}.csv")
    
    # Save parquet (with cleaned data)
    try:
        cleaned_df.to_parquet(f'output/combined_marine_data_{timestamp}.parquet', index=False)
        print(f"✅ Parquet saved: output/combined_marine_data_{timestamp}.parquet")
    except Exception as e:
        print(f"⚠️ Could not save parquet file: {e}")
        print("ℹ️ CSV file saved successfully")
    
    print(f"✅ Local files saved to output/")
    
    # Connect to storage
    s3_client = connect_to_storage()
    if not s3_client:
        print("ℹ️ Data saved locally only")
        return
    
    # Get storage details
    bucket_name = input("\nEnter bucket name: ").strip()
    if not bucket_name:
        print("❌ Bucket name required")
        return
    
    folder_name = input("Enter folder name (default: combined_data): ").strip() or "combined_data"
    
    # Save to storage
    success = save_to_storage(cleaned_df, s3_client, bucket_name, folder_name)
    
    if success:
        print(f"\n🎉 Successfully combined and saved data!")
        print(f"📊 Combined dataset: {len(combined_df)} rows, {len(combined_df.columns)} columns")
    else:
        print(f"\n❌ Failed to save to storage, but data is saved locally")

if __name__ == "__main__":
    main()
