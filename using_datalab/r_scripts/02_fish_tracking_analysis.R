# =============================================================================
# EDITO Datalab Tutorial: Marine Biodiversity Data Analysis with ARCO Data
# =============================================================================
# This script demonstrates marine biodiversity data analysis using EDITO's ARCO data
# Perfect for researchers working with marine biodiversity and environmental data

# Load required packages
library(arrow)      # For reading Parquet files (ARCO data)
library(sf)         # For spatial data handling
library(dplyr)      # For data manipulation
library(ggplot2)    # For plotting
library(rstac)      # For accessing EDITO STAC API
library(terra)      # For raster data (environmental layers)
library(raster)     # Alternative raster package

# =============================================================================
# 1. SETUP: Accessing Marine Data Collections
# =============================================================================

# Connect to EDITO STAC API
stac_endpoint <- "https://api.dive.edito.eu/data/"

# Search for marine data collections
collections <- stac(stac_endpoint) %>%
  rstac::collections() %>%
  get_request()

# Look for oceanographic data collections
ocean_collections <- collections$collections %>%
  purrr::keep(~grepl("ocean|marine|sea|cmems", .$id, ignore.case = TRUE))

print("Oceanographic data collections:")
for(i in 1:min(10, length(ocean_collections))) {
  cat(i, ":", ocean_collections[[i]]$id, "-", ocean_collections[[i]]$title, "\n")
}

# =============================================================================
# 2. LOADING MARINE BIODIVERSITY OCCURRENCE DATA
# =============================================================================

# Read EUROBIS occurrence data (contains marine biodiversity observations)
parquet_url <- "https://s3.waw3-1.cloudferro.com/emodnet/biology/eurobis_occurrence_data/eurobis_occurrences_geoparquet_2024-10-01.parquet"

# Read a larger sample for analysis (5000 rows)
biodiversity_occurrences <- arrow::read_parquet(parquet_url) %>%
  head(5000)

print(paste("Loaded", nrow(biodiversity_occurrences), "occurrence records"))

# =============================================================================
# 3. FILTERING FOR MARINE SPECIES
# =============================================================================

# Filter for marine species using multiple criteria
marine_data <- biodiversity_occurrences %>%
  filter(
    # Filter by scientific name patterns for various marine taxa
    grepl("fish|Fish|pisces|Pisces|mollusca|Mollusca|algae|Algae|crustacea|Crustacea", scientificName, ignore.case = TRUE) |
    grepl("fish|Fish|mollusk|Mollusk|algae|Algae|crab|Crab|shrimp|Shrimp", vernacularName, ignore.case = TRUE) |
    # Filter by kingdom (if available)
    (kingdom == "Animalia" & phylum %in% c("Chordata", "Mollusca", "Arthropoda", "Echinodermata")) |
    (kingdom == "Plantae" & phylum %in% c("Rhodophyta", "Chlorophyta", "Ochrophyta"))
  )

print(paste("Found", nrow(marine_data), "marine biodiversity occurrence records"))

# =============================================================================
# 4. SPATIAL ANALYSIS OF MARINE BIODIVERSITY DISTRIBUTIONS
# =============================================================================

if(nrow(marine_data) > 0) {
  # Convert to spatial data
  marine_sf <- st_as_sf(marine_data, wkt = "geometry")
  
  # Basic spatial summary
  print("Spatial extent of marine biodiversity data:")
  print(st_bbox(marine_sf))
  
  # Plot marine biodiversity occurrences
  ggplot(marine_sf) +
    geom_sf(aes(color = scientificName), size = 0.5) +
    labs(title = "Marine Biodiversity Occurrences from EDITO Data",
         subtitle = paste("Total records:", nrow(marine_sf)),
         color = "Species") +
    theme_minimal() +
    theme(legend.position = "bottom")
  
  # Species diversity by region
  species_summary <- marine_sf %>%
    group_by(scientificName) %>%
    summarise(
      count = n(),
      .groups = "drop"
    ) %>%
    arrange(desc(count))
  
  print("Top 10 marine species by occurrence count:")
  print(head(species_summary, 10))
}

# =============================================================================
# 5. TEMPORAL ANALYSIS OF MARINE BIODIVERSITY OCCURRENCES
# =============================================================================

if(nrow(marine_data) > 0 && "eventDate" %in% colnames(marine_data)) {
  # Parse dates
  marine_data$date <- as.Date(marine_data$eventDate)
  
  # Remove records without valid dates
  marine_data <- marine_data %>%
    filter(!is.na(date))
  
  # Monthly occurrence patterns
  monthly_counts <- marine_data %>%
    mutate(month = format(date, "%Y-%m")) %>%
    group_by(month) %>%
    summarise(count = n(), .groups = "drop") %>%
    arrange(month)
  
  # Plot temporal patterns
  ggplot(monthly_counts, aes(x = month, y = count)) +
    geom_line(group = 1) +
    geom_point() +
    labs(title = "Marine Biodiversity Occurrences Over Time",
         x = "Month",
         y = "Number of Records") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
}

# =============================================================================
# 6. ACCESSING ENVIRONMENTAL DATA FOR HABITAT MODELING
# =============================================================================

# Search for oceanographic data that could be used for fish habitat modeling
ocean_collections <- stac(stac_endpoint) %>%
  rstac::collections() %>%
  get_request()

# Look for temperature, salinity, or other environmental variables
env_collections <- ocean_collections$collections %>%
  purrr::keep(~grepl("temperature|salinity|ocean|sea|marine", .$id, ignore.case = TRUE))

print("Available environmental data collections:")
for(i in 1:min(5, length(env_collections))) {
  cat(i, ":", env_collections[[i]]$id, "\n")
}

# =============================================================================
# 7. EXAMPLE: HABITAT SUITABILITY MODELING
# =============================================================================

# This is a simplified example of how you might use environmental data
# for marine habitat modeling

if(nrow(marine_data) > 0) {
  # Create a simple habitat model based on depth (if available)
  if("minimumDepthInMeters" %in% colnames(marine_data)) {
    # Filter out records without depth information
    marine_with_depth <- marine_data %>%
      filter(!is.na(minimumDepthInMeters) & minimumDepthInMeters > 0)
    
    if(nrow(marine_with_depth) > 0) {
      # Simple depth preference analysis
      depth_summary <- marine_with_depth %>%
        group_by(scientificName) %>%
        summarise(
          mean_depth = mean(minimumDepthInMeters, na.rm = TRUE),
          min_depth = min(minimumDepthInMeters, na.rm = TRUE),
          max_depth = max(minimumDepthInMeters, na.rm = TRUE),
          count = n(),
          .groups = "drop"
        ) %>%
        arrange(mean_depth)
      
      print("Marine species depth preferences:")
      print(head(depth_summary, 10))
      
      # Plot depth distribution
      ggplot(marine_with_depth, aes(x = minimumDepthInMeters)) +
        geom_histogram(bins = 30, fill = "skyblue", alpha = 0.7) +
        labs(title = "Distribution of Marine Biodiversity Occurrences by Depth",
             x = "Depth (meters)",
             y = "Frequency") +
        theme_minimal()
    }
  }
}

# =============================================================================
# 8. EXPORTING RESULTS FOR FURTHER ANALYSIS
# =============================================================================

# Save processed marine biodiversity data
if(nrow(marine_data) > 0) {
  # Save as CSV for further analysis
  write.csv(marine_data, "marine_biodiversity_analysis.csv", row.names = FALSE)
  
  # Save as GeoPackage for GIS software
  if(exists("marine_sf")) {
    st_write(marine_sf, "marine_occurrences.gpkg", delete_dsn = TRUE)
  }
  
  print("Results saved:")
  print("- marine_biodiversity_analysis.csv")
  print("- marine_occurrences.gpkg")
}

# =============================================================================
# 9. NEXT STEPS FOR MARINE RESEARCHERS
# =============================================================================

print("=== NEXT STEPS ===")
print("1. Explore more environmental data collections")
print("2. Integrate with your own marine biodiversity data")
print("3. Use Jupyter notebooks for more advanced analysis")
print("4. Access your personal storage for data persistence")
print("5. Consider using VSCode for larger projects")

print("Marine biodiversity analysis completed!")
