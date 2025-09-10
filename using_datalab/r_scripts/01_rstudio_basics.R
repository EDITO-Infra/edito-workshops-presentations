# =============================================================================
# EDITO Datalab Tutorial: RStudio Service Basics
# =============================================================================
# This script demonstrates basic usage of RStudio service on EDITO Datalab
# Perfect for marine researchers getting started with cloud computing

# Load required packages
library(arrow)      # For reading Parquet files (ARCO data)
library(sf)         # For spatial data handling
library(dplyr)      # For data manipulation
library(ggplot2)    # For plotting
library(rstac)      # For accessing EDITO STAC API
library(terra)      # For raster data

# =============================================================================
# 1. EXPLORING EDITO DATA CATALOG
# =============================================================================

# Connect to EDITO STAC API
stac_endpoint <- "https://api.dive.edito.eu/data/"
collections <- stac(stac_endpoint) %>%
  rstac::collections() %>%
  get_request()

# See what data collections are available
print("Available data collections:")
for(i in 1:min(15, length(collections$collections))) {
  cat(i, ":", collections$collections[[i]]$id, "\n")
}

# =============================================================================
# 2. ACCESSING BIODIVERSITY DATA
# =============================================================================

# Search for biodiversity/occurrence data
biodiversity_collection <- stac(stac_endpoint) %>%
  rstac::collections() %>%
  rstac::get_collection("eurobis-occurrence-data") %>%
  get_request()

print(paste("Biodiversity collection:", biodiversity_collection$title))

# =============================================================================
# 3. READING ARCO DATA (Analysis Ready Cloud Optimized)
# =============================================================================

# Example: Read EUROBIS occurrence data in Parquet format
# This is much faster than traditional CSV files!
parquet_url <- "https://s3.waw3-1.cloudferro.com/emodnet/biology/eurobis_occurrence_data/eurobis_occurrences_geoparquet_2024-10-01.parquet"

# Read a sample of the data (first 1000 rows)
# Note: This is a large dataset, so we'll read just a sample
occurrence_data <- arrow::read_parquet(parquet_url) %>%
  head(1000)

# Explore the data structure
print("Data structure:")
str(occurrence_data)

print("Column names:")
colnames(occurrence_data)

# =============================================================================
# 4. MARINE BIODIVERSITY ANALYSIS
# =============================================================================

# Filter for marine species
marine_data <- occurrence_data %>%
  filter(!is.na(decimalLatitude) & !is.na(decimalLongitude)) %>%
  filter(decimalLatitude >= -90 & decimalLatitude <= 90) %>%
  filter(decimalLongitude >= -180 & decimalLongitude <= 180)

print(paste("Found", nrow(marine_data), "marine occurrence records"))

# Basic summary statistics
if(nrow(marine_data) > 0) {
  print("Top 10 species found:")
  top_species <- marine_data %>%
    count(scientificName, sort = TRUE) %>%
    head(10)
  print(top_species)
  
  # Create a simple map of occurrences
  if("geometry" %in% colnames(marine_data)) {
    # Convert to spatial data
    marine_sf <- st_as_sf(marine_data, wkt = "geometry")
    
    # Simple plot
    plot(marine_sf$geometry, main = "Marine Species Occurrences from EDITO Data")
  }
}

# =============================================================================
# 5. WORKING WITH OCEANOGRAPHIC DATA
# =============================================================================

# Search for oceanographic data (temperature, salinity, etc.)
ocean_collections <- stac(stac_endpoint) %>%
  rstac::collections() %>%
  get_request()

# Look for CMEMS (Copernicus Marine) data
cmems_collections <- ocean_collections$collections %>%
  purrr::keep(~grepl("cmems|CMEMS", .$id))

print("Available CMEMS oceanographic collections:")
for(i in 1:min(5, length(cmems_collections))) {
  cat(i, ":", cmems_collections[[i]]$id, "\n")
}

# Look for sea surface temperature data
sst_collections <- ocean_collections$collections %>%
  purrr::keep(~grepl("temperature|sst|SST", .$id, ignore.case = TRUE))

print("Available sea surface temperature collections:")
for(i in 1:min(3, length(sst_collections))) {
  cat(i, ":", sst_collections[[i]]$id, "\n")
}

# =============================================================================
# 6. WORKING WITH SATELLITE DATA
# =============================================================================

# Look for satellite data collections
satellite_collections <- ocean_collections$collections %>%
  purrr::keep(~grepl("satellite|sentinel|landsat|modis", .$id, ignore.case = TRUE))

print("Available satellite data collections:")
for(i in 1:min(5, length(satellite_collections))) {
  cat(i, ":", satellite_collections[[i]]$id, "\n")
}

# =============================================================================
# 7. SAVING YOUR WORK
# =============================================================================

# Save your results to your personal storage
# (This will be covered in the storage tutorial)

# For now, save locally
if(nrow(marine_data) > 0) {
  write.csv(marine_data, "marine_occurrences_sample.csv", row.names = FALSE)
  print("Marine data saved to marine_occurrences_sample.csv")
}

print("RStudio basics tutorial completed!")
print("Next: Try the Jupyter notebook or explore more data collections!")
