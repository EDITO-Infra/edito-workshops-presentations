# =============================================================================
# EDITO Datalab: Personal Storage Connection Example
# =============================================================================
# This script shows how to connect to personal storage and transfer data
# Perfect for a 15-minute tutorial on using EDITO Datalab

# Generic function to install packages if missing
install_packages_if_missing <- function(packages) {
  missing_packages <- packages[!sapply(packages, requireNamespace, quietly = TRUE)]
  if (length(missing_packages) > 0) {
    install.packages(missing_packages)
  }
}

# Define required packages
required_packages <- c("aws.s3", "arrow", "dplyr")

# Install missing packages
install_packages_if_missing(required_packages)

# Load required packages
library(aws.s3)     # For S3 storage access
library(arrow)      # For reading Parquet files
library(dplyr)      # For data manipulation

# =============================================================================
# 1. CHECK STORAGE CREDENTIALS
# =============================================================================

print("💾 Checking personal storage credentials...")

# Check if storage credentials are available
if(Sys.getenv("AWS_ACCESS_KEY_ID") != "") {
  cat("✅ Personal storage credentials found!\n")
  cat("Storage endpoint:", Sys.getenv("AWS_S3_ENDPOINT"), "\n")
  cat("Region:", Sys.getenv("AWS_DEFAULT_REGION"), "\n")
  cat("Access Key ID:", substr(Sys.getenv("AWS_ACCESS_KEY_ID"), 1, 8), "...\n")
} else {
  cat("❌ No storage credentials found. Make sure you're running in EDITO Datalab.\n")
  cat("💡 Your credentials will be automatically available in EDITO services\n")
  cat("💡 For demo purposes, we'll show the connection code\n")
}

# =============================================================================
# 2. CONNECT TO PERSONAL STORAGE
# =============================================================================

print("\n🔗 Connecting to personal storage...")

# In EDITO Datalab, your credentials are automatically available as environment variables
# No need to go to project settings - they're already there!

# Get credentials from environment variables
aws_access_key_id <- Sys.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key <- Sys.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token <- Sys.getenv("AWS_SESSION_TOKEN")
s3_endpoint <- Sys.getenv("AWS_S3_ENDPOINT")
s3_region <- Sys.getenv("AWS_DEFAULT_REGION")

# Check if credentials are available
if(aws_access_key_id != "") {
  cat("✅ AWS credentials found in environment variables!\n")
#   cat("Storage endpoint:", s3_endpoint, "\n")
#   cat("Region:", s3_region, "\n")
#   cat("Access Key ID:", substr(aws_access_key_id, 1, 8), "...\n")
  
  # Set AWS credentials for aws.s3 package
  Sys.setenv(
    "AWS_ACCESS_KEY_ID" = aws_access_key_id,
    "AWS_SECRET_ACCESS_KEY" = aws_secret_access_key,
    "AWS_SESSION_TOKEN" = aws_session_token,
    "AWS_DEFAULT_REGION" = s3_region
  )
  
  cat("✅ AWS credentials configured!\n")
} else {
  cat("❌ No storage credentials found. Make sure you're running in EDITO Datalab.\n")
  cat("💡 Your credentials are automatically available in EDITO services\n")
  cat("💡 No need to go to project settings - they're already there!\n")
}

# =============================================================================
# 3. CREATE SAMPLE DATA
# =============================================================================

print("\n📊 Creating sample marine data...")

# Create sample marine biodiversity data
marine_data <- data.frame(
  scientificName = rep(c("Scomber scombrus", "Gadus morhua", "Pleuronectes platessa"), 100),
  decimalLatitude = runif(300, 50, 60),
  decimalLongitude = runif(300, 0, 10),
  eventDate = seq(as.Date("2020-01-01"), as.Date("2023-12-31"), length.out = 300),
  depth = runif(300, 5, 200),
  temperature = rnorm(300, 10, 3)
)

print(paste("✅ Created", nrow(marine_data), "marine records"))

# =============================================================================
# 4. PROCESS DATA
# =============================================================================

print("\n🔄 Processing data...")

# Process the data
processed_data <- marine_data %>%
  group_by(scientificName) %>%
  summarise(
    count = n(),
    mean_latitude = mean(decimalLatitude, na.rm = TRUE),
    mean_longitude = mean(decimalLongitude, na.rm = TRUE),
    mean_depth = mean(depth, na.rm = TRUE),
    mean_temperature = mean(temperature, na.rm = TRUE),
    .groups = "drop"
  )

print("✅ Data processed!")
print(processed_data)

# =============================================================================
# 5. SAVE DATA LOCALLY
# =============================================================================

print("\n💾 Saving data locally...")

# Save as CSV
write.csv(processed_data, "processed_marine_data.csv", row.names = FALSE)

# Save as Parquet (more efficient)
arrow::write_parquet(processed_data, "processed_marine_data.parquet")

cat("✅ Data saved locally:\n")
cat("- processed_marine_data.csv\n")
cat("- processed_marine_data.parquet\n")

# =============================================================================
# 6. UPLOAD TO PERSONAL STORAGE
# =============================================================================

print("\n☁️ Uploading to personal storage...")

# Get your bucket name from environment or use a default
bucket_name <- Sys.getenv("AWS_S3_BUCKET", "your-bucket-name")

if(aws_access_key_id != "") {
  tryCatch({
    # Upload CSV file
    aws.s3::s3write_using(
      processed_data, 
      FUN = write.csv, 
      bucket = bucket_name, 
      object = "marine_analysis/processed_marine_data.csv",
      row.names = FALSE
    )
    
    # Upload Parquet file
    aws.s3::s3write_using(
      processed_data, 
      FUN = arrow::write_parquet, 
      bucket = bucket_name, 
      object = "marine_analysis/processed_marine_data.parquet"
    )
    
    cat("✅ Data uploaded to personal storage!\n")
    cat("📁 Files uploaded to:", paste0("s3://", bucket_name, "/marine_analysis/\n"))
    
  }, error = function(e) {
    cat("❌ Error uploading to storage:", e$message, "\n")
    cat("💡 Make sure to replace 'your-bucket-name' with your actual bucket name\n")
  })
} else {
  cat("💡 To upload to storage, make sure you're running in EDITO Datalab\n")
  cat("💡 Your credentials are automatically available as environment variables\n")
}

# =============================================================================
# 7. DOWNLOAD FROM PERSONAL STORAGE
# =============================================================================

print("\n📥 Downloading from personal storage...")

if(aws_access_key_id != "") {
  tryCatch({
    # Download CSV file
    downloaded_data <- aws.s3::s3read_using(
      FUN = read.csv,
      bucket = bucket_name,
      object = "marine_analysis/processed_marine_data.csv"
    )
    
    cat("✅ Data downloaded from personal storage!\n")
    cat("📊 Downloaded", nrow(downloaded_data), "records\n")
    print(head(downloaded_data))
    
  }, error = function(e) {
    cat("❌ Error downloading from storage:", e$message, "\n")
    cat("💡 Make sure the file exists in your storage\n")
  })
} else {
  cat("💡 To download from storage, make sure you're running in EDITO Datalab\n")
  cat("💡 Your credentials are automatically available as environment variables\n")
}

# =============================================================================
# 8. SUMMARY
# =============================================================================

print("\n✅ Personal storage workflow complete!")
print("💡 This demonstrates how to:")
print("   - Connect to personal storage")
print("   - Process and save data")
print("   - Upload to cloud storage")
print("   - Download from cloud storage")
print("\n🌊 Ready to use EDITO Datalab for your marine research!")
