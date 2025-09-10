# global.R

# Generic function to install packages if missing
install_packages_if_missing <- function(packages) {
  missing_packages <- packages[!sapply(packages, requireNamespace, quietly = TRUE)]
  if (length(missing_packages) > 0) {
    install.packages(missing_packages)
  }
}

# Define required packages
required_packages <- c("shiny", "arrow", "leaflet", "DT", "dplyr", "sf", "leaflet.extras", "shinythemes")

# Install missing packages
install_packages_if_missing(required_packages)

library(shiny)
library(arrow)
library(leaflet)
library(DT)
library(dplyr)
library(sf)
library(leaflet.extras)
library(shinythemes)

open_my_parquet <- function(s3_url) {
  temp <- strsplit(s3_url, "//")[[1]][2]
  endpoint <- strsplit(temp, "/")[[1]][1]
  data_path <- sub(paste0(endpoint, "/"), "", temp)
  data_lake <- S3FileSystem$create(anonymous = TRUE, scheme = "https", endpoint_override = endpoint)
  dataset <- NULL
  tryCatch({
    dataset <- arrow::open_dataset(data_path, filesystem = data_lake, format = "parquet")
  }, error = function(e) {
    cat("Error loading dataset:", e$message, "\n")
  })
  return(dataset)
}
