#!/usr/bin/env Rscript

# 01_data_preparation.R
# First script: Data preparation and preprocessing
# This script reads input data from personal storage and prepares it for analysis

# Load required libraries
library(dplyr)
library(readr)
library(jsonlite)

# Set up paths
input_dir <- "/data/input"
output_dir <- "/data/output"
user_name <- Sys.getenv("USER_NAME", "default-user")

cat("=== Data Preparation Script ===\n")
cat("User:", user_name, "\n")
cat("Input directory:", input_dir, "\n")
cat("Output directory:", output_dir, "\n")

# Create output directory if it doesn't exist
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# Check if input directory exists and list files
if (dir.exists(input_dir)) {
  input_files <- list.files(input_dir, full.names = TRUE, recursive = TRUE)
  cat("Found", length(input_files), "input files:\n")
  for (file in input_files) {
    cat("  -", file, "\n")
  }
} else {
  cat("Warning: Input directory does not exist:", input_dir, "\n")
  cat("Creating sample data for demonstration...\n")
  
  # Create sample data if no input data is available
  set.seed(42)
  sample_data <- data.frame(
    id = 1:100,
    x = rnorm(100, mean = 10, sd = 2),
    y = rnorm(100, mean = 5, sd = 1.5),
    category = sample(c("A", "B", "C"), 100, replace = TRUE),
    timestamp = Sys.time() - runif(100, 0, 86400*30) # Last 30 days
  )
  
  # Save sample data to input directory
  dir.create(input_dir, recursive = TRUE)
  write_csv(sample_data, file.path(input_dir, "sample_data.csv"))
  cat("Sample data created at:", file.path(input_dir, "sample_data.csv"), "\n")
}

# Read input data
input_files <- list.files(input_dir, pattern = "\\.(csv|parquet)$", full.names = TRUE, recursive = TRUE)

if (length(input_files) == 0) {
  stop("No input data files found in ", input_dir)
}

# Process each input file
processed_data <- list()

for (file in input_files) {
  cat("Processing file:", basename(file), "\n")
  
  # Read data based on file extension
  if (grepl("\\.csv$", file)) {
    data <- read_csv(file, show_col_types = FALSE)
  } else if (grepl("\\.parquet$", file)) {
    data <- arrow::read_parquet(file)
  }
  
  # Basic data cleaning and preparation
  data_clean <- data %>%
    # Remove any rows with missing values in key columns
    filter(!is.na(x), !is.na(y)) %>%
    # Add derived variables
    mutate(
      x_squared = x^2,
      y_log = log(abs(y) + 1),
      ratio = x / (y + 0.001), # Avoid division by zero
      processed_at = Sys.time()
    )
  
  # Store processed data
  processed_data[[basename(file)]] <- data_clean
  
  cat("  - Rows:", nrow(data_clean), "\n")
  cat("  - Columns:", ncol(data_clean), "\n")
}

# Combine all processed data
if (length(processed_data) > 1) {
  combined_data <- bind_rows(processed_data, .id = "source_file")
} else {
  combined_data <- processed_data[[1]]
  combined_data$source_file <- names(processed_data)[1]
}

# Save processed data
processed_file <- file.path(output_dir, "processed_data.csv")
write_csv(combined_data, processed_file)

# Create summary statistics
summary_stats <- combined_data %>%
  group_by(category) %>%
  summarise(
    count = n(),
    mean_x = mean(x, na.rm = TRUE),
    mean_y = mean(y, na.rm = TRUE),
    sd_x = sd(x, na.rm = TRUE),
    sd_y = sd(y, na.rm = TRUE),
    .groups = "drop"
  )

# Save summary
summary_file <- file.path(output_dir, "data_summary.csv")
write_csv(summary_stats, summary_file)

# Create metadata
metadata <- list(
  script = "01_data_preparation.R",
  user = user_name,
  input_files = input_files,
  processed_at = Sys.time(),
  total_rows = nrow(combined_data),
  categories = unique(combined_data$category),
  output_files = c("processed_data.csv", "data_summary.csv")
)

metadata_file <- file.path(output_dir, "preparation_metadata.json")
write_json(metadata, metadata_file, pretty = TRUE)

cat("Data preparation completed!\n")
cat("Output files created:\n")
cat("  -", processed_file, "\n")
cat("  -", summary_file, "\n")
cat("  -", metadata_file, "\n")
cat("Total rows processed:", nrow(combined_data), "\n")
