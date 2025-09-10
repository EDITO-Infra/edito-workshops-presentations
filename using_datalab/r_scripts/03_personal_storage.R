# =============================================================================
# EDITO Datalab Tutorial: Using Personal Storage
# =============================================================================
# This script demonstrates how to connect to and use personal storage
# on EDITO Datalab for data persistence and sharing

# Load required packages
library(arrow)      # For reading/writing Parquet files
library(aws.s3)     # For S3-compatible storage access
library(dplyr)      # For data manipulation
library(sf)         # For spatial data

# =============================================================================
# 1. SETUP: CONNECTING TO PERSONAL STORAGE
# =============================================================================

# Your personal storage credentials are automatically available in EDITO
# These environment variables are set when you launch a service

# Check if storage credentials are available
if(Sys.getenv("AWS_ACCESS_KEY_ID") != "") {
  print("✅ Personal storage credentials found!")
  print("Storage endpoint:", Sys.getenv("AWS_S3_ENDPOINT"))
  print("Region:", Sys.getenv("AWS_DEFAULT_REGION"))
} else {
  print("❌ No storage credentials found. Make sure you're running in EDITO Datalab.")
}

# =============================================================================
# 2. CONNECTING TO MINIO (EDITO's S3-compatible storage)
# =============================================================================

# Set up connection to EDITO's MinIO storage
# This uses the same interface as Amazon S3 but connects to EDITO's storage

# Configure AWS credentials for MinIO
Sys.setenv(
  "AWS_ACCESS_KEY_ID" = Sys.getenv("AWS_ACCESS_KEY_ID"),
  "AWS_SECRET_ACCESS_KEY" = Sys.getenv("AWS_SECRET_ACCESS_KEY"),
  "AWS_DEFAULT_REGION" = Sys.getenv("AWS_DEFAULT_REGION"),
  "AWS_SESSION_TOKEN" = Sys.getenv("AWS_SESSION_TOKEN"),
  "AWS_S3_ENDPOINT" = Sys.getenv("AWS_S3_ENDPOINT")
)

# =============================================================================
# 3. EXPLORING YOUR PERSONAL STORAGE
# =============================================================================

# List your personal buckets
tryCatch({
  buckets <- aws.s3::bucketlist()
  print("Your personal storage buckets:")
  print(buckets)
}, error = function(e) {
  print("Could not access storage. Make sure you're in EDITO Datalab with storage enabled.")
  print("Error:", e$message)
})

# =============================================================================
# 4. WORKING WITH YOUR PERSONAL BUCKET
# =============================================================================

# Get your personal bucket name (usually your username)
personal_bucket <- Sys.getenv("AWS_S3_BUCKET")
if(personal_bucket == "") {
  # Try to get from the first available bucket
  if(exists("buckets") && nrow(buckets) > 0) {
    personal_bucket <- buckets$Bucket[1]
  }
}

if(personal_bucket != "") {
  print(paste("Using personal bucket:", personal_bucket))
  
  # List contents of your personal bucket
  tryCatch({
    bucket_contents <- aws.s3::get_bucket(personal_bucket)
    print("Contents of your personal bucket:")
    print(bucket_contents)
  }, error = function(e) {
    print("Could not list bucket contents. This might be normal for a new bucket.")
  })
} else {
  print("Could not determine personal bucket name.")
}

# =============================================================================
# 5. SAVING DATA TO PERSONAL STORAGE
# =============================================================================

# Create some sample data to save
sample_data <- data.frame(
  species = c("Cod", "Haddock", "Mackerel", "Herring"),
  latitude = c(54.5, 55.2, 53.8, 54.1),
  longitude = c(3.2, 2.8, 3.5, 3.1),
  depth = c(45, 60, 25, 35),
  temperature = c(8.5, 7.2, 12.1, 9.8)
)

print("Sample fish data created:")
print(sample_data)

# Save as CSV to personal storage
if(personal_bucket != "") {
  tryCatch({
    # Save as CSV
    aws.s3::s3write_using(
      sample_data,
      FUN = write.csv,
      bucket = personal_bucket,
      object = "fish_data/sample_fish_data.csv",
      row.names = FALSE
    )
    print("✅ Sample data saved to personal storage as CSV")
    
    # Save as Parquet (more efficient for large datasets)
    aws.s3::s3write_using(
      sample_data,
      FUN = arrow::write_parquet,
      bucket = personal_bucket,
      object = "fish_data/sample_fish_data.parquet"
    )
    print("✅ Sample data saved to personal storage as Parquet")
    
  }, error = function(e) {
    print("Error saving to storage:")
    print(e$message)
  })
}

# =============================================================================
# 6. READING DATA FROM PERSONAL STORAGE
# =============================================================================

# Read data back from personal storage
if(personal_bucket != "") {
  tryCatch({
    # Read CSV
    loaded_csv <- aws.s3::s3read_using(
      FUN = read.csv,
      bucket = personal_bucket,
      object = "fish_data/sample_fish_data.csv"
    )
    print("✅ Data loaded from personal storage (CSV):")
    print(loaded_csv)
    
    # Read Parquet
    loaded_parquet <- aws.s3::s3read_using(
      FUN = arrow::read_parquet,
      bucket = personal_bucket,
      object = "fish_data/sample_fish_data.parquet"
    )
    print("✅ Data loaded from personal storage (Parquet):")
    print(loaded_parquet)
    
  }, error = function(e) {
    print("Error reading from storage:")
    print(e$message)
  })
}

# =============================================================================
# 7. WORKING WITH LARGER DATASETS
# =============================================================================

# For larger datasets, you can work directly with files in storage
# without loading everything into memory

# Example: Process a large fish tracking dataset
if(personal_bucket != "") {
  tryCatch({
    # Create a larger dataset
    large_fish_data <- data.frame(
      fish_id = rep(1:100, each = 10),
      timestamp = rep(seq(as.POSIXct("2024-01-01"), 
                         as.POSIXct("2024-01-10"), 
                         length.out = 10), 100),
      latitude = runif(1000, 50, 60),
      longitude = runif(1000, 0, 10),
      depth = runif(1000, 10, 100)
    )
    
    # Save large dataset
    aws.s3::s3write_using(
      large_fish_data,
      FUN = arrow::write_parquet,
      bucket = personal_bucket,
      object = "fish_data/large_tracking_dataset.parquet"
    )
    print("✅ Large tracking dataset saved to personal storage")
    
    # Read and process in chunks (memory efficient)
    # This is useful for very large datasets
    print("Processing large dataset in chunks...")
    
    # For demonstration, we'll read the whole thing
    # In practice, you might use arrow::open_dataset() for chunked processing
    loaded_large <- aws.s3::s3read_using(
      FUN = arrow::read_parquet,
      bucket = personal_bucket,
      object = "fish_data/large_tracking_dataset.parquet"
    )
    
    print(paste("✅ Loaded", nrow(loaded_large), "tracking records"))
    
  }, error = function(e) {
    print("Error with large dataset:")
    print(e$message)
  })
}

# =============================================================================
# 8. SHARING DATA WITH COLLABORATORS
# =============================================================================

# You can share data by making it publicly accessible
# or by sharing the bucket/object names with collaborators

if(personal_bucket != "") {
  print("=== DATA SHARING OPTIONS ===")
  print("1. Share bucket/object names with collaborators")
  print("2. Make objects publicly readable (if needed)")
  print("3. Export data to external services")
  print("4. Use EDITO's data sharing features")
  
  # List all your data files
  tryCatch({
    all_files <- aws.s3::get_bucket_df(personal_bucket, prefix = "fish_data/")
    print("Your fish data files:")
    print(all_files)
  }, error = function(e) {
    print("Could not list files (this might be normal)")
  })
}

# =============================================================================
# 9. BEST PRACTICES FOR FISH TRACKING DATA
# =============================================================================

print("=== BEST PRACTICES ===")
print("1. Use Parquet format for large datasets (faster, smaller)")
print("2. Organize data in folders (e.g., fish_data/, environmental_data/)")
print("3. Include metadata files describing your data")
print("4. Use consistent naming conventions")
print("5. Regular backups of important datasets")
print("6. Document your data processing steps")

# =============================================================================
# 10. CLEANUP AND NEXT STEPS
# =============================================================================

print("=== PERSONAL STORAGE TUTORIAL COMPLETED ===")
print("Next steps:")
print("1. Try the Jupyter notebook for Python storage access")
print("2. Explore VSCode for larger projects")
print("3. Learn about data sharing and collaboration")
print("4. Integrate with your fish tracking workflows")

print("Personal storage tutorial completed!")
