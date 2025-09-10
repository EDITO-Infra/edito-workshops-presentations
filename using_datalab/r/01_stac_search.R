# =============================================================================
# EDITO Datalab: Simple STAC Search Example
# =============================================================================
# This script shows how to search the EDITO STAC catalog for marine data
# Perfect for a 15-minute tutorial on using EDITO Datalab

# Generic function to install packages if missing
install_packages_if_missing <- function(packages) {
  missing_packages <- packages[!sapply(packages, requireNamespace, quietly = TRUE)]
  if (length(missing_packages) > 0) {
    install.packages(missing_packages)
  }
}

# Define required packages
required_packages <- c("rstac", "dplyr")

# Install missing packages
install_packages_if_missing(required_packages)

# Load required packages
library(rstac)      # For accessing EDITO STAC API
library(dplyr)      # For data manipulation

# =============================================================================
# 1. CONNECT TO EDITO STAC API
# =============================================================================

print("🌊 Connecting to EDITO STAC API...")

# Connect to EDITO STAC API
stac_endpoint <- "https://api.dive.edito.eu/data/"

# Get available collections
collections <- stac(stac_endpoint) %>%
  rstac::collections() %>%
  get_request()

print(paste("✅ Found", length(collections$collections), "data collections"))

# =============================================================================
# 2. EXPLORE AVAILABLE COLLECTIONS
# =============================================================================

print("\n📋 Available data collections:")
for(i in 1:min(10, length(collections$collections))) {
  cat(i, ":", collections$collections[[i]]$id, "\n")
}

# =============================================================================
# 3. FIND BIODIVERSITY COLLECTIONS
# =============================================================================

print("\n🔍 Looking for biodiversity-related collections...")

# Find collections with biodiversity/occurrence/marine life keywords
biodiversity_collections <- collections$collections[sapply(collections$collections, function(collection) {
  title <- tolower(collection$title %||% "")
  description <- tolower(collection$description %||% "")
  id <- tolower(collection$id %||% "")
  
  any(grepl("biodiversity|occurrence|marine|fish|species|biology|eurobis", 
            paste(title, description, id), ignore.case = TRUE))
})]

print(paste("✅ Found", length(biodiversity_collections), "biodiversity-related collections"))

if(length(biodiversity_collections) > 0) {
  print("\n📊 Biodiversity collections:")
  for(i in 1:min(5, length(biodiversity_collections))) {
    cat(i, ":", biodiversity_collections[[i]]$id, "\n")
  }
  
  # =============================================================================
  # 4. SEARCH FOR BIODIVERSITY DATA
  # =============================================================================
  
  print("\n🔍 Searching for biodiversity data...")
  
  # Use the first biodiversity collection for the search
  first_bio_collection <- biodiversity_collections[[1]]$id
  
  biodiversity_search <- stac(stac_endpoint) %>%
    stac_search(collections = first_bio_collection) %>%
    get_request()
  
  print(paste("✅ Found", length(biodiversity_search$features), "biodiversity items from", first_bio_collection))
  
  # Show first few items
  if(length(biodiversity_search$features) > 0) {
    print("\n📊 Sample biodiversity items:")
    for(i in 1:min(3, length(biodiversity_search$features))) {
      item <- biodiversity_search$features[[i]]
      cat(i, ":", item$id, "-", item$properties$title %||% "No title", "\n")
    }
  }
} else {
  print("❌ No biodiversity collections found")
  biodiversity_search <- list(features = list())
}

# =============================================================================
# 5. GET DATA ACCESS URLS
# =============================================================================

print("\n🔗 Getting data access URLs...")

if(length(biodiversity_search$features) > 0) {
  first_item <- biodiversity_search$features[[1]]
  
  print("Available data formats:")
  for(asset_name in names(first_item$assets)) {
    asset <- first_item$assets[[asset_name]]
    cat("-", asset_name, ":", asset$href, "\n")
  }
} else {
  print("❌ No data items found to show URLs")
}

print("\n✅ STAC search complete! Use these URLs to access the data.")
