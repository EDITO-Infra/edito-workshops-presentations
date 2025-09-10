#!/usr/bin/env python3
"""
EDITO Datalab: Storage Utilities

This script provides utilities for interacting with EDITO personal storage:
- Browse storage structure without downloading files
- List buckets and folders
- Select files from storage
- Display storage structure in tree format
"""

import boto3
import os
import json
from datetime import datetime
from collections import defaultdict

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

def browse_storage_structure(s3_client, bucket_name, prefix="", max_depth=3, current_depth=0):
    """
    Browse and display the structure of S3 storage without downloading files
    
    Args:
        s3_client: S3 client
        bucket_name (str): Bucket name
        prefix (str): Current prefix/folder path
        max_depth (int): Maximum depth to explore
        current_depth (int): Current depth level
        
    Returns:
        dict: Structure tree of the storage
    """
    if current_depth >= max_depth:
        return {"type": "max_depth_reached", "path": prefix}
    
    structure = {"type": "folder", "path": prefix, "contents": {}}
    
    try:
        # List objects with the current prefix
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
            Delimiter='/'
        )
        
        # Process folders (CommonPrefixes)
        if 'CommonPrefixes' in response:
            for folder in response['CommonPrefixes']:
                folder_name = folder['Prefix'].rstrip('/')
                folder_short = folder_name.split('/')[-1] if '/' in folder_name else folder_name
                
                if current_depth < max_depth - 1:
                    structure["contents"][folder_short] = browse_storage_structure(
                        s3_client, bucket_name, folder['Prefix'], max_depth, current_depth + 1
                    )
                else:
                    structure["contents"][folder_short] = {"type": "folder", "path": folder['Prefix'], "contents": "..."}
        
        # Process files (Contents)
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'] != prefix:  # Skip the folder itself
                    file_name = obj['Key'].split('/')[-1]
                    file_size = obj['Size']
                    last_modified = obj['LastModified']
                    
                    structure["contents"][file_name] = {
                        "type": "file",
                        "path": obj['Key'],
                        "size": file_size,
                        "last_modified": last_modified.isoformat(),
                        "size_mb": round(file_size / (1024 * 1024), 2)
                    }
        
        return structure
        
    except Exception as e:
        print(f"❌ Error browsing storage structure: {e}")
        return {"type": "error", "path": prefix, "error": str(e)}

def display_storage_structure(structure, indent=0):
    """
    Display the storage structure in a tree format
    
    Args:
        structure (dict): Structure tree
        indent (int): Current indentation level
    """
    if structure["type"] == "folder":
        print("  " * indent + f"📁 {structure['path'].split('/')[-1] if structure['path'] else 'root'}/")
        
        if "contents" in structure:
            for name, content in structure["contents"].items():
                if content["type"] == "folder":
                    display_storage_structure(content, indent + 1)
                elif content["type"] == "file":
                    size_str = f"({content['size_mb']} MB)" if content['size_mb'] > 0 else "(<1 MB)"
                    print("  " * (indent + 1) + f"📄 {name} {size_str}")
                elif content["type"] == "max_depth_reached":
                    print("  " * (indent + 1) + "... (max depth reached)")
                elif content["type"] == "error":
                    print("  " * (indent + 1) + f"❌ Error: {content['error']}")
    
    elif structure["type"] == "file":
        size_str = f"({structure['size_mb']} MB)" if structure['size_mb'] > 0 else "(<1 MB)"
        print("  " * indent + f"📄 {structure['path'].split('/')[-1]} {size_str}")

def browse_my_files(s3_client):
    """
    Interactive browsing of MyFiles storage structure
    
    Args:
        s3_client: S3 client
        
    Returns:
        str: Selected file path or None
    """
    print("\n📁 Browsing MyFiles Storage Structure")
    print("=" * 50)
    
    # Select bucket
    bucket_name = list_buckets(s3_client)
    if not bucket_name:
        print("❌ No bucket selected.")
        return None
    
    # Ask for depth
    while True:
        try:
            depth_input = input("\n🎯 How many folder levels to explore? (1-5, default=3): ").strip()
            if not depth_input:
                max_depth = 3
            else:
                max_depth = int(depth_input)
            
            if 1 <= max_depth <= 5:
                break
            else:
                print("❌ Please enter a number between 1 and 5")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Browse structure
    print(f"\n🔍 Exploring structure of '{bucket_name}' (max depth: {max_depth})...")
    structure = browse_storage_structure(s3_client, bucket_name, max_depth=max_depth)
    
    print(f"\n📂 Storage Structure:")
    display_storage_structure(structure)
    
    # Ask if user wants to select a file
    print(f"\n🎯 Options:")
    print("1. Select a file from the structure above")
    print("2. Enter a file path manually")
    print("3. Skip file selection")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == '1':
            file_path = input("Enter the full file path (e.g., folder/subfolder/file.nc): ").strip()
            if file_path:
                # Verify file exists
                try:
                    response = s3_client.head_object(Bucket=bucket_name, Key=file_path)
                    print(f"✅ File found: {file_path}")
                    return f"s3://{bucket_name}/{file_path}"
                except Exception as e:
                    print(f"❌ File not found: {file_path}")
                    print(f"Error: {e}")
            break
        elif choice == '2':
            file_path = input("Enter the full S3 path (e.g., s3://bucket/folder/file.nc): ").strip()
            if file_path.startswith('s3://'):
                print(f"✅ Using file: {file_path}")
                return file_path
            else:
                print("❌ Please enter a valid S3 path starting with 's3://'")
            break
        elif choice == '3':
            print("⏭️ Skipping file selection")
            return None
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3")
    
    return None

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

def main():
    """Standalone storage browser"""
    print("🌊 EDITO Datalab: Storage Browser")
    print("=" * 40)
    
    # Connect to storage
    s3_client = connect_to_storage()
    if not s3_client:
        print("❌ Could not connect to storage. Exiting.")
        return
    
    # Browse files
    selected_file = browse_my_files(s3_client)
    if selected_file:
        print(f"\n🎯 Selected file: {selected_file}")
        print("💡 You can copy this path to use in other scripts!")
    else:
        print("👋 No file selected. Goodbye!")

if __name__ == "__main__":
    main()
