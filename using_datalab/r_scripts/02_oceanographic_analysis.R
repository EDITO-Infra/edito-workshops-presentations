# =============================================================================
# EDITO Datalab Tutorial: Oceanographic Data Analysis with ARCO Data
# =============================================================================
# This script demonstrates oceanographic data analysis using EDITO's ARCO data
# Perfect for researchers working with marine environmental data

# Load required packages
library(arrow)      # For reading Parquet files (ARCO data)
library(sf)         # For spatial data handling
library(dplyr)      # For data manipulation
library(ggplot2)    # For plotting
library(rstac)      # For accessing EDITO STAC API
library(terra)      # For raster data (environmental layers)
library(ncdf4)      # For NetCDF files

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
# 2. WORKING WITH SEA SURFACE TEMPERATURE DATA
# =============================================================================

# Look for sea surface temperature (SST) data
sst_collections <- collections$collections %>%
  purrr::keep(~grepl("temperature|sst|SST", .$id, ignore.case = TRUE))

print("Sea Surface Temperature collections:")
for(i in 1:min(5, length(sst_collections))) {
  cat(i, ":", sst_collections[[i]]$id, "\n")
}

# Example: Access CMEMS SST data
if(length(sst_collections) > 0) {
  sst_collection <- sst_collections[[1]]
  print(paste("Selected SST collection:", sst_collection$id))
  
  # Get items from the collection
  sst_items <- stac(stac_endpoint) %>%
    rstac::collections() %>%
    rstac::get_collection(sst_collection$id) %>%
    rstac::items() %>%
    rstac::limit(5) %>%
    get_request()
  
  print(paste("Found", length(sst_items$features), "SST data items"))
}

# =============================================================================
# 3. WORKING WITH OCEAN CURRENTS DATA
# =============================================================================

# Look for ocean currents data
currents_collections <- collections$collections %>%
  purrr::keep(~grepl("current|velocity|u-velocity|v-velocity", .$id, ignore.case = TRUE))

print("Ocean currents collections:")
for(i in 1:min(5, length(currents_collections))) {
  cat(i, ":", currents_collections[[i]]$id, "\n")
}

# =============================================================================
# 4. WORKING WITH SALINITY DATA
# =============================================================================

# Look for salinity data
salinity_collections <- collections$collections %>%
  purrr::keep(~grepl("salinity|salt", .$id, ignore.case = TRUE))

print("Salinity collections:")
for(i in 1:min(5, length(salinity_collections))) {
  cat(i, ":", salinity_collections[[i]]$id, "\n")
}

# =============================================================================
# 5. WORKING WITH SEA LEVEL DATA
# =============================================================================

# Look for sea level data
sealevel_collections <- collections$collections %>%
  purrr::keep(~grepl("sea.level|sealevel|altimetry", .$id, ignore.case = TRUE))

print("Sea level collections:")
for(i in 1:min(5, length(sealevel_collections))) {
  cat(i, ":", sealevel_collections[[i]]$id, "\n")
}

# =============================================================================
# 6. WORKING WITH SATELLITE DATA
# =============================================================================

# Look for satellite data (Sentinel, MODIS, etc.)
satellite_collections <- collections$collections %>%
  purrr::keep(~grepl("sentinel|modis|landsat|satellite", .$id, ignore.case = TRUE))

print("Satellite data collections:")
for(i in 1:min(5, length(satellite_collections))) {
  cat(i, ":", satellite_collections[[i]]$id, "\n")
}

# =============================================================================
# 7. CREATING SAMPLE OCEANOGRAPHIC DATA FOR ANALYSIS
# =============================================================================

# Since we can't directly access large datasets in this demo,
# let's create sample oceanographic data for analysis

set.seed(42)
n_points <- 1000

# Create sample oceanographic data
ocean_data <- data.frame(
  longitude = runif(n_points, -10, 10),
  latitude = runif(n_points, 50, 60),
  sst = rnorm(n_points, 12, 2),  # Sea surface temperature
  salinity = rnorm(n_points, 35, 1),  # Salinity
  u_velocity = rnorm(n_points, 0, 0.5),  # Eastward velocity
  v_velocity = rnorm(n_points, 0, 0.5),  # Northward velocity
  depth = runif(n_points, 10, 200),  # Depth
  month = sample(1:12, n_points, replace = TRUE)
)

print(paste("Created sample oceanographic dataset with", nrow(ocean_data), "points"))

# =============================================================================
# 8. OCEANOGRAPHIC DATA ANALYSIS
# =============================================================================

# Basic statistics
print("Oceanographic data summary:")
print(summary(ocean_data))

# Calculate current speed
ocean_data$current_speed <- sqrt(ocean_data$u_velocity^2 + ocean_data$v_velocity^2)

# Create visualizations
par(mfrow = c(2, 2))

# Sea surface temperature map
plot(ocean_data$longitude, ocean_data$latitude, 
     col = heat.colors(10)[cut(ocean_data$sst, 10)],
     pch = 16, cex = 0.8,
     main = "Sea Surface Temperature",
     xlab = "Longitude", ylab = "Latitude")

# Salinity distribution
hist(ocean_data$salinity, breaks = 20, col = "lightblue",
     main = "Salinity Distribution",
     xlab = "Salinity (PSU)", ylab = "Frequency")

# Current speed
hist(ocean_data$current_speed, breaks = 20, col = "lightgreen",
     main = "Current Speed Distribution",
     xlab = "Speed (m/s)", ylab = "Frequency")

# SST vs Salinity
plot(ocean_data$sst, ocean_data$salinity, 
     pch = 16, cex = 0.6,
     main = "SST vs Salinity",
     xlab = "Sea Surface Temperature (°C)", 
     ylab = "Salinity (PSU)")

par(mfrow = c(1, 1))

# =============================================================================
# 9. SEASONAL ANALYSIS
# =============================================================================

# Analyze seasonal patterns
seasonal_sst <- ocean_data %>%
  group_by(month) %>%
  summarise(
    mean_sst = mean(sst, na.rm = TRUE),
    mean_salinity = mean(salinity, na.rm = TRUE),
    mean_speed = mean(current_speed, na.rm = TRUE),
    .groups = "drop"
  )

print("Seasonal patterns:")
print(seasonal_sst)

# Plot seasonal patterns
ggplot(seasonal_sst, aes(x = month)) +
  geom_line(aes(y = mean_sst, color = "SST"), size = 1) +
  geom_line(aes(y = mean_salinity, color = "Salinity"), size = 1) +
  labs(title = "Seasonal Oceanographic Patterns",
       x = "Month", y = "Value",
       color = "Variable") +
  theme_minimal()

# =============================================================================
# 10. SPATIAL ANALYSIS
# =============================================================================

# Convert to spatial data
ocean_sf <- st_as_sf(ocean_data, coords = c("longitude", "latitude"), crs = 4326)

# Create spatial plots
ggplot(ocean_sf) +
  geom_sf(aes(color = sst), size = 0.8) +
  scale_color_gradient2(low = "blue", mid = "white", high = "red",
                       midpoint = median(ocean_data$sst)) +
  labs(title = "Sea Surface Temperature Map",
       color = "SST (°C)") +
  theme_minimal()

# =============================================================================
# 11. CORRELATION ANALYSIS
# =============================================================================

# Calculate correlations between oceanographic variables
correlation_vars <- ocean_data %>%
  select(sst, salinity, u_velocity, v_velocity, current_speed, depth)

correlation_matrix <- cor(correlation_vars, use = "complete.obs")

print("Correlation matrix:")
print(round(correlation_matrix, 2))

# Visualize correlations
library(corrplot)
corrplot(correlation_matrix, method = "color", type = "upper",
         title = "Oceanographic Variables Correlation",
         mar = c(0,0,2,0))

# =============================================================================
# 12. EXPORTING RESULTS
# =============================================================================

# Save processed oceanographic data
write.csv(ocean_data, "oceanographic_analysis_results.csv", row.names = FALSE)
print("Oceanographic data saved to oceanographic_analysis_results.csv")

# Save as Parquet (more efficient)
arrow::write_parquet(ocean_data, "oceanographic_analysis_results.parquet")
print("Oceanographic data saved to oceanographic_analysis_results.parquet")

# Save spatial data
st_write(ocean_sf, "oceanographic_data.gpkg", delete_dsn = TRUE)
print("Spatial oceanographic data saved to oceanographic_data.gpkg")

# =============================================================================
# 13. NEXT STEPS FOR OCEANOGRAPHIC RESEARCH
# =============================================================================

print("=== NEXT STEPS ===")
print("1. Access real oceanographic data from EDITO collections")
print("2. Use Jupyter notebooks for more advanced analysis")
print("3. Integrate with your personal storage")
print("4. Explore VSCode for larger projects")
print("5. Consider using R Markdown for reproducible reports")

print("Oceanographic analysis tutorial completed!")
