#!/usr/bin/env python3
"""
EDITO Datalab Demo: Interactive Data Processing and Storage

This script provides an interactive interface for:
- Selecting STAC collections
- Choosing datasets to overlay
- Selecting storage buckets and folders
- Saving processed data to personal storage
"""

import pandas as pd
import numpy as np
import boto3
import os
import json
import re
import requests
import logging
from datetime import datetime
from collections import defaultdict
from using_storage import connect_to_storage, save_to_storage_interactive

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

def get_stac_collections():
    """
    Get available STAC collections from EDITO API

    Returns:
        dict: Full collections response with 'collections' key
    """
    logger = logging.getLogger(__name__)
    logger.info("🔍 Fetching available STAC collections...")
    logger.info("⏳ This may take a moment...")

    try:
        stac_endpoint = "https://api.dive.edito.eu/data/"
        logger.info(f"📡 Connecting to: {stac_endpoint}collections")

        # Add timeout to prevent hanging
        response = requests.get(f"{stac_endpoint}collections", timeout=30)

        logger.info(f"📊 Response status: {response.status_code}")

        if response.status_code == 200:
            logger.info("📥 Parsing response...")
            collections_data = response.json()
            collections = collections_data.get('collections', [])
            logger.info(f"✅ Found {len(collections)} collections")
            return collections_data
        else:
            logger.error(f"❌ Failed to fetch collections: HTTP {response.status_code}")
            logger.error(f"Response: {response.text[:200]}...")
            return None
    except requests.exceptions.Timeout:
        logger.error("❌ Request timed out. The API might be slow or unavailable.")
        logger.info("💡 Try running the script again, or check your internet connection.")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("❌ Connection error. Please check your internet connection.")
        return None
    except Exception as e:
        logger.error(f"❌ Error fetching collections: {e}")
        return None

def select_collection(collections):
    """
    Interactive collection selection
    
    Args:
        collections (list): List of collection dictionaries
        
    Returns:
        str: Selected collection ID
    """
    if not collections:
        print("❌ No collections available")
        return None
    
    print("\n📋 Available collections:")
    for i, collection in enumerate(collections[:20]):  # Show first 20
        title = collection.get('title', 'No title')
        collection_id = collection.get('id', 'No ID')
        print(f"{i+1:2d}. {collection_id} - {title}")
    
    if len(collections) > 20:
        print(f"    ... and {len(collections) - 20} more collections")
    
    while True:
        try:
            choice = input(f"\n🎯 Select collection (1-{min(20, len(collections))}): ").strip()
            if choice.lower() == 'q':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= min(20, len(collections)):
                selected_collection = collections[choice_num - 1]
                print(f"✅ Selected: {selected_collection['id']} - {selected_collection.get('title', 'No title')}")
                return selected_collection['id']
            else:
                print(f"❌ Please enter a number between 1 and {min(20, len(collections))}")
        except ValueError:
            print("❌ Please enter a valid number or 'q' to quit")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None

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
            return s3
            
        except Exception as e:
            print(f"❌ Error connecting to storage: {e}")
            return None
    else:
        print("❌ No storage credentials found. Make sure you're running in EDITO Datalab.")
        print("💡 Your credentials are automatically available in EDITO services")
        return None

def list_buckets(s3_client):
    """
    List available buckets and let user select one
    
    Args:
        s3_client: S3 client
        
    Returns:
        str: Selected bucket name
    """
    try:
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        
        if not buckets:
            print("❌ No buckets found")
            return None
        
        print(f"\n📁 Available buckets ({len(buckets)}):")
        for i, bucket in enumerate(buckets):
            print(f"{i+1:2d}. {bucket}")
        
        while True:
            try:
                choice = input(f"\n🎯 Select bucket (1-{len(buckets)}): ").strip()
                if choice.lower() == 'q':
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(buckets):
                    selected_bucket = buckets[choice_num - 1]
                    print(f"✅ Selected bucket: {selected_bucket}")
                    return selected_bucket
                else:
                    print(f"❌ Please enter a number between 1 and {len(buckets)}")
            except ValueError:
                print("❌ Please enter a valid number or 'q' to quit")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return None
                
    except Exception as e:
        print(f"❌ Error listing buckets: {e}")
        return None

def list_folders(s3_client, bucket_name):
    """
    List folders in the selected bucket
    
    Args:
        s3_client: S3 client
        bucket_name (str): Bucket name
        
    Returns:
        list: List of folder names
    """
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')
        folders = []
        
        if 'CommonPrefixes' in response:
            folders = [prefix['Prefix'].rstrip('/') for prefix in response['CommonPrefixes']]
        
        print(f"\n📁 Available folders in '{bucket_name}' ({len(folders)}):")
        if folders:
            for i, folder in enumerate(folders):
                print(f"{i+1:2d}. {folder}")
        else:
            print("   No folders found (bucket is empty or has no folders)")
        
        return folders
        
    except Exception as e:
        print(f"❌ Error listing folders: {e}")
        return []

def select_folder(s3_client, bucket_name, folders):
    """
    Let user select a folder or create a new one
    
    Args:
        s3_client: S3 client
        bucket_name (str): Bucket name
        folders (list): List of available folders
        
    Returns:
        str: Selected folder path
    """
    while True:
        print(f"\n🎯 Folder options:")
        print("1. Create new folder")
        if folders:
            print("2. Select existing folder")
            print("3. Use root directory (no folder)")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            folder_name = input("Enter new folder name: ").strip()
            if folder_name:
                folder_path = f"{folder_name}/"
                print(f"✅ Will create folder: {folder_path}")
                return folder_path
            else:
                print("❌ Please enter a valid folder name")
        
        elif choice == '2' and folders:
            print("\nSelect existing folder:")
            for i, folder in enumerate(folders):
                print(f"{i+1:2d}. {folder}")
            
            try:
                folder_choice = int(input(f"Enter choice (1-{len(folders)}): "))
                if 1 <= folder_choice <= len(folders):
                    selected_folder = folders[folder_choice - 1] + "/"
                    print(f"✅ Selected folder: {selected_folder}")
                    return selected_folder
                else:
                    print(f"❌ Please enter a number between 1 and {len(folders)}")
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == '3':
            print("✅ Using root directory")
            return ""
        
        else:
            print("❌ Invalid choice. Please try again.")

def save_to_storage_interactive(combined_df, s3_client, collection_id=None):
    """
    Interactive save to personal storage with bucket and folder selection
    
    Args:
        combined_df (pd.DataFrame): Combined dataset
        s3_client: S3 client for storage
        collection_id (str): Selected collection ID for naming
    """
    if not s3_client or combined_df.empty:
        if not s3_client:
            print("💡 To upload to storage, make sure you're running in EDITO Datalab")
        if combined_df.empty:
            print("❌ No data to upload to storage")
        return
    
    print("\n💾 Saving to Personal Storage")
    print("=" * 40)
    
    # Select bucket
    bucket_name = list_buckets(s3_client)
    if not bucket_name:
        print("❌ No bucket selected. Skipping storage upload.")
        return
    
    # List and select folder
    folders = list_folders(s3_client, bucket_name)
    folder_path = select_folder(s3_client, bucket_name, folders)
    if folder_path is None:
        print("❌ No folder selected. Skipping storage upload.")
        return
    
    # Generate filename based on collection and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if collection_id:
        filename = f"marine_data_{collection_id}_{timestamp}.csv"
        summary_filename = f"summary_{collection_id}_{timestamp}.json"
    else:
        filename = f"marine_data_{timestamp}.csv"
        summary_filename = f"summary_{timestamp}.json"
    
    try:
        # Save main dataset
        main_key = f"{folder_path}{filename}"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=main_key,
            Body=combined_df.to_csv(index=False),
            ContentType='text/csv'
        )
        print(f"✅ Combined data uploaded: s3://{bucket_name}/{main_key}")
        
        # Save summary statistics
        summary_data = {
            'collection_id': collection_id,
            'total_records': len(combined_df),
            'data_sources': combined_df['data_source'].value_counts().to_dict() if 'data_source' in combined_df.columns else {},
            'unique_species': combined_df['species'].nunique() if 'species' in combined_df.columns else 0,
            'raster_value_range': {
                'min': float(combined_df['raster_value'].min()) if 'raster_value' in combined_df.columns else None,
                'max': float(combined_df['raster_value'].max()) if 'raster_value' in combined_df.columns else None
            } if 'raster_value' in combined_df.columns else {},
            'created_at': datetime.now().isoformat(),
            'bucket': bucket_name,
            'folder': folder_path
        }
        
        summary_key = f"{folder_path}{summary_filename}"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=summary_key,
            Body=json.dumps(summary_data, indent=2),
            ContentType='application/json'
        )
        print(f"✅ Summary statistics uploaded: s3://{bucket_name}/{summary_key}")
        
        print(f"\n🎯 Files saved successfully!")
        print(f"   📁 Bucket: {bucket_name}")
        print(f"   📂 Folder: {folder_path}")
        print(f"   📊 Data file: {filename}")
        print(f"   📋 Summary file: {summary_filename}")
        
    except Exception as e:
        print(f"❌ Error uploading to storage: {e}")

def create_sample_data(collection_id):
    """
    Create sample marine data for demonstration
    
    Args:
        collection_id (str): Collection ID for context
        
    Returns:
        pd.DataFrame: Sample marine data
    """
    print(f"📊 Creating sample marine data for collection: {collection_id}")
    
    # Create sample data
    np.random.seed(42)  # For reproducible results
    n_records = 100
    
    sample_data = pd.DataFrame({
        'scientificName': np.random.choice([
            'Scomber scombrus', 'Gadus morhua', 'Pleuronectes platessa',
            'Merlangius merlangus', 'Solea solea', 'Clupea harengus'
        ], n_records),
        'decimalLatitude': np.random.uniform(50, 60, n_records),
        'decimalLongitude': np.random.uniform(0, 10, n_records),
        'eventDate': pd.date_range('2020-01-01', '2023-12-31', periods=n_records),
        'depth': np.random.uniform(5, 200, n_records),
        'temperature': np.random.normal(10, 3, n_records),
        'data_source': 'parquet',
        'item_id': collection_id,
        'item_title': f'Sample data from {collection_id}',
        'raster_value': np.nan
    })
    
    print(f"✅ Created {len(sample_data)} sample records")
    return sample_data

def main():
    """Interactive main function"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Setup logging - simple and direct
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/edito_workflow.log', mode='a'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("🚀 Starting EDITO Datalab: Interactive Data Processing")
    logger.info("=" * 60)
    
    # Step 1: Get STAC collections
    collections_data = get_stac_collections()
    if not collections_data:
        logger.error("Could not fetch STAC collections.")
        logger.info("This might be due to network issues or API unavailability.")
        logger.info("Would you like to continue with sample data instead?")

        while True:
            choice = input("Continue with sample data? (y/n): ").strip().lower()
            if choice == 'y':
                logger.info("Continuing with sample data...")
                collection_id = "sample-collection"
                break
            elif choice == 'n':
                logger.info("Exiting. Please check your connection and try again.")
                return
            else:
                logger.error("Please enter 'y' or 'n'")
        
        # Skip to data processing with sample data
        combined_df = create_sample_data(collection_id)
        if combined_df.empty:
            logger.error("No data to process")
            return

        # Save to local storage
        logger.info("Saving data locally...")
        save_to_local(combined_df)

        # Connect to storage and save
        s3_client = connect_to_storage()
        if s3_client:
            save_to_storage_interactive(combined_df, s3_client, collection_id)

        logger.info("=" * 60)
        logger.info("✅ Sample data processing finished successfully!")
        logger.info("=" * 60)
        return
    
    # Extract the collections list from the response
    collections = collections_data.get('collections', [])
    if not collections:
        logger.error("No collections found in response. Exiting.")
        return

    # Step 2: Select collection
    collection_id = select_collection(collections)
    if not collection_id:
        logger.info("No collection selected. Exiting.")
        return

    # Step 3: Ask about data overlay
    logger.info(f"Data Processing Options for '{collection_id}':")
    print("1. Use existing processed data (from previous scripts)")
    print("2. Create sample data for demonstration")
    print("3. Search and process data from this collection")

    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == '1':
            # Try to load existing data
            raster_df, parquet_df = load_processed_data()
            if raster_df.empty and parquet_df.empty:
                logger.error("No existing data found. Creating sample data instead.")
                combined_df = create_sample_data(collection_id)
            else:
                combined_df = combine_datasets(raster_df, parquet_df)
            break
        elif choice == '2':
            # Create sample data
            combined_df = create_sample_data(collection_id)
            break
        elif choice == '3':
            logger.info("This would search and process data from the selected collection.")
            logger.info("For now, creating sample data instead.")
            combined_df = create_sample_data(collection_id)
            break
        else:
            logger.error("Invalid choice. Please enter 1, 2, or 3.")
    
    if combined_df.empty:
        logger.error("No data to process")
        return
    
    # Step 4: Save locally
    logger.info("Saving data locally...")
    save_to_local(combined_df)

    # Step 5: Connect to storage
    s3_client = connect_to_storage()
    if not s3_client:
        logger.error("Could not connect to storage. Data saved locally only.")
        return

    # Step 6: Interactive save to storage
    save_to_storage_interactive(combined_df, s3_client, collection_id)

    logger.info("=" * 60)
    logger.info("✅ Interactive data processing finished successfully!")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
