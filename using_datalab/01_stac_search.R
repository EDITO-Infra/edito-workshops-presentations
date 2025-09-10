# =============================================================================
# EDITO Datalab: Simple STAC Search Example
# =============================================================================
# This script shows how to search the EDITO STAC catalog for marine data
# Perfect for a 15-minute tutorial on using EDITO Datalab

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
# 3. SEARCH FOR BIODIVERSITY DATA
# =============================================================================

print("\n🔍 Searching for biodiversity data...")

# Search for biodiversity/occurrence data
biodiversity_search <- stac(stac_endpoint) %>%
  stac_search(collections = "eurobis-occurrence-data") %>%
  get_request()

print(paste("✅ Found", length(biodiversity_search$features), "biodiversity items"))

# Show first few items
if(length(biodiversity_search$features) > 0) {
  print("\n📊 Sample biodiversity items:")
  for(i in 1:min(3, length(biodiversity_search$features))) {
    item <- biodiversity_search$features[[i]]
    cat(i, ":", item$id, "-", item$properties$title, "\n")
  }
}

# =============================================================================
# 4. GET DATA ACCESS URLS
# =============================================================================

print("\n🔗 Getting data access URLs...")

if(length(biodiversity_search$features) > 0) {
  first_item <- biodiversity_search$features[[1]]
  
  print("Available data formats:")
  for(asset_name in names(first_item$assets)) {
    asset <- first_item$assets[[asset_name]]
    cat("-", asset_name, ":", asset$href, "\n")
  }
}

print("\n✅ STAC search complete! Use these URLs to access the data.")
