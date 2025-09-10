#!/usr/bin/env python3
"""
EDITO Datalab Demo: STAC, Parquet, and Zarr

This script demonstrates the core workflow of using EDITO Datalab:
1. **Find services** on the datalab website
2. **Configure services** (RStudio, Jupyter, VSCode)
3. **Run analysis** with STAC search, Parquet reading, and Zarr data

Perfect for a 15-minute tutorial! 🚀
"""

import requests
import json
import pyarrow.parquet as pq
import pyarrow as pa
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
import zarr
import boto3
import os
import pandas as pd

def wait_for_enter(message="Press Enter to continue..."):
    """Wait for user input to continue"""
    input(f"\n{message}")

def main():
    print("🌊 EDITO Datalab Jupyter Demo")
    print("=" * 40)
    
    # 1. STAC Search - Finding Marine Data
    print("\n## 1. STAC Search - Finding Marine Data")
    print("First, let's search the EDITO STAC catalog to find available marine datasets.")
    wait_for_enter()
    
    # Connect to EDITO STAC API
    stac_endpoint = "https://api.dive.edito.eu/data/"
    
    try:
        response = requests.get(f"{stac_endpoint}collections")
        
        if response.status_code == 200:
            collections = response.json()
            
            print(f"✅ Connected to EDITO STAC API")
            print(f"Found {len(collections['collections'])} data collections")
            
            # Show first few collections
            print("\n📋 Available data collections:")
            for i, collection in enumerate(collections['collections'][:10]):
                print(f"{i+1:2d}. {collection['id']} - {collection.get('title', 'No title')}")
                
            # Store available collection IDs for later use
            available_collections = [col['id'] for col in collections['collections']]
            print(f"\n💡 Available collection IDs: {available_collections[:5]}...")
            
        else:
            print(f"❌ Failed to connect to EDITO API: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error connecting to EDITO API: {e}")
        available_collections = []
    
    wait_for_enter()
    
    # Search for biodiversity data
    print("\n🔍 Searching for biodiversity data...")
    
    try:
        search_url = f"{stac_endpoint}search"
        
        # Look for occurrence data collection specifically (has parquet files)
        if available_collections:
            occurrence_collections = [col for col in available_collections if 'occurrence' in col.lower() and 'emodnet-occurrence_data' in col]
            if occurrence_collections:
                search_collections = occurrence_collections[:1]  # Use occurrence data collection
                print(f"🔍 Searching in occurrence data collection: {search_collections[0]}")
            else:
                # Look for other biodiversity collections
                bio_collections = [col for col in available_collections if any(keyword in col.lower() for keyword in ['eurobis', 'bio', 'species', 'fish', 'habitat'])]
                if bio_collections:
                    search_collections = bio_collections[:1]  # Use first biodiversity collection found
                    print(f"🔍 Searching in biodiversity collection: {search_collections[0]}")
                else:
                    search_collections = available_collections[:1]  # Use first available collection
                    print(f"🔍 Searching in available collection: {search_collections[0]}")
        else:
            # Use the occurrence data collection as fallback
            search_collections = ["emodnet-occurrence_data"]
            print("🔍 Searching in occurrence data collection (fallback)")
        
        search_params = {
            "collections": search_collections,
            "limit": 5
        }
        
        response = requests.post(search_url, json=search_params)
        
        # Check if the response was successful
        if response.status_code == 200:
            search_results = response.json()
            
            # Check if the response contains features
            if 'features' in search_results:
                print(f"✅ Found {len(search_results['features'])} biodiversity items")
                
                # Show first item
                if search_results['features']:
                    first_item = search_results['features'][0]
                    print(f"\n📊 Sample item: {first_item['id']}")
                    print(f"Title: {first_item['properties'].get('title', 'No title')}")
                    
                    print("\n🔗 Available data formats:")
                    for asset_name, asset in first_item['assets'].items():
                        print(f"- {asset_name}: {asset['href']}")
                else:
                    print("ℹ️ No biodiversity items found in the search results")
            else:
                print(f"⚠️ Unexpected response format: {search_results}")
        else:
            print(f"❌ STAC search failed with status {response.status_code}")
            error_response = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"Error details: {error_response}")
            
            # Fallback: try a different collection or search without specific collection
            print("\n🔄 Trying alternative search...")
            fallback_params = {"limit": 5}
            fallback_response = requests.post(search_url, json=fallback_params)
            
            if fallback_response.status_code == 200:
                fallback_results = fallback_response.json()
                if 'features' in fallback_results and fallback_results['features']:
                    print(f"✅ Found {len(fallback_results['features'])} items in general search")
                    first_item = fallback_results['features'][0]
                    print(f"\n📊 Sample item: {first_item['id']}")
                    print(f"Collection: {first_item.get('collection', 'Unknown')}")
                else:
                    print("ℹ️ No items found in general search either")
            else:
                print(f"❌ Fallback search also failed with status {fallback_response.status_code}")
                
    except Exception as e:
        print(f"❌ Error searching STAC: {e}")
    
    wait_for_enter()
    
    # 2. Reading Parquet Data - Biodiversity Analysis
    print("\n## 2. Reading Parquet Data - Biodiversity Analysis")
    print("Now let's read the biodiversity data using Parquet format for efficient access.")
    wait_for_enter()
    
    print("📊 Querying parquet data metadata...")
    
    # EUROBIS biodiversity occurrence data
    parquet_url = "https://s3.waw3-1.cloudferro.com/emodnet/emodnet_biology/12639/eurobis_obisenv_view_2025-03-20.parquet"
    
    print(f"🔗 Parquet URL: {parquet_url}")
    
    try:
        # Use pyarrow to read parquet metadata without downloading the entire file
        print("📥 Reading parquet schema and metadata...")
        
        # Create a filesystem for S3
        import pyarrow.fs as fs
        s3_fs = fs.S3FileSystem(endpoint_override="s3.waw3-1.cloudferro.com")
        
        # Convert URL to S3 path format
        s3_path = "emodnet/emodnet_biology/12639/eurobis_obisenv_view_2025-03-20.parquet"
        
        # Read just the schema and metadata
        parquet_file = pq.ParquetFile(s3_path, filesystem=s3_fs)
        
        print(f"✅ Successfully connected to parquet file")
        print(f"📊 Number of row groups: {parquet_file.num_row_groups}")
        print(f"📏 Total rows: {parquet_file.metadata.num_rows}")
        print(f"📋 Schema:")
        
        # Print schema information
        schema = parquet_file.schema
        for i, field in enumerate(schema):
            print(f"  {i+1:2d}. {field.name}: {field.physical_type}")
        
        # Get row group information
        print(f"\n📊 Row group details:")
        for i in range(parquet_file.num_row_groups):
            rg = parquet_file.metadata.row_group(i)
            if i % 100 == 0:
                print(f"  Row group {i}: {rg.num_rows} rows, {rg.total_byte_size} bytes")
        
        # Read just a small sample to show data structure
        print(f"\n📊 Reading sample data (first 10 rows)...")
        # Read only the first few columns and limit rows
        sample_columns = list(schema.names)[:10]  # First 10 columns only
        sample_table = parquet_file.read_row_groups([0], columns=sample_columns)
        sample_df = sample_table.to_pandas().head(10)  # Only take first 10 rows
        
        print(f"✅ Sample data loaded: {len(sample_df)} rows")
        print(f"📋 Sample columns: {list(sample_df.columns)[:10]}...")
        print(f"\nFirst 3 rows of sample data:")
        print(sample_df.head(3))
        
        # Use the sample data for demonstration
        df = sample_df
        
    except Exception as e:
        print(f"❌ Error reading parquet metadata: {e}")
        print("📊 Creating sample biodiversity data for demonstration...")
        
        # Create sample data for demonstration
        df = pd.DataFrame({
            'scientificName': ['Scomber scombrus', 'Gadus morhua', 'Pleuronectes platessa', 'Merlangius merlangus', 'Solea solea'] * 20,
            'decimalLatitude': np.random.uniform(50, 60, 100),
            'decimalLongitude': np.random.uniform(0, 10, 100),
            'eventDate': pd.date_range('2020-01-01', '2023-12-31', periods=100)
        })
        
        print(f"✅ Created sample dataset with {len(df)} records")
        print(f"📋 Columns: {list(df.columns)}")
        print(f"📊 Data types: {df.dtypes.value_counts().to_dict()}")
        
        # Show first few rows
        print(f"\nFirst 5 rows:")
        print(df.head())
    
    wait_for_enter()
    
    # Filter for marine species
    print("🐠 Analyzing marine species data...")
    
    # Check what columns are available
    print(f"📋 Available columns: {list(df.columns)[:20]}...")
    
    # Look for species-related columns
    species_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in ['species', 'scientific', 'taxon', 'name'])]
    print(f"🔍 Species-related columns: {species_columns}")
    
    if species_columns:
        # Use the first species column found
        species_col = species_columns[0]
        print(f"📊 Using column '{species_col}' for species analysis")
        
        # Show unique values in the species column
        unique_species = df[species_col].value_counts().head(10)
        print(f"\nTop 10 species in '{species_col}':")
        print(unique_species)
        
        marine_data = df  # Use all data for now
    else:
        print("ℹ️ No species columns found, using all data")
        marine_data = df
    
    print(f"✅ Found {len(marine_data)} records")
    
    wait_for_enter()
    
    # Create a simple visualization
    if len(marine_data) > 0:
        print("📊 Creating visualizations...")
        
        plt.figure(figsize=(12, 8))
        
        # Plot 1: Species distribution (if species column exists)
        plt.subplot(2, 2, 1)
        if species_columns:
            species_count = marine_data[species_col].value_counts().head(5)
            species_count.plot(kind='bar')
            plt.title(f'Top 5 Species in {species_col}')
            plt.xticks(rotation=45)
        else:
            plt.text(0.5, 0.5, 'No species data available', ha='center', va='center')
            plt.title('Species Distribution')
        
        # Plot 2: Geographic distribution (if coordinates exist)
        plt.subplot(2, 2, 2)
        coord_cols = [col for col in marine_data.columns if any(keyword in col.lower() for keyword in ['lat', 'lon', 'longitude', 'latitude'])]
        if coord_cols and len(coord_cols) >= 2:
            lat_col = [col for col in coord_cols if 'lat' in col.lower()][0]
            lon_col = [col for col in coord_cols if 'lon' in col.lower()][0]
            plt.scatter(marine_data[lon_col], marine_data[lat_col], alpha=0.6, s=20)
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.title('Geographic Distribution')
        else:
            plt.text(0.5, 0.5, 'No coordinate data available', ha='center', va='center')
            plt.title('Geographic Distribution')
        
        # Plot 3: Temporal distribution (if date columns exist)
        plt.subplot(2, 2, 3)
        date_cols = [col for col in marine_data.columns if any(keyword in col.lower() for keyword in ['date', 'year', 'time'])]
        if date_cols:
            date_col = date_cols[0]
            if 'year' in date_col.lower():
                marine_data[date_col].value_counts().sort_index().plot(kind='line')
            else:
                # Try to extract year from date
                try:
                    marine_data['year'] = pd.to_datetime(marine_data[date_col]).dt.year
                    marine_data['year'].value_counts().sort_index().plot(kind='line')
                except:
                    marine_data[date_col].value_counts().head(10).plot(kind='bar')
            plt.title(f'Records by {date_col}')
            plt.xlabel(date_col)
            plt.ylabel('Count')
        else:
            plt.text(0.5, 0.5, 'No date data available', ha='center', va='center')
            plt.title('Temporal Distribution')
        
        # Plot 4: Summary stats
        plt.subplot(2, 2, 4)
        plt.text(0.1, 0.7, f'Total Records: {len(marine_data)}', fontsize=12)
        if species_columns:
            plt.text(0.1, 0.5, f'Unique Species: {marine_data[species_col].nunique()}', fontsize=12)
        else:
            plt.text(0.1, 0.5, f'Total Columns: {len(marine_data.columns)}', fontsize=12)
        
        if coord_cols and len(coord_cols) >= 2:
            lat_col = [col for col in coord_cols if 'lat' in col.lower()][0]
            lon_col = [col for col in coord_cols if 'lon' in col.lower()][0]
            plt.text(0.1, 0.3, f'Latitude Range: {marine_data[lat_col].min():.1f} - {marine_data[lat_col].max():.1f}', fontsize=12)
            plt.text(0.1, 0.1, f'Longitude Range: {marine_data[lon_col].min():.1f} - {marine_data[lon_col].max():.1f}', fontsize=12)
        else:
            plt.text(0.1, 0.3, f'Data Shape: {marine_data.shape}', fontsize=12)
        
        plt.title('Summary Statistics')
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
    else:
        print("❌ No marine data to visualize")
    
    wait_for_enter()
    
    # 3. Reading Zarr Data - Oceanographic Analysis
    print("\n## 3. Reading Zarr Data - Oceanographic Analysis")
    print("Now let's work with Zarr data for oceanographic analysis using xarray.")
    wait_for_enter()
    
    print("🧊 Reading oceanographic data from Zarr...")
    
    # Example Zarr URL (you would get this from STAC search)
    # For demo purposes, we'll create sample oceanographic data
    print("Creating sample oceanographic data for demonstration...")
    
    # Create sample oceanographic data
    lats = np.linspace(50, 60, 50)
    lons = np.linspace(0, 10, 50)
    times = pd.date_range('2020-01-01', '2020-12-31', freq='D')
    depths = np.array([0, 10, 20, 50, 100, 200, 500, 1000])
    
    # Create temperature data with realistic patterns
    temp_data = np.random.normal(10, 2, (len(times), len(depths), len(lats), len(lons)))
    # Add seasonal variation
    seasonal = 5 * np.sin(2 * np.pi * np.arange(len(times)) / 365.25)
    temp_data += seasonal[:, np.newaxis, np.newaxis, np.newaxis]
    # Add depth variation
    temp_data += -0.01 * depths[np.newaxis, :, np.newaxis, np.newaxis]
    
    # Create xarray Dataset
    ds = xr.Dataset({
        'temperature': (['time', 'depth', 'lat', 'lon'], temp_data),
        'salinity': (['time', 'depth', 'lat', 'lon'], 
                     temp_data + np.random.normal(0, 0.5, temp_data.shape))
    }, coords={
        'time': times,
        'depth': depths,
        'lat': lats,
        'lon': lons
    })
    
    print(f"✅ Created oceanographic dataset")
    print(f"Dimensions: {ds.dims}")
    print(f"Variables: {list(ds.data_vars)}")
    print(f"Coordinates: {list(ds.coords)}")
    
    wait_for_enter()
    
    # Analyze the oceanographic data
    print("📊 Analyzing oceanographic data...")
    
    # Calculate mean temperature by depth
    mean_temp_by_depth = ds.temperature.mean(dim=['time', 'lat', 'lon'])
    
    # Calculate seasonal cycle
    seasonal_temp = ds.temperature.mean(dim=['depth', 'lat', 'lon'])
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot 1: Temperature profile by depth
    axes[0, 0].plot(mean_temp_by_depth, -mean_temp_by_depth.depth)
    axes[0, 0].set_xlabel('Temperature (°C)')
    axes[0, 0].set_ylabel('Depth (m)')
    axes[0, 0].set_title('Mean Temperature Profile')
    axes[0, 0].grid(True)
    
    # Plot 2: Seasonal temperature cycle
    axes[0, 1].plot(seasonal_temp.time, seasonal_temp)
    axes[0, 1].set_xlabel('Date')
    axes[0, 1].set_ylabel('Temperature (°C)')
    axes[0, 1].set_title('Seasonal Temperature Cycle')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Plot 3: Temperature at surface
    surface_temp = ds.temperature.isel(depth=0, time=0)
    im = axes[1, 0].contourf(surface_temp.lon, surface_temp.lat, surface_temp, levels=20)
    axes[1, 0].set_xlabel('Longitude')
    axes[1, 0].set_ylabel('Latitude')
    axes[1, 0].set_title('Surface Temperature (Jan 1, 2020)')
    plt.colorbar(im, ax=axes[1, 0])
    
    # Plot 4: Temperature vs Salinity
    temp_flat = ds.temperature.values.flatten()
    sal_flat = ds.salinity.values.flatten()
    # Sample for plotting
    sample_idx = np.random.choice(len(temp_flat), 1000, replace=False)
    axes[1, 1].scatter(sal_flat[sample_idx], temp_flat[sample_idx], alpha=0.6, s=1)
    axes[1, 1].set_xlabel('Salinity')
    axes[1, 1].set_ylabel('Temperature (°C)')
    axes[1, 1].set_title('Temperature vs Salinity')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("✅ Oceanographic analysis complete!")
    
    wait_for_enter()
    
    # 4. Personal Storage - Connect and Transfer Data
    print("\n## 4. Personal Storage - Connect and Transfer Data")
    print("Now let's connect to your personal storage and transfer data.")
    wait_for_enter()
    
    # Connect to personal storage
    print("💾 Connecting to personal storage...")
    
    # Check if storage credentials are available
    if os.getenv("AWS_ACCESS_KEY_ID"):
        print("✅ Personal storage credentials found!")
        
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
        
    else:
        print("❌ No storage credentials found. Make sure you're running in EDITO Datalab.")
        print("💡 Your credentials are automatically available in EDITO services")
        print("💡 No need to go to project settings - they're already there!")
        
        # For demo purposes, create a mock connection
        print("Creating mock connection for demonstration...")
        s3 = None
    
    wait_for_enter()
    
    # Process and save data to personal storage
    print("📊 Processing data for storage...")
    
    if len(marine_data) > 0:
        # Process the marine data
        processed_data = marine_data.groupby('scientificName').agg({
            'decimalLatitude': 'mean',
            'decimalLongitude': 'mean',
            'eventDate': 'count'
        }).reset_index()
        
        processed_data.columns = ['species', 'mean_latitude', 'mean_longitude', 'count']
        
        print(f"✅ Processed data: {len(processed_data)} species")
        print(processed_data.head())
        
        # Save to local file first
        processed_data.to_csv('processed_marine_data.csv', index=False)
        print("✅ Data saved locally as processed_marine_data.csv")
        
        # Upload to personal storage (if connected)
        if s3:
            try:
                s3.put_object(
                    Bucket='your-bucket-name',  # Replace with your actual bucket name
                    Key='marine_analysis/processed_marine_data.csv',
                    Body=processed_data.to_csv(index=False),
                    ContentType='text/csv'
                )
                print("✅ Data uploaded to personal storage!")
            except Exception as e:
                print(f"❌ Error uploading to storage: {e}")
                print("💡 Make sure to replace 'your-bucket-name' with your actual bucket name")
        else:
            print("💡 To upload to storage, make sure you're running in EDITO Datalab")
            
    else:
        print("❌ No marine data to process")
    
    wait_for_enter()
    
    # 5. Summary - EDITO Datalab Workflow
    print("\n## 5. Summary - EDITO Datalab Workflow")
    print("This script demonstrated the core EDITO Datalab workflow:")
    print()
    print("### 🎯 Key Steps:")
    print("1. **Find Services**: Go to [datalab.dive.edito.eu](https://datalab.dive.edito.eu/) and select a service")
    print("2. **Configure Service**: Choose RStudio, Jupyter, or VSCode with appropriate resources")
    print("3. **Run Analysis**: Use STAC to find data, Parquet for tabular data, Zarr for arrays")
    print("4. **Connect Storage**: Access your personal storage with automatic credentials")
    print("5. **Process & Transfer**: Analyze data and save results to your storage")
    print()
    print("### 🛠️ Services Available:")
    print("- **RStudio**: Perfect for statistical analysis and visualization")
    print("- **Jupyter**: Ideal for machine learning and data exploration")
    print("- **VSCode**: Great for larger projects with R and Python")
    print()
    print("### 📊 Data Formats:")
    print("- **STAC**: Find and discover marine datasets")
    print("- **Parquet**: Efficient tabular data (biodiversity, observations)")
    print("- **Zarr**: Cloud-optimized arrays (oceanographic, climate data)")
    print()
    print("### 🚀 Next Steps:")
    print("- Try the RStudio service for R-based analysis")
    print("- Explore more datasets in the EDITO STAC catalog")
    print("- Use personal storage to save your results")
    print()
    print("**Happy analyzing! 🌊🐠**")

if __name__ == "__main__":
    main()
