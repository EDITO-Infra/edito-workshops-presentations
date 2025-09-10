# =============================================================================
# EDITO Datalab Tutorial: Personal Storage with Python
# =============================================================================
# This script demonstrates how to connect to and use personal storage
# on EDITO Datalab using Python and boto3 for marine data

import boto3
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. SETUP: CONNECTING TO PERSONAL STORAGE
# =============================================================================

print("🌊 EDITO Datalab Personal Storage Tutorial")
print("=" * 50)

# Your personal storage credentials are automatically available in EDITO
# These environment variables are set when you launch a service

# Check if storage credentials are available
required_env_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_S3_ENDPOINT', 'AWS_DEFAULT_REGION']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if not missing_vars:
    print("✅ Personal storage credentials found!")
    print(f"Storage endpoint: {os.getenv('AWS_S3_ENDPOINT')}")
    print(f"Region: {os.getenv('AWS_DEFAULT_REGION')}")
else:
    print(f"❌ Missing environment variables: {missing_vars}")
    print("Make sure you're running in EDITO Datalab with storage enabled.")

# =============================================================================
# 2. CONNECTING TO MINIO (EDITO's S3-compatible storage)
# =============================================================================

# Set up boto3 client for MinIO
# This uses the same interface as Amazon S3 but connects to EDITO's storage

try:
    s3_client = boto3.client(
        's3',
        endpoint_url=f"https://{os.getenv('AWS_S3_ENDPOINT')}",
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
        region_name=os.getenv('AWS_DEFAULT_REGION')
    )
    
    print("✅ Successfully connected to EDITO MinIO storage")
    
except Exception as e:
    print(f"❌ Error connecting to storage: {e}")
    s3_client = None

# =============================================================================
# 3. EXPLORING YOUR PERSONAL STORAGE
# =============================================================================

if s3_client:
    try:
        # List your personal buckets
        response = s3_client.list_buckets()
        buckets = response['Buckets']
        
        print(f"\nYour personal storage buckets ({len(buckets)} found):")
        for bucket in buckets:
            print(f"  - {bucket['Name']} (created: {bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')})")
        
        # Use the first bucket as your personal bucket
        if buckets:
            personal_bucket = buckets[0]['Name']
            print(f"\nUsing personal bucket: {personal_bucket}")
        else:
            print("No buckets found. This might be normal for a new account.")
            personal_bucket = None
            
    except Exception as e:
        print(f"❌ Error listing buckets: {e}")
        personal_bucket = None

# =============================================================================
# 4. WORKING WITH YOUR PERSONAL BUCKET
# =============================================================================

if s3_client and personal_bucket:
    try:
        # List contents of your personal bucket
        response = s3_client.list_objects_v2(Bucket=personal_bucket)
        
        if 'Contents' in response:
            print(f"\nContents of bucket '{personal_bucket}':")
            for obj in response['Contents']:
                print(f"  - {obj['Key']} ({obj['Size']} bytes, {obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print(f"\nBucket '{personal_bucket}' is empty (this is normal for a new bucket)")
            
    except Exception as e:
        print(f"❌ Error listing bucket contents: {e}")

# =============================================================================
# 5. SAVING DATA TO PERSONAL STORAGE
# =============================================================================

print("\n" + "=" * 50)
print("💾 SAVING DATA TO PERSONAL STORAGE")
print("=" * 50)

# Create some sample marine data
np.random.seed(42)
n_points = 500

marine_data = pd.DataFrame({
    'station_id': np.repeat(range(1, 51), n_points // 50),
    'timestamp': pd.date_range('2024-01-01', '2024-12-31', periods=n_points),
    'latitude': np.random.uniform(50, 60, n_points),
    'longitude': np.random.uniform(0, 10, n_points),
    'depth': np.random.uniform(5, 200, n_points),
    'temperature': np.random.normal(10, 3, n_points),
    'salinity': np.random.normal(35, 1, n_points),
    'chlorophyll_a': np.random.exponential(1, n_points),
    'turbidity': np.random.exponential(0.5, n_points)
})

print(f"Created sample marine dataset with {len(marine_data)} observations")
print("\nFirst few records:")
print(marine_data.head())

# Save data to personal storage
if s3_client and personal_bucket:
    try:
        # Save as CSV
        csv_key = "marine_data/marine_observations.csv"
        csv_buffer = marine_data.to_csv(index=False)
        s3_client.put_object(
            Bucket=personal_bucket,
            Key=csv_key,
            Body=csv_buffer,
            ContentType='text/csv'
        )
        print(f"✅ Marine data saved as CSV: {csv_key}")
        
        # Save as Parquet (more efficient for large datasets)
        parquet_key = "marine_data/marine_observations.parquet"
        parquet_buffer = marine_data.to_parquet(index=False)
        s3_client.put_object(
            Bucket=personal_bucket,
            Key=parquet_key,
            Body=parquet_buffer,
            ContentType='application/octet-stream'
        )
        print(f"✅ Marine data saved as Parquet: {parquet_key}")
        
        # Save metadata
        metadata = {
            'dataset_name': 'Marine Observations Data',
            'description': 'Sample marine data for EDITO tutorial',
            'created_date': datetime.now().isoformat(),
            'total_records': len(marine_data),
            'station_count': marine_data['station_id'].nunique(),
            'date_range': {
                'start': marine_data['timestamp'].min().isoformat(),
                'end': marine_data['timestamp'].max().isoformat()
            },
            'spatial_extent': {
                'min_lat': float(marine_data['latitude'].min()),
                'max_lat': float(marine_data['latitude'].max()),
                'min_lon': float(marine_data['longitude'].min()),
                'max_lon': float(marine_data['longitude'].max())
            }
        }
        
        metadata_key = "marine_data/metadata.json"
        s3_client.put_object(
            Bucket=personal_bucket,
            Key=metadata_key,
            Body=json.dumps(metadata, indent=2),
            ContentType='application/json'
        )
        print(f"✅ Metadata saved: {metadata_key}")
        
    except Exception as e:
        print(f"❌ Error saving data: {e}")

# =============================================================================
# 6. READING DATA FROM PERSONAL STORAGE
# =============================================================================

print("\n" + "=" * 50)
print("📖 READING DATA FROM PERSONAL STORAGE")
print("=" * 50)

if s3_client and personal_bucket:
    try:
        # Read CSV data
        csv_key = "fish_tracking/fish_tracking_data.csv"
        response = s3_client.get_object(Bucket=personal_bucket, Key=csv_key)
        loaded_csv = pd.read_csv(response['Body'])
        print(f"✅ Loaded CSV data: {len(loaded_csv)} records")
        print(f"Columns: {list(loaded_csv.columns)}")
        
        # Read Parquet data
        parquet_key = "fish_tracking/fish_tracking_data.parquet"
        response = s3_client.get_object(Bucket=personal_bucket, Key=parquet_key)
        loaded_parquet = pd.read_parquet(response['Body'])
        print(f"✅ Loaded Parquet data: {len(loaded_parquet)} records")
        
        # Read metadata
        metadata_key = "fish_tracking/metadata.json"
        response = s3_client.get_object(Bucket=personal_bucket, Key=metadata_key)
        metadata = json.loads(response['Body'].read().decode('utf-8'))
        print(f"✅ Loaded metadata:")
        print(json.dumps(metadata, indent=2))
        
    except Exception as e:
        print(f"❌ Error reading data: {e}")

# =============================================================================
# 7. WORKING WITH LARGER DATASETS
# =============================================================================

print("\n" + "=" * 50)
print("📊 WORKING WITH LARGER DATASETS")
print("=" * 50)

# For larger datasets, you can work directly with files in storage
# without loading everything into memory

if s3_client and personal_bucket:
    try:
        # Create a larger dataset
        print("Creating larger dataset...")
        large_dataset = pd.DataFrame({
            'fish_id': np.repeat(range(1, 1001), 100),  # 1000 fish, 100 observations each
            'timestamp': pd.date_range('2020-01-01', '2024-01-01', periods=100000),
            'latitude': np.random.uniform(45, 65, 100000),
            'longitude': np.random.uniform(-5, 15, 100000),
            'depth': np.random.uniform(1, 500, 100000),
            'temperature': np.random.normal(8, 4, 100000),
            'salinity': np.random.normal(34, 2, 100000)
        })
        
        print(f"Created large dataset with {len(large_dataset)} records")
        
        # Save large dataset in chunks (memory efficient)
        chunk_size = 10000
        for i in range(0, len(large_dataset), chunk_size):
            chunk = large_dataset.iloc[i:i+chunk_size]
            chunk_key = f"large_datasets/fish_tracking_chunk_{i//chunk_size:03d}.parquet"
            
            parquet_buffer = chunk.to_parquet(index=False)
            s3_client.put_object(
                Bucket=personal_bucket,
                Key=chunk_key,
                Body=parquet_buffer,
                ContentType='application/octet-stream'
            )
        
        print(f"✅ Large dataset saved in {(len(large_dataset) // chunk_size) + 1} chunks")
        
        # List the chunks
        response = s3_client.list_objects_v2(Bucket=personal_bucket, Prefix="large_datasets/")
        if 'Contents' in response:
            print(f"Chunks created: {len(response['Contents'])}")
            for obj in response['Contents'][:5]:  # Show first 5
                print(f"  - {obj['Key']} ({obj['Size']} bytes)")
        
    except Exception as e:
        print(f"❌ Error with large dataset: {e}")

# =============================================================================
# 8. DATA SHARING AND COLLABORATION
# =============================================================================

print("\n" + "=" * 50)
print("🤝 DATA SHARING AND COLLABORATION")
print("=" * 50)

if s3_client and personal_bucket:
    try:
        # List all your data files
        response = s3_client.list_objects_v2(Bucket=personal_bucket)
        
        if 'Contents' in response:
            print("Your data files:")
            for obj in response['Contents']:
                print(f"  - {obj['Key']} ({obj['Size']} bytes)")
            
            print(f"\nTotal files: {len(response['Contents'])}")
            total_size = sum(obj['Size'] for obj in response['Contents'])
            print(f"Total size: {total_size / (1024*1024):.2f} MB")
        
        print("\n=== SHARING OPTIONS ===")
        print("1. Share bucket/object names with collaborators")
        print("2. Generate pre-signed URLs for temporary access")
        print("3. Make objects publicly readable (if needed)")
        print("4. Export data to external services")
        print("5. Use EDITO's data sharing features")
        
    except Exception as e:
        print(f"❌ Error listing files: {e}")

# =============================================================================
# 9. BEST PRACTICES FOR FISH TRACKING DATA
# =============================================================================

print("\n" + "=" * 50)
print("📋 BEST PRACTICES FOR FISH TRACKING DATA")
print("=" * 50)

best_practices = [
    "Use Parquet format for large datasets (faster, smaller)",
    "Organize data in folders (e.g., fish_tracking/, environmental_data/)",
    "Include metadata files describing your data",
    "Use consistent naming conventions",
    "Regular backups of important datasets",
    "Document your data processing steps",
    "Use version control for your code",
    "Share data with proper attribution",
    "Consider data privacy and sharing policies",
    "Test data integrity regularly"
]

print("Best practices for managing fish tracking data:")
for i, practice in enumerate(best_practices, 1):
    print(f"{i:2d}. {practice}")

# =============================================================================
# 10. CLEANUP AND NEXT STEPS
# =============================================================================

print("\n" + "=" * 50)
print("🚀 NEXT STEPS")
print("=" * 50)

print("1. 🐍 Try the RStudio service for R-based analysis")
print("2. 🔧 Use VSCode for larger projects")
print("3. 📊 Explore more data analysis techniques")
print("4. 🌊 Access real environmental data from EDITO")
print("5. 🤝 Learn about data sharing and collaboration")
print("6. 📚 Check out the R Markdown tutorial")

print("\n✅ Personal storage tutorial completed!")
print("You now know how to save and manage your fish tracking data on EDITO!")
