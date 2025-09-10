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
import logging

def get_stac_collections(stac_endpoint="https://api.dive.edito.eu/data/"):
    """
    Get available collections from EDITO STAC API
    
    Args:
        stac_endpoint (str): URL of the STAC API endpoint
        
    Returns:
        dict: Collections data from STAC API
    """
    logger = logging.getLogger(__name__)
    
    logger.info("🌊 EDITO Datalab: Getting STAC Collections")
    logger.info("=" * 50)
    logger.info(f"Getting STAC Collections from {stac_endpoint}")
    
    try:
        logger.info(f"🔗 Connecting to STAC API: {stac_endpoint}")
        response = requests.get(f"{stac_endpoint}collections")
        
        if response.status_code == 200:
            collections = response.json()
            
            logger.info(f"✅ Connected to EDITO STAC API")
            logger.info(f"📊 Found {len(collections['collections'])} data collections")
            
            # Show first few collections
            print("\n📋 Available data collections:")
            logger.info("📋 Available data collections:")
            for i, collection in enumerate(collections['collections'][:10]):
                print(f"{i+1:2d}. {collection['id']} - {collection.get('title', 'No title')}")
                logger.info(f"Collection {i+1}: {collection['id']} - {collection.get('title', 'No title')}")
            
            if len(collections['collections']) > 10:
                print(f"    ... and {len(collections['collections']) - 10} more collections")
                logger.info(f"Additional collections available: {len(collections['collections']) - 10}")
            
            # Store available collection IDs for later use
            available_collections = [col['id'] for col in collections['collections']]
            print(f"\n💡 Available collection IDs: {available_collections[:5]}...")
            logger.info(f"Available collection IDs: {available_collections[:5]}")
            
            return collections
            
        else:
            print(f"❌ Failed to connect to EDITO API: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            logger.error(f"❌ Failed to connect to EDITO API: HTTP {response.status_code}")
            logger.error(f"Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Error connecting to EDITO API: {e}")
        logger.error(f"❌ Error connecting to EDITO API: {e}")
        return None

def save_collections(collections, output_file="stac_collections.json"):
    """
    Save collections data to JSON file
    
    Args:
        collections (dict): Collections data from STAC API
        output_file (str): Output file path
    """
    logger = logging.getLogger(__name__)
    
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
            logger.info(f"✅ Collections saved to {output_file} ({len(collections['collections'])} collections)")
            
        except Exception as e:
            print(f"❌ Error saving collections: {e}")
            logger.error(f"❌ Error saving collections: {e} (file: {output_file})")
    else:
        print("❌ No collections data to save")
        logger.error("❌ No collections data to save")

def main():
    """Interactive main function"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Setup simple logging
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
    
    logger.info("🌊 EDITO Datalab: Interactive STAC Collections Discovery")
    logger.info("=" * 60)
    logger.info("Starting STAC Collections Discovery")
    
    # Get collections
    collections = get_stac_collections()
    
    if collections:
        # Save to file
        save_collections(collections)
        
        # Show interactive options
        print("\n🎯 What would you like to do next?")
        print("1. Search for specific data types (parquet/raster)")
        print("2. Explore collection details")
        print("3. Exit")
        logger.info("🎯 Interactive options presented to user")
        
        while True:
            choice = input("Enter choice (1-3): ").strip()
            if choice == '1':
                print("💡 Run: python 02_search_stac_assets.py")
                logger.info("User selected option 1: Search for data types")
                break
            elif choice == '2':
                # Show detailed info for first few collections
                print("\n📋 Collection Details:")
                logger.info("User selected option 2: Explore collection details")
                for i, collection in enumerate(collections['collections'][:5]):
                    print(f"\n{i+1}. {collection['id']}")
                    print(f"   Title: {collection.get('title', 'No title')}")
                    print(f"   Description: {collection.get('description', 'No description')[:100]}...")
                    print(f"   Keywords: {collection.get('keywords', [])}")
                    logger.info(f"Collection {i+1} details: {collection['id']} - {collection.get('title', 'No title')}")
                break
            elif choice == '3':
                print("👋 Goodbye!")
                logger.info("User selected option 3: Exit")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                logger.warning("User entered invalid choice")
    else:
        print("❌ Could not fetch collections. Please check your connection.")
        logger.error("❌ Could not fetch collections from STAC API")
    
    log_path = 'logs/edito_workflow.log'
    print(f"\n📝 Log file: {log_path}")
    print("💡 You can tail the log with: tail -f", log_path)
    logger.info(f"📝 Log file: {log_path}")
    logger.info("💡 You can tail the log with: tail -f logs/edito_workflow.log")

if __name__ == "__main__":
    main()
