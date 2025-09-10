#!/usr/bin/env python3
"""
EDITO Datalab Demo: Search STAC Assets

Simple script to search STAC for collections and find data assets.
By default searches all collections, but can be filtered by search term.
"""

import requests
import json
from datetime import datetime

def load_collections(collections_file="stac_collections.json"):
    """Load collections data from JSON file"""
    try:
        with open(collections_file, 'r') as f:
            collections_data = json.load(f)
        
        available_collections = [col['id'] for col in collections_data['collections']]
        print(f"✅ Loaded {len(available_collections)} collections from {collections_file}")
        return available_collections
        
    except Exception as e:
        print(f"❌ Error loading collections: {e}")
        return []

def search_stac_assets(stac_endpoint="https://api.dive.edito.eu/data/", 
                      collections=None, 
                      search_term="",
                      limit=50):
    """Search STAC for items in specific collections"""
    if search_term:
        print(f"🔍 Searching for '{search_term}' collections...")
    else:
        print("🔍 Searching all collections...")
    
    if not collections:
        print("❌ No collections provided")
        return []
    
    # Filter collections that contain the search term (if provided)
    if search_term:
        matching_collections = [col for col in collections if search_term.lower() in col.lower()]
    else:
        # If no search term, use all provided collections
        matching_collections = collections
    
    if not matching_collections:
        if search_term:
            print(f"ℹ️ No collections found containing '{search_term}'")
        else:
            print("ℹ️ No collections available")
        print(f"Available collections: {collections[:5]}...")
        return []
    
    # Show what types of collections we're searching
    biodiversity_count = len([col for col in matching_collections if any(keyword in col.lower() for keyword in ['occurrence', 'biodiversity', 'eurobis'])])
    ocean_count = len([col for col in matching_collections if any(keyword in col.lower() for keyword in ['arco', 'cmems', 'wave', 'current', 'temperature'])])
    print(f"🔍 Searching {len(matching_collections)} collections ({biodiversity_count} biodiversity/parquet, {ocean_count} ocean/zarr data)")
    
    print(f"📋 Found {len(matching_collections)} collections: {matching_collections}")
    
    try:
        search_url = f"{stac_endpoint}search"
        search_params = {
            "collections": matching_collections,
            "limit": limit
        }
        
        print(f"📡 Searching STAC API...")
        response = requests.post(search_url, json=search_params)
        
        if response.status_code == 200:
            search_results = response.json()
            
            if 'features' in search_results and search_results['features']:
                print(f"✅ Found {len(search_results['features'])} items")
                
                # Show sample items
                print(f"\n📊 Sample items:")
                for i, item in enumerate(search_results['features'][:5]):
                    print(f"  {i+1}. {item['id']} - {item['properties'].get('title', 'No title')}")
                    print(f"     Collection: {item['collection']}")
                    
                    # Show available assets
                    asset_types = []
                    for asset_name, asset in item['assets'].items():
                        href = asset['href'].lower()
                        if '.parquet' in href:
                            asset_types.append('parquet')
                        elif '.zarr' in href:
                            asset_types.append('zarr')
                        elif '.nc' in href:
                            asset_types.append('netcdf')
                        elif any(ext in href for ext in ['.tif', '.tiff', '.geotiff']):
                            asset_types.append('geotiff')
                    
                    if asset_types:
                        print(f"     Assets: {', '.join(set(asset_types))}")
                
                return search_results['features']
            else:
                print("ℹ️ No items found in search results")
                return []
        else:
            print(f"❌ Search failed: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error searching STAC: {e}")
        return []

def extract_parquet_items(items):
    """Extract items that contain parquet assets"""
    parquet_items = []
    
    for item in items:
        parquet_assets = []
        for asset_name, asset in item.get('assets', {}).items():
            if '.parquet' in asset['href'].lower():
                parquet_assets.append((asset_name, asset))
        
        if parquet_assets:
            parquet_items.append({
                'item': item,
                'assets': parquet_assets
            })
    
    return parquet_items

def save_search_results(items, search_term="", output_file="stac_search_results.json"):
    """Save search results to JSON file"""
    if items:
        try:
            search_data = {
                'metadata': {
                    'retrieved_at': datetime.now().isoformat(),
                    'total_items': len(items),
                    'search_term': search_term
                },
                'items': items
            }
            
            with open(output_file, 'w') as f:
                json.dump(search_data, f, indent=2)
            
            print(f"✅ Search results saved to {output_file}")
            
            # Also extract and save parquet items for the parquet processing script
            parquet_items = extract_parquet_items(items)
            if parquet_items:
                parquet_data = {
                    'metadata': {
                        'retrieved_at': datetime.now().isoformat(),
                        'total_parquet_items': len(parquet_items),
                        'search_term': search_term
                    },
                    'items': parquet_items
                }
                
                with open("stac_parquet_items.json", 'w') as f:
                    json.dump(parquet_data, f, indent=2)
                
                print(f"✅ Parquet items saved to stac_parquet_items.json ({len(parquet_items)} items)")
            else:
                print("ℹ️ No parquet assets found in search results")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    else:
        print("ℹ️ No results to save")

def get_user_collections():
    """Get collections from user input or previous step"""
    print("\n🔍 Collection Selection Options:")
    print("1. Use collections from previous step (01_get_stac_collections.py)")
    print("2. Enter specific collections manually")
    print("3. Search all collections with a filter term")
    
    choice = input("\nChoose option (1-3, default=1): ").strip() or "1"
    
    if choice == "1":
        # Load collections from previous step
        collections = load_collections()
        if not collections:
            print("❌ No collections available. Run 01_get_stac_collections.py first.")
            return None, ""
        
        # Show available collections
        print(f"\n📋 Found {len(collections)} collections from previous step")
        print("First 10 collections:")
        for i, col in enumerate(collections[:10]):
            print(f"  {i+1:2d}. {col}")
        if len(collections) > 10:
            print(f"  ... and {len(collections) - 10} more")
        
        # Ask for search term
        search_term = input("\nEnter search term to filter collections (default: none - use all): ").strip()
        return collections, search_term
    
    elif choice == "2":
        # Manual collection input
        print("\n📝 Enter collections manually (one per line, empty line to finish):")
        collections = []
        while True:
            col = input("Collection ID: ").strip()
            if not col:
                break
            collections.append(col)
        
        if not collections:
            print("❌ No collections entered")
            return None, ""
        
        print(f"\n📋 Using {len(collections)} manually entered collections:")
        for i, col in enumerate(collections):
            print(f"  {i+1:2d}. {col}")
        
        search_term = ""  # No filtering for manual collections
        return collections, search_term
    
    elif choice == "3":
        # Search all collections with filter
        collections = load_collections()
        if not collections:
            print("❌ No collections available. Run 01_get_stac_collections.py first.")
            return None, ""
        
        search_term = input("\nEnter search term to filter collections: ").strip()
        if not search_term:
            print("❌ Search term required for this option")
            return None, ""
        
        return collections, search_term
    
    else:
        print("❌ Invalid choice")
        return None, ""

def main():
    """Simple demo to search for collections and assets"""
    print("🌊 EDITO Datalab: Search STAC Assets")
    print("=" * 40)
    
    # Get collections and search term from user
    collections, search_term = get_user_collections()
    
    if not collections:
        return
    
    # Search for assets
    items = search_stac_assets(collections=collections, search_term=search_term)
    
    # Save results
    save_search_results(items, search_term)
    
    if items:
        print(f"\n💡 Next: Run 'python 03_get_zarr_to_df.py' to process the data")
    else:
        print(f"\n💡 Try different collections or search terms")

if __name__ == "__main__":
    main()