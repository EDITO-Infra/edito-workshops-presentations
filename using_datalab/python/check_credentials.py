#!/usr/bin/env python3
"""
Check EDITO Datalab Personal Storage Credentials
Run this in any EDITO Datalab service (RStudio, Jupyter, VSCode) terminal
"""

import os
import boto3
import logging

print("🔍 Checking EDITO Datalab Personal Storage Credentials")
print("=" * 60)

# Check if we're in EDITO Datalab
if os.getenv("AWS_ACCESS_KEY_ID"):
    print("✅ You're in EDITO Datalab! Credentials are available.")
    print()
    
    # Show credential information
    print("📋 Available Environment Variables:")
    print(f"  AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID', 'Not set')[:8]}...")
    print(f"  AWS_SECRET_ACCESS_KEY: {os.getenv('AWS_SECRET_ACCESS_KEY', 'Not set')[:8]}...")
    print(f"  AWS_SESSION_TOKEN: {os.getenv('AWS_SESSION_TOKEN', 'Not set')[:20]}...")
    print(f"  AWS_S3_ENDPOINT: {os.getenv('AWS_S3_ENDPOINT', 'Not set')}")
    print(f"  AWS_DEFAULT_REGION: {os.getenv('AWS_DEFAULT_REGION', 'Not set')}")
    print()
    
    # Test connection
    print("🔗 Testing connection to personal storage...")
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=f"https://{os.getenv('AWS_S3_ENDPOINT')}",
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
        )
        
        # List buckets
        response = s3.list_buckets()
        print("✅ Successfully connected to personal storage!")
        print(f"📁 Available buckets: {[bucket['Name'] for bucket in response['Buckets']]}")
        
    except Exception as e:
        print(f"❌ Error connecting to storage: {e}")
        
else:
    print("❌ No credentials found. Make sure you're running in EDITO Datalab.")
    print("💡 Your credentials are automatically available when you launch a service.")
    print("💡 No need to go to project settings - they're already there!")

print()
print("🚀 To use these credentials in your code:")
print("   Python: os.getenv('AWS_ACCESS_KEY_ID')")
print("   R: Sys.getenv('AWS_ACCESS_KEY_ID')")
print("   Terminal: echo $AWS_ACCESS_KEY_ID")
