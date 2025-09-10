#!/usr/bin/env python3
"""
EDITO Datalab Demo: Get STAC Collections

Simple script to get STAC collections and save to JSON.
Allows searching for specific collections by term.
"""

import requests
import json
from datetime import datetime

def get_stac_collections(stac_endpoint="https://api.dive.edito.eu/data/"):
    """Get available collections from EDITO STAC API"""
    print(f"🔗 Getting collections from {stac_endpoint}")
    

    try:
        response = requests.get(f"{stac_endpoint}collections")
        
        if response.status_code == 200:
            collections = response.json()
            print(f"✅ Found {len(collections['collections'])} collections")
            
            # Show collections
            print("\n📋 Available collections:")
            for i, collection in enumerate(collections['collections'][:10]):
                print(f"{i+1:2d}. {collection['id']} - {collection.get('title', 'No title')}")
            
            if len(collections['collections']) > 10:
                print(f"    ... and {len(collections['collections']) - 10} more")
            
            return collections
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def save_collections(collections, output_file="stac_collections.json"):
    """Save collections data to JSON file"""
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
            print(f"❌ Error saving: {e}")
    else:
        print("❌ No collections to save")

def search_collections(collections, search_term):
    """Search for collections containing a specific term"""
    if not collections:
        return []
    
    matching = []
    for collection in collections['collections']:
        collection_id = collection['id'].lower()
        title = collection.get('title', '').lower()
        description = collection.get('description', '').lower()
        
        if (search_term.lower() in collection_id or 
            search_term.lower() in title or 
            search_term.lower() in description):
            matching.append(collection)
    
    return matching

def main():
    """Simple demo to get collections and search for specific terms"""
    print("🌊 EDITO Datalab: Get STAC Collections")
    print("=" * 40)
    
    # Get collections
    collections = get_stac_collections()
    
    if collections:
        # Save to file
        save_collections(collections)
        
        # Allow custom search
        print(f"\n🔍 Search for specific collections? (Enter search term or press Enter to skip)")
        search_term = input("Search term: ").strip()
        
        if search_term:
            matching = search_collections(collections, search_term)
            if matching:
                print(f"✅ Found {len(matching)} collections containing '{search_term}':")
                for i, collection in enumerate(matching):
                    print(f"  {i+1}. {collection['id']} - {collection.get('title', 'No title')}")
            else:
                print(f"ℹ️ No collections found containing '{search_term}'")
        
        print(f"\n💡 Next: Run 'python 02_search_stac_assets.py' to search for data")
    else:
        print("❌ Could not fetch collections. Check your connection.")

if __name__ == "__main__":
    main()