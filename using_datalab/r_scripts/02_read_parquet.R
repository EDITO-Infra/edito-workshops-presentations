# =============================================================================
# EDITO Datalab: Simple Parquet Reading Example
# =============================================================================
# This script shows how to read parquet files from EDITO data
# Perfect for a 15-minute tutorial on using EDITO Datalab

# Load required packages
library(arrow)      # For reading Parquet files
library(dplyr)      # For data manipulation
library(ggplot2)    # For plotting
library(sf)         # For spatial data

# =============================================================================
# 1. READ BIODIVERSITY DATA FROM PARQUET
# =============================================================================

print("🌊 Reading biodiversity data from parquet...")

# EUROBIS biodiversity occurrence data (marine species observations)
parquet_url <- "https://s3.waw3-1.cloudferro.com/emodnet/biology/eurobis_occurrence_data/eurobis_occurrences_geoparquet_2024-10-01.parquet"

# Read a sample of the data (first 1000 records for demo)
biodiversity_data <- arrow::read_parquet(parquet_url) %>%
  head(1000)

print(paste("✅ Loaded", nrow(biodiversity_data), "biodiversity records"))

# =============================================================================
# 2. EXPLORE THE DATA
# =============================================================================

print("\n📊 Data structure:")
print(str(biodiversity_data))

print("\n📋 First few records:")
print(head(biodiversity_data))

# =============================================================================
# 3. FILTER FOR MARINE SPECIES
# =============================================================================

print("\n🐠 Filtering for marine species...")

# Filter for marine species (fish, invertebrates, algae, etc.)
marine_data <- biodiversity_data %>%
  filter(grepl("fish|Fish|pisces|Pisces|mollusca|Mollusca|algae|Algae|crustacea|Crustacea", 
               scientificName, ignore.case = TRUE) |
         grepl("fish|Fish|mollusk|Mollusk|algae|Algae|crab|Crab", 
               vernacularName, ignore.case = TRUE))

print(paste("✅ Found", nrow(marine_data), "marine species records"))

# =============================================================================
# 4. SIMPLE ANALYSIS
# =============================================================================

if(nrow(marine_data) > 0) {
  print("\n📈 Marine species summary:")
  
  # Count by species
  species_count <- marine_data %>%
    count(scientificName, sort = TRUE) %>%
    head(10)
  
  print("Top 10 marine species:")
  print(species_count)
  
  # =============================================================================
  # 5. CREATE A SIMPLE MAP
  # =============================================================================
  
  print("\n🗺️ Creating map of marine biodiversity...")
  
  # Convert to spatial data
  marine_sf <- st_as_sf(marine_data, wkt = "geometry")
  
  # Create a simple map
  p <- ggplot(marine_sf) +
    geom_sf(aes(color = scientificName), size = 0.5) +
    labs(title = "Marine Biodiversity Occurrences",
         subtitle = paste("Total records:", nrow(marine_sf)),
         color = "Species") +
    theme_minimal() +
    theme(legend.position = "bottom")
  
  print(p)
  
} else {
  print("❌ No marine species found in the sample data")
}

print("\n✅ Parquet reading complete!")
print("💡 This demonstrates how to efficiently read large datasets from EDITO")

# =============================================================================
# 6. PERSONAL STORAGE CONNECTION
# =============================================================================

print("\n💾 Connecting to personal storage...")

# Check if storage credentials are available
if(Sys.getenv("AWS_ACCESS_KEY_ID") != "") {
  # cat("✅ Personal storage credentials found!\n")
  # cat("Storage endpoint:", Sys.getenv("AWS_S3_ENDPOINT"), "\n")
  # cat("Region:", Sys.getenv("AWS_DEFAULT_REGION"), "\n")
  
  # Example: Save processed data to personal storage
  if(nrow(marine_data) > 0) {
    # Save as CSV
    write.csv(marine_data, "marine_analysis_results.csv", row.names = FALSE)
    
    # Save as Parquet (more efficient)
    arrow::write_parquet(marine_data, "marine_analysis_results.parquet")
    
    cat("✅ Data saved locally\n")
    cat("- marine_analysis_results.csv\n")
    cat("- marine_analysis_results.parquet\n")
    cat("\n💡 Use aws.s3 package to upload to your personal storage\n")
  }
} else {
  cat("❌ No storage credentials found. Make sure you're running in EDITO Datalab.\n")
  cat("💡 Your credentials will be automatically available in EDITO services\n")
}

print("\n✅ Personal storage connection complete!")
