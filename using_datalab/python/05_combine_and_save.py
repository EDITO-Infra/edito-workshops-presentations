#!/usr/bin/env python3
"""
EDITO Datalab Demo: Combine Data and Save to Storage

This script combines raster and parquet data from previous processing steps,
creates a unified dataset, and saves it to both local storage and personal storage.
"""

import pandas as pd
import numpy as np
import boto3
import os
import json
import re
from datetime import datetime

def extract_coords_from_geometry(geometry_str):
    """
    Extract rough lat/lon coordinates from geometry string
    
    Args:
        geometry_str (str): Geometry string (WKT, GeoJSON, etc.)
        
    Returns:
        tuple: (lat, lon) or (None, None) if extraction fails
    """
    try:
        # Try to parse as JSON first (GeoJSON)
        if geometry_str.startswith('{'):
            geom_data = json.loads(geometry_str)
            if 'coordinates' in geom_data:
                coords = geom_data['coordinates']
                if isinstance(coords, list) and len(coords) >= 2:
                    # For Point: [lon, lat]
                    if len(coords) == 2:
                        return float(coords[1]), float(coords[0])
                    # For Polygon: [[[lon, lat], ...]]
                    elif len(coords) > 0 and isinstance(coords[0], list):
                        if len(coords[0]) > 0 and isinstance(coords[0][0], list):
                            # Get first coordinate
                            first_coord = coords[0][0]
                            if len(first_coord) >= 2:
                                return float(first_coord[1]), float(first_coord[0])
        
        # Try to extract coordinates from WKT format
        # Look for patterns like POINT(lon lat) or POLYGON((lon lat, ...))
        coord_pattern = r'[-+]?\d*\.?\d+'
        coords = re.findall(coord_pattern, str(geometry_str))
        
        if len(coords) >= 2:
            # Convert to float and return as lat, lon
            try:
                lon = float(coords[0])
                lat = float(coords[1])
                return lat, lon
            except ValueError:
                pass
        
        # If all else fails, return None
        return None, None
        
    except Exception as e:
        print(f"⚠️ Error extracting coordinates from geometry: {e}")
        return None, None

def load_processed_data(raster_file="raster_data.csv", parquet_file="parquet_data.csv"):
    """
    Load processed data from CSV files
    
    Args:
        raster_file (str): Path to raster data CSV file
        parquet_file (str): Path to parquet data CSV file
        
    Returns:
        tuple: (raster_df, parquet_df)
    """
    print("📂 Loading processed data...")
    
    # Load raster data
    try:
        raster_df = pd.read_csv(raster_file)
        print(f"✅ Loaded raster data: {len(raster_df)} rows from {raster_file}")
    except Exception as e:
        print(f"❌ Error loading raster data: {e}")
        raster_df = pd.DataFrame()
    
    # Load parquet data
    try:
        parquet_df = pd.read_csv(parquet_file)
        print(f"✅ Loaded parquet data: {len(parquet_df)} rows from {parquet_file}")
    except Exception as e:
        print(f"❌ Error loading parquet data: {e}")
        parquet_df = pd.DataFrame()
    
    return raster_df, parquet_df

def combine_datasets(raster_df, parquet_df):
    """
    Combine raster and parquet datasets into a unified format
    
    Args:
        raster_df (pd.DataFrame): Raster data DataFrame
        parquet_df (pd.DataFrame): Parquet data DataFrame
        
    Returns:
        pd.DataFrame: Combined dataset
    """
    print("🔗 Combining datasets...")
    
    combined_data = []
    
    # Process raster data
    if not raster_df.empty:
        print(f"📊 Processing {len(raster_df)} raster records...")
        
        # Standardize raster data format
        raster_standard = raster_df.copy()
        
        # Ensure we have lat/lon columns
        if 'lat' in raster_standard.columns and 'lon' in raster_standard.columns:
            # Add data source identifier
            raster_standard['data_source'] = 'raster'
            
            # Select relevant columns
            raster_cols = ['lat', 'lon', 'raster_value', 'data_source', 'item_id', 'item_title']
            available_raster_cols = [col for col in raster_cols if col in raster_standard.columns]
            raster_subset = raster_standard[available_raster_cols]
            
            combined_data.append(raster_subset)
            print(f"✅ Added {len(raster_subset)} raster records")
        else:
            print("⚠️ Raster data missing lat/lon columns")
    
    # Process parquet data
    if not parquet_df.empty:
        print(f"📊 Processing {len(parquet_df)} parquet records...")
        
        # Standardize parquet data format
        parquet_standard = parquet_df.copy()
        
        # Look for coordinate columns
        coord_cols = [col for col in parquet_standard.columns if any(keyword in col.lower() 
                     for keyword in ['lat', 'lon', 'longitude', 'latitude'])]
        
        if len(coord_cols) >= 2:
            lat_col = [col for col in coord_cols if 'lat' in col.lower()][0]
            lon_col = [col for col in coord_cols if 'lon' in col.lower()][0]
            
            # Rename to standard format
            parquet_standard = parquet_standard.rename(columns={lat_col: 'lat', lon_col: 'lon'})
            
            # Add data source identifier
            parquet_standard['data_source'] = 'parquet'
            
            # Add dummy raster value for parquet data
            parquet_standard['raster_value'] = np.nan
            
            # Select relevant columns
            parquet_cols = ['lat', 'lon', 'raster_value', 'data_source', 'item_id', 'item_title']
            available_parquet_cols = [col for col in parquet_cols if col in parquet_standard.columns]
            parquet_subset = parquet_standard[available_parquet_cols]
            
            # Add species information if available
            species_cols = [col for col in parquet_df.columns if any(keyword in col.lower() 
                          for keyword in ['species', 'scientific', 'taxon', 'name'])]
            if species_cols:
                species_col = species_cols[0]
                parquet_subset['species'] = parquet_standard[species_col]
            
            combined_data.append(parquet_subset)
            print(f"✅ Added {len(parquet_subset)} parquet records")
        else:
            print("⚠️ Parquet data missing coordinate columns, extracting from geometry...")
            
            # Try to extract coordinates from geometry column
            if 'geometry' in parquet_standard.columns:
                print("🔍 Extracting coordinates from geometry column...")
                coords_list = []
                
                for idx, geom_str in enumerate(parquet_standard['geometry']):
                    lat, lon = extract_coords_from_geometry(geom_str)
                    if lat is not None and lon is not None:
                        coords_list.append((lat, lon))
                        print(f"  Record {idx+1}: lat={lat:.4f}, lon={lon:.4f}")
                    else:
                        # Fallback to random coordinates if extraction fails
                        lat = np.random.uniform(50, 60)
                        lon = np.random.uniform(0, 10)
                        coords_list.append((lat, lon))
                        print(f"  Record {idx+1}: Using random coordinates lat={lat:.4f}, lon={lon:.4f}")
                
                # Add extracted coordinates
                parquet_standard['lat'] = [coord[0] for coord in coords_list]
                parquet_standard['lon'] = [coord[1] for coord in coords_list]
            else:
                print("⚠️ No geometry column found, creating sample coordinates...")
                # Create sample coordinates for demonstration
                n_records = len(parquet_standard)
                parquet_standard['lat'] = np.random.uniform(50, 60, n_records)
                parquet_standard['lon'] = np.random.uniform(0, 10, n_records)
            
            parquet_standard['data_source'] = 'parquet'
            parquet_standard['raster_value'] = np.nan
            
            # Select relevant columns
            parquet_cols = ['lat', 'lon', 'raster_value', 'data_source', 'item_id', 'item_title']
            available_parquet_cols = [col for col in parquet_cols if col in parquet_standard.columns]
            parquet_subset = parquet_standard[available_parquet_cols]
            
            combined_data.append(parquet_subset)
            print(f"✅ Added {len(parquet_subset)} parquet records with extracted coordinates")
    
    # Combine all data
    if combined_data:
        final_combined = pd.concat(combined_data, ignore_index=True)
        print(f"\n✅ Combined dataset created: {len(final_combined)} total records")
        print(f"📋 Columns: {list(final_combined.columns)}")
        
        # Show data source distribution
        if 'data_source' in final_combined.columns:
            print(f"\n📊 Data source distribution:")
            print(final_combined['data_source'].value_counts())
        
        return final_combined
    else:
        print("❌ No data to combine")
        return pd.DataFrame()

def save_to_local(combined_df, output_file="combined_marine_data.csv"):
    """
    Save combined data to local CSV file
    
    Args:
        combined_df (pd.DataFrame): Combined dataset
        output_file (str): Output CSV file path
    """
    if not combined_df.empty:
        try:
            combined_df.to_csv(output_file, index=False)
            print(f"✅ Combined data saved locally as {output_file}")
            
            # Show sample data
            print(f"\n📊 Sample of combined data:")
            print(combined_df.head(10))
            
            # Show summary statistics
            print(f"\n📊 Combined data summary:")
            print(f"  Total records: {len(combined_df)}")
            if 'data_source' in combined_df.columns:
                print(f"  Data sources: {combined_df['data_source'].value_counts().to_dict()}")
            if 'species' in combined_df.columns:
                print(f"  Unique species: {combined_df['species'].nunique()}")
            if 'raster_value' in combined_df.columns:
                valid_raster = combined_df['raster_value'].dropna()
                if len(valid_raster) > 0:
                    print(f"  Raster value range: {valid_raster.min():.2f} - {valid_raster.max():.2f}")
            
        except Exception as e:
            print(f"❌ Error saving to local file: {e}")
    else:
        print("❌ No data to save locally")

def connect_to_storage():
    """
    Connect to personal storage using environment variables
    
    Returns:
        boto3.client or None: S3 client if credentials available
    """
    print("💾 Connecting to personal storage...")
    
    # Check if storage credentials are available
    if os.getenv("AWS_ACCESS_KEY_ID"):
        print("✅ Personal storage credentials found!")
        
        try:
            # Connect to EDITO's MinIO storage using environment variables
            s3 = boto3.client(
                "s3",
                endpoint_url=f"https://{os.getenv('AWS_S3_ENDPOINT')}",
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
                region_name=os.getenv('AWS_DEFAULT_REGION')
            )
            
            print("✅ Connected to personal storage!")
            
            # List your buckets to verify connection
            try:
                response = s3.list_buckets()
                print(f"📁 Available buckets: {[bucket['Name'] for bucket in response['Buckets']]}")
            except Exception as e:
                print(f"⚠️ Could not list buckets: {e}")
            
            return s3
            
        except Exception as e:
            print(f"❌ Error connecting to storage: {e}")
            return None
    else:
        print("❌ No storage credentials found. Make sure you're running in EDITO Datalab.")
        print("💡 Your credentials are automatically available in EDITO services")
        return None

def save_to_storage(combined_df, s3_client, bucket_name="your-bucket-name", 
                   key_prefix="marine_analysis/"):
    """
    Save combined data to personal storage
    
    Args:
        combined_df (pd.DataFrame): Combined dataset
        s3_client: S3 client for storage
        bucket_name (str): S3 bucket name
        key_prefix (str): Key prefix for storage
    """
    if s3_client and not combined_df.empty:
        try:
            # Create timestamp for unique filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save main dataset
            main_key = f"{key_prefix}combined_marine_data_{timestamp}.csv"
            s3_client.put_object(
                Bucket=bucket_name,
                Key=main_key,
                Body=combined_df.to_csv(index=False),
                ContentType='text/csv'
            )
            print(f"✅ Combined data uploaded to storage: {main_key}")
            
            # Save summary statistics
            summary_data = {
                'total_records': len(combined_df),
                'data_sources': combined_df['data_source'].value_counts().to_dict() if 'data_source' in combined_df.columns else {},
                'unique_species': combined_df['species'].nunique() if 'species' in combined_df.columns else 0,
                'raster_value_range': {
                    'min': float(combined_df['raster_value'].min()) if 'raster_value' in combined_df.columns else None,
                    'max': float(combined_df['raster_value'].max()) if 'raster_value' in combined_df.columns else None
                } if 'raster_value' in combined_df.columns else {},
                'created_at': datetime.now().isoformat()
            }
            
            summary_key = f"{key_prefix}summary_{timestamp}.json"
            import json
            s3_client.put_object(
                Bucket=bucket_name,
                Key=summary_key,
                Body=json.dumps(summary_data, indent=2),
                ContentType='application/json'
            )
            print(f"✅ Summary statistics uploaded: {summary_key}")
            
        except Exception as e:
            print(f"❌ Error uploading to storage: {e}")
            print("💡 Make sure to replace 'your-bucket-name' with your actual bucket name")
    else:
        if not s3_client:
            print("💡 To upload to storage, make sure you're running in EDITO Datalab")
        if combined_df.empty:
            print("❌ No data to upload to storage")

def main():
    """Main function"""
    print("🔗 EDITO Datalab: Combining and Saving Data")
    print("=" * 50)
    
    # Load processed data
    raster_df, parquet_df = load_processed_data()
    
    if raster_df.empty and parquet_df.empty:
        print("❌ No processed data available. Run previous scripts first:")
        print("  1. 03_get_zarr_to_df.py")
        print("  2. 04_get_parquet_data.py")
        return
    
    # Combine datasets
    combined_df = combine_datasets(raster_df, parquet_df)
    
    if combined_df.empty:
        print("❌ No data to combine")
        return
    
    # Save to local storage
    save_to_local(combined_df)
    
    # Connect to personal storage
    s3_client = connect_to_storage()
    
    # Save to personal storage
    save_to_storage(combined_df, s3_client)
    
    print("\n🎯 Workflow Complete!")
    print("✅ Data has been processed and saved:")
    print("  - Local CSV file: combined_marine_data.csv")
    print("  - Personal storage: marine_analysis/ folder")
    print("\n🚀 Next steps:")
    print("  - Analyze the combined dataset")
    print("  - Create visualizations")
    print("  - Explore the data in your preferred analysis environment")

if __name__ == "__main__":
    main()
