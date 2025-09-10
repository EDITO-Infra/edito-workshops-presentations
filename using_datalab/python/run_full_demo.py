#!/usr/bin/env python3
"""
EDITO Datalab Demo: Simple Workflow Runner

Simple script to run the EDITO Datalab demo workflow.
Runs the simplified scripts in sequence.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*50}")
    print(f"🚀 Running: {script_name}")
    print(f"📝 {description}")
    print(f"{'='*50}")
    
    try:
        # Run script with automatic input for interactive parts
        if script_name == '01_get_stac_collections.py':
            # This script will automatically search for collections and ask for custom search
            input_data = "\n"  # Just press Enter to skip custom search
        elif script_name == '02_search_stac_assets.py':
            # This script now has interactive collection selection
            input_data = "1\n\n"  # Option 1 (use previous collections), then empty search term
        else:
            input_data = ""
        
        result = subprocess.run([sys.executable, script_name], 
                              input=input_data,
                              text=True, 
                              check=True,
                              timeout=120)  # 2 minute timeout
        
        print("✅ Script completed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print(f"⏰ Script timed out: {script_name}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Script failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    required_packages = ['requests', 'pandas', 'numpy', 'pyarrow', 'xarray', 'fsspec', 's3fs']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All dependencies available")
    return True

def main():
    """Main function to run the simplified workflow"""
    print("🌊 EDITO Datalab: Simple Demo Workflow")
    print("=" * 50)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot proceed without required dependencies")
        return
    
    # Define the workflow steps
    workflow_steps = [
        {
            'script': '01_get_stac_collections.py',
            'description': 'Get STAC collections and search for data'
        },
        {
            'script': '02_search_stac_assets.py',
            'description': 'Search for assets in all collections'
        },
        {
            'script': '03_get_zarr_to_df.py',
            'description': 'Process ARCO raster data (NetCDF/Zarr) to DataFrame'
        },
        {
            'script': '04_get_parquet_data.py',
            'description': 'Process parquet data from STAC search'
        },
        {
            'script': '05_combine_and_save.py',
            'description': 'Combine datasets and save to EDITO storage'
        }
    ]
    
    # Track success/failure
    successful_steps = 0
    failed_steps = []
    
    # Run each step
    for i, step in enumerate(workflow_steps, 1):
        print(f"\n📋 Step {i}/{len(workflow_steps)}")
        
        success = run_script(step['script'], step['description'])
        
        if success:
            successful_steps += 1
        else:
            failed_steps.append(step['script'])
            
            # Ask if user wants to continue
            response = input(f"\n❓ Script {step['script']} failed. Continue? (y/n): ")
            if response.lower() != 'y':
                print("🛑 Workflow stopped")
                break
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 WORKFLOW SUMMARY")
    print(f"{'='*50}")
    print(f"✅ Successful steps: {successful_steps}/{len(workflow_steps)}")
    
    if failed_steps:
        print(f"❌ Failed steps: {', '.join(failed_steps)}")
    else:
        print("🎉 All steps completed successfully!")
    
    print(f"\n🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show output files
    print(f"\n📁 Output files created:")
    output_files = [
        'stac_collections.json',
        'stac_search_results.json',
        'raster_data.csv',
        'parquet_data.csv',
        'output/combined_marine_data.csv',
        'output/combined_marine_data.parquet',
        'output/metadata.json'
    ]
    
    for file in output_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size:,} bytes)")
        else:
            print(f"  ❌ {file} (not found)")
    
    print(f"\n🎯 Next steps:")
    print("  - Review the output files")
    print("  - Explore the data in your preferred analysis environment")
    print("  - Run individual scripts for more detailed exploration")

if __name__ == "__main__":
    main()