#!/usr/bin/env python3
"""
EDITO Datalab Demo: Full Workflow Runner

This script runs the complete EDITO Datalab workflow by executing all
individual scripts in sequence. It provides a single entry point for
the entire data processing pipeline.
"""

import subprocess
import sys
import os
from datetime import datetime
import logging

def run_script(script_name, description):
    """
    Run a Python script and handle errors
    
    Args:
        script_name (str): Name of the script to run
        description (str): Description of what the script does
        
    Returns:
        bool: True if script ran successfully, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"🚀 Running: {script_name}")
    print(f"📝 Description: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        print("✅ Script completed successfully")
        if result.stdout:
            print("📤 Output:")
            print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Script failed with error code {e.returncode}")
        if e.stdout:
            print("📤 Output:")
            print(e.stdout)
        if e.stderr:
            print("❌ Error:")
            print(e.stderr)
        return False
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False

def check_dependencies():
    """
    Check if required dependencies are available
    
    Returns:
        bool: True if all dependencies are available
    """
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'requests', 'pandas', 'numpy', 'pyarrow', 'xarray', 
        'boto3', 'fsspec', 's3fs'
    ]
    
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
        print("💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies available")
    return True

def main():
    """Main function to run the complete workflow"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/edito_workflow.log', mode='a'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    logger.info("🌊 EDITO Datalab: Complete Workflow Runner")
    logger.info("=" * 60)
    logger.info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("🌊 EDITO Datalab: Complete Workflow Runner")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot proceed without required dependencies")
        logger.error("Cannot proceed without required dependencies")
        return
    
    # Define the workflow steps
    workflow_steps = [
        {
            'script': '01_get_stac_collections.py',
            'description': 'Get available STAC collections from EDITO API'
        },
        {
            'script': '02_search_stac_assets.py',
            'description': 'Search STAC for parquet and raster assets'
        },
        {
            'script': '03_get_zarr_to_df.py',
            'description': 'Process raster data and convert to DataFrame'
        },
        {
            'script': '04_get_parquet_data.py',
            'description': 'Process parquet data from STAC search'
        },
        {
            'script': '05_combine_and_save.py',
            'description': 'Combine datasets and save to storage'
        }
    ]
    
    # Track success/failure
    successful_steps = 0
    failed_steps = []
    
    # Run each step
    for i, step in enumerate(workflow_steps, 1):
        print(f"\n📋 Step {i}/{len(workflow_steps)}")
        logger.info(f"Step {i}/{len(workflow_steps)}: {step['script']}")
        
        success = run_script(step['script'], step['description'])
        
        if success:
            successful_steps += 1
            logger.info(f"Step {i} completed successfully: {step['script']}")
        else:
            failed_steps.append(step['script'])
            logger.error(f"Step {i} failed: {step['script']}")
            
            # Ask if user wants to continue
            response = input(f"\n❓ Script {step['script']} failed. Continue with remaining steps? (y/n): ")
            if response.lower() != 'y':
                print("🛑 Workflow stopped by user")
                logger.info("Workflow stopped by user")
                break
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 WORKFLOW SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful steps: {successful_steps}/{len(workflow_steps)}")
    
    logger.info(f"Workflow completed: {successful_steps}/{len(workflow_steps)} successful steps")
    
    if failed_steps:
        print(f"❌ Failed steps: {', '.join(failed_steps)}")
        logger.error(f"Failed steps: {', '.join(failed_steps)}")
    else:
        print("🎉 All steps completed successfully!")
        logger.info("All steps completed successfully!")
    
    print(f"\n🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show output files
    print(f"\n📁 Output files created:")
    output_files = [
        'stac_collections.json',
        'stac_parquet_items.json',
        'stac_raster_items.json',
        'raster_data.csv',
        'parquet_data.csv',
        'combined_marine_data.csv'
    ]
    
    for file in output_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size:,} bytes)")
            logger.info(f"Output file created: {file} ({size:,} bytes)")
        else:
            print(f"  ❌ {file} (not found)")
            logger.warning(f"Output file not found: {file}")
    
    print(f"\n🎯 Next steps:")
    print("  - Review the output files")
    print("  - Analyze the combined dataset")
    print("  - Create visualizations")
    print("  - Explore the data in your preferred analysis environment")

if __name__ == "__main__":
    main()
