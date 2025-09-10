#!/usr/bin/env python3
"""
EDITO Datalab Demo: Search STAC for Parquet and NetCDF/Zarr Assets

This script searches the EDITO STAC catalog for biodiversity collections
and finds items with parquet and raster (NetCDF/Zarr) assets.
It saves the search results to JSON files for use by other scripts.
"""

import requests
import json
import os
from datetime import datetime
import logging

def load_collections(collections_file="stac_collections.json"):
    """
    Load collections data from JSON file
    
    Args:
        collections_file (str): Path to collections JSON file
        
    Returns:
        list: List of collection IDs
    """
    try:
        with open(collections_file, 'r') as f:
            collections_data = json.load(f)
        
        available_collections = [col['id'] for col in collections_data['collections']]
        print(f"✅ Loaded {len(available_collections)} collections from {collections_file}")
        logger = logging.getLogger(__name__)
        logger.info(f"✅ Loaded {len(available_collections)} collections from {collections_file}")
        return available_collections
        
    except Exception as e:
        print(f"❌ Error loading collections: {e}")
        logger = logging.getLogger(__name__)
        logger.error(f"❌ Error loading collections: {e}")
        return []

def search_stac_assets(stac_endpoint="https://api.dive.edito.eu/data/", 
                      collections=None, 
                      limit=20):
    """
    Search STAC for items with parquet and raster assets
    
    Args:
        stac_endpoint (str): URL of the STAC API endpoint
        collections (list): List of collection IDs to search
        limit (int): Maximum number of items to return
        
    Returns:
        tuple: (parquet_items, raster_items)
    """
    logger = logging.getLogger(__name__)
    
    print("🔍 EDITO Datalab: Searching STAC for Assets")
    print("=" * 50)
    logger.info("🔍 EDITO Datalab: Searching STAC for Assets")
    logger.info("=" * 50)
    
    if not collections:
        print("❌ No collections provided")
        logger.error("No collections provided")
        return [], []
    
    # Look for biodiversity collections that might have different data types
    bio_collections = [col for col in collections if any(keyword in col.lower() 
                     for keyword in ['eurobis', 'bio', 'species', 'fish', 'habitat', 
                                   'bathymetry', 'seabed', 'marine', 'occurrence'])]
    
    if bio_collections:
        search_collections = bio_collections[:5]  # Search in top 5 biodiversity collections
        print(f"🔍 Searching in biodiversity collections: {search_collections}")
        logger.info(f"Searching in biodiversity collections: {search_collections}")
    else:
        search_collections = collections[:5]  # Use first 5 available collections
        print(f"🔍 Searching in available collections: {search_collections}")
        logger.info(f"Searching in available collections: {search_collections}")
    
    try:
        search_url = f"{stac_endpoint}search"
        search_params = {
            "collections": search_collections,
            "limit": limit
        }
        
        print(f"📡 Searching STAC API...")
        logger.info(f"Searching STAC API: {search_url}")
        logger.info(f"Search parameters: {search_params}")
        response = requests.post(search_url, json=search_params)
        
        if response.status_code == 200:
            search_results = response.json()
            logger.info(f"STAC API response received: {response.status_code}")
            
            if 'features' in search_results and search_results['features']:
                print(f"✅ Found {len(search_results['features'])} items")
                logger.info(f"Found {len(search_results['features'])} items in search results")
                
                # Categorize items by asset types
                parquet_items = []
                raster_items = []
                
                for item in search_results['features']:
                    item_parquet = []
                    item_raster = []
                    
                    for asset_name, asset in item['assets'].items():
                        asset_url = asset['href'].lower()
                        
                        # Check for parquet files
                        if any(ext in asset_url for ext in ['.parquet', '.pq']):
                            item_parquet.append((asset_name, asset))
                        
                        # Check for raster files (NetCDF, Zarr)
                        elif any(ext in asset_url for ext in ['.nc', '.zarr', '.netcdf']):
                            item_raster.append((asset_name, asset))
                    
                    # Add item to appropriate category if it has the right assets
                    if item_parquet:
                        parquet_items.append({
                            'item': item,
                            'assets': item_parquet
                        })
                    
                    if item_raster:
                        raster_items.append({
                            'item': item,
                            'assets': item_raster
                        })
                
                print(f"📊 Found {len(parquet_items)} items with parquet assets")
                print(f"🗺️ Found {len(raster_items)} items with raster assets")
                logger.info(f"📊 Found {len(parquet_items)} items with parquet assets")
                logger.info(f"🗺️ Found {len(raster_items)} items with raster assets")
                
                return parquet_items, raster_items
                
            else:
                print("ℹ️ No items found in search results")
                logger.info("ℹ️ No items found in search results")
                return [], []
                
        else:
            print(f"❌ STAC search failed with status {response.status_code}")
            error_response = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"Error details: {error_response}")
            logger.error(f"❌ STAC search failed with status {response.status_code}")
            logger.error(f"Error details: {error_response}")
            return [], []
            
    except Exception as e:
        print(f"❌ Error searching STAC: {e}")
        logger.error(f"❌ Error searching STAC: {e}")
        return [], []

def save_search_results(parquet_items, raster_items, 
                       parquet_file="stac_parquet_items.json",
                       raster_file="stac_raster_items.json"):
    """
    Save search results to JSON files
    
    Args:
        parquet_items (list): List of items with parquet assets
        raster_items (list): List of items with raster assets
        parquet_file (str): Output file for parquet items
        raster_file (str): Output file for raster items
    """
    # Save parquet items
    logger = logging.getLogger(__name__)
    if parquet_items:
        try:
            parquet_data = {
                'metadata': {
                    'retrieved_at': datetime.now().isoformat(),
                    'total_items': len(parquet_items),
                    'asset_type': 'parquet'
                },
                'items': parquet_items
            }
            
            with open(parquet_file, 'w') as f:
                json.dump(parquet_data, f, indent=2)
            
            print(f"✅ Parquet items saved to {parquet_file}")
            logger.info(f"✅ Parquet items saved to {parquet_file}")
            
            # Show sample parquet items
            print(f"\n📊 Sample parquet items:")
            logger.info("📊 Sample parquet items:")
            for i, item_data in enumerate(parquet_items[:3]):
                item = item_data['item']
                print(f"  {i+1}. {item['id']} - {item['properties'].get('title', 'No title')}")
                logger.info(f"  Parquet item {i+1}: {item['id']} - {item['properties'].get('title', 'No title')}")
                for asset_name, asset in item_data['assets']:
                    print(f"     - {asset_name}: {asset['href']}")
                    logger.info(f"     - {asset_name}: {asset['href']}")
            
        except Exception as e:
            print(f"❌ Error saving parquet items: {e}")
            logger.error(f"❌ Error saving parquet items: {e}")
    else:
        print("ℹ️ No parquet items to save")
        logger.info("ℹ️ No parquet items to save")
    
    # Save raster items
    if raster_items:
        try:
            raster_data = {
                'metadata': {
                    'retrieved_at': datetime.now().isoformat(),
                    'total_items': len(raster_items),
                    'asset_type': 'raster'
                },
                'items': raster_items
            }
            
            with open(raster_file, 'w') as f:
                json.dump(raster_data, f, indent=2)
            
            print(f"✅ Raster items saved to {raster_file}")
            logger.info(f"✅ Raster items saved to {raster_file}")
            
            # Show sample raster items
            print(f"\n🗺️ Sample raster items:")
            logger.info("🗺️ Sample raster items:")
            for i, item_data in enumerate(raster_items[:3]):
                item = item_data['item']
                print(f"  {i+1}. {item['id']} - {item['properties'].get('title', 'No title')}")
                logger.info(f"  Raster item {i+1}: {item['id']} - {item['properties'].get('title', 'No title')}")
                for asset_name, asset in item_data['assets']:
                    print(f"     - {asset_name}: {asset['href']}")
                    logger.info(f"     - {asset_name}: {asset['href']}")
            
        except Exception as e:
            print(f"❌ Error saving raster items: {e}")
            logger.error(f"❌ Error saving raster items: {e}")
    else:
        print("ℹ️ No raster items to save")
        logger.info("ℹ️ No raster items to save")

def main():
    """Main function"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/edito_workflow.log', mode='a'),
            logging.StreamHandler()
        ],
        force=True  # Force reconfiguration
    )
    logger = logging.getLogger(__name__)
    
    logger.info("🔍 EDITO Datalab: STAC Asset Search")
    logger.info("=" * 50)
    
    # Load collections
    collections = load_collections()
    
    if not collections:
        print("❌ No collections available. Run 01_get_stac_collections.py first.")
        logger.error("❌ No collections available. Run 01_get_stac_collections.py first.")
        return
    
    # Search for assets
    parquet_items, raster_items = search_stac_assets(collections=collections)
    
    # Save results
    save_search_results(parquet_items, raster_items)
    
    logger.info(f"Search completed: {len(parquet_items)} parquet items, {len(raster_items)} raster items")
    
    print("\n🎯 Next steps:")
    print("1. Run 03_get_zarr_to_df.py to process raster data")
    print("2. Run 04_get_parquet_data.py to process parquet data")
    print("3. Run 05_combine_and_save.py to combine and save to storage")
    logger.info("🎯 Next steps presented to user")

if __name__ == "__main__":
    main()
