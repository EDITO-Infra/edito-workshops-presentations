#!/usr/bin/env python3
"""
EDITO Datalab Demo: Get STAC Collections

This script connects to the EDITO STAC API and retrieves available collections.
It saves the collections information to a JSON file for use by other scripts.
"""

import requests
import json
import os
from datetime import datetime

def get_stac_collections(stac_endpoint="https://api.dive.edito.eu/data/"):
    """
    Get available collections from EDITO STAC API
    
    Args:
        stac_endpoint (str): URL of the STAC API endpoint
        
    Returns:
        dict: Collections data from STAC API
    """
    print("🌊 EDITO Datalab: Getting STAC Collections")
    print("=" * 50)
    
    try:
        print(f"🔗 Connecting to STAC API: {stac_endpoint}")
        response = requests.get(f"{stac_endpoint}collections")
        
        if response.status_code == 200:
            collections = response.json()
            
            print(f"✅ Connected to EDITO STAC API")
            print(f"📊 Found {len(collections['collections'])} data collections")
            
            # Show first few collections
            print("\n📋 Available data collections:")
            for i, collection in enumerate(collections['collections'][:10]):
                print(f"{i+1:2d}. {collection['id']} - {collection.get('title', 'No title')}")
            
            if len(collections['collections']) > 10:
                print(f"    ... and {len(collections['collections']) - 10} more collections")
            
            # Store available collection IDs for later use
            available_collections = [col['id'] for col in collections['collections']]
            print(f"\n💡 Available collection IDs: {available_collections[:5]}...")
            
            return collections
            
        else:
            print(f"❌ Failed to connect to EDITO API: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error connecting to EDITO API: {e}")
        return None

def save_collections(collections, output_file="stac_collections.json"):
    """
    Save collections data to JSON file
    
    Args:
        collections (dict): Collections data from STAC API
        output_file (str): Output file path
    """
    if collections:
        try:
            # Add metadata
            collections['metadata'] = {
                'retrieved_at': datetime.now().isoformat(),
                'total_collections': len(collections['collections']),
                'api_endpoint': 'https://api.dive.edito.eu/data/'
            }
            
            with open(output_file, 'w') as f:
                json.dump(collections, f, indent=2)
            
            print(f"✅ Collections saved to {output_file}")
            
        except Exception as e:
            print(f"❌ Error saving collections: {e}")
    else:
        print("❌ No collections data to save")

def main():
    """Main function"""
    # Get collections
    collections = get_stac_collections()
    
    # Save to file
    save_collections(collections)
    
    print("\n🎯 Next steps:")
    print("1. Run 02_search_stac_assets.py to find parquet and raster data")
    print("2. Use the collections information to search for specific data types")

if __name__ == "__main__":
    main()
