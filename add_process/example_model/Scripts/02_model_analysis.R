#!/usr/bin/env Rscript

# 02_model_analysis.R
# Second script: Model analysis and prediction
# This script performs statistical analysis and creates visualizations

# Load required libraries
library(dplyr)
library(ggplot2)
library(jsonlite)

# Set up paths
input_dir <- "/data/input"
output_dir <- "/data/output"
user_name <- Sys.getenv("USER_NAME", "default-user")

cat("=== Model Analysis Script ===\n")
cat("User:", user_name, "\n")
cat("Input directory:", input_dir, "\n")
cat("Output directory:", output_dir, "\n")

# Check if processed data exists from previous script
processed_file <- file.path(output_dir, "processed_data.csv")
if (!file.exists(processed_file)) {
  stop("Processed data not found. Please run 01_data_preparation.R first.")
}

# Read processed data
cat("Reading processed data from:", processed_file, "\n")
data <- read_csv(processed_file, show_col_types = FALSE)
cat("Loaded", nrow(data), "rows of data\n")

# Perform statistical analysis
cat("Performing statistical analysis...\n")

# Linear regression model
model <- lm(y ~ x + x_squared + category, data = data)
model_summary <- summary(model)

# Create predictions
data$predicted_y <- predict(model, data)
data$residuals <- data$y - data$predicted_y

# Calculate model performance metrics
r_squared <- model_summary$r.squared
rmse <- sqrt(mean(data$residuals^2))
mae <- mean(abs(data$residuals))

cat("Model performance:\n")
cat("  - R-squared:", round(r_squared, 4), "\n")
cat("  - RMSE:", round(rmse, 4), "\n")
cat("  - MAE:", round(mae, 4), "\n")

# Save model results
results_file <- file.path(output_dir, "model_results.csv")
write_csv(data, results_file)

# Create visualizations
cat("Creating visualizations...\n")

# 1. Scatter plot with regression line
p1 <- ggplot(data, aes(x = x, y = y)) +
  geom_point(aes(color = category), alpha = 0.7) +
  geom_line(aes(y = predicted_y), color = "red", size = 1) +
  labs(
    title = "Linear Regression Model",
    subtitle = paste("R² =", round(r_squared, 3)),
    x = "X variable",
    y = "Y variable",
    color = "Category"
  ) +
  theme_minimal() +
  theme(legend.position = "bottom")

# Save plot 1
plot1_file <- file.path(output_dir, "regression_plot.png")
ggsave(plot1_file, p1, width = 10, height = 6, dpi = 300)

# 2. Residuals plot
p2 <- ggplot(data, aes(x = predicted_y, y = residuals)) +
  geom_point(aes(color = category), alpha = 0.7) +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed") +
  labs(
    title = "Residuals Plot",
    x = "Predicted Values",
    y = "Residuals",
    color = "Category"
  ) +
  theme_minimal() +
  theme(legend.position = "bottom")

# Save plot 2
plot2_file <- file.path(output_dir, "residuals_plot.png")
ggsave(plot2_file, p2, width = 10, height = 6, dpi = 300)

# 3. Category comparison
p3 <- ggplot(data, aes(x = category, y = y)) +
  geom_boxplot(aes(fill = category), alpha = 0.7) +
  geom_jitter(width = 0.2, alpha = 0.5) +
  labs(
    title = "Y Variable by Category",
    x = "Category",
    y = "Y variable",
    fill = "Category"
  ) +
  theme_minimal() +
  theme(legend.position = "none")

# Save plot 3
plot3_file <- file.path(output_dir, "category_comparison.png")
ggsave(plot3_file, p3, width = 8, height = 6, dpi = 300)

# Create model summary
model_summary_data <- data.frame(
  metric = c("R_squared", "RMSE", "MAE", "n_observations", "n_predictors"),
  value = c(r_squared, rmse, mae, nrow(data), length(coef(model)) - 1)
)

summary_file <- file.path(output_dir, "model_summary.csv")
write_csv(model_summary_data, summary_file)

# Create detailed model output
model_details <- list(
  script = "02_model_analysis.R",
  user = user_name,
  model_type = "Linear Regression",
  formula = "y ~ x + x_squared + category",
  coefficients = as.list(coef(model)),
  performance = list(
    r_squared = r_squared,
    rmse = rmse,
    mae = mae
  ),
  data_info = list(
    n_observations = nrow(data),
    n_categories = length(unique(data$category)),
    categories = unique(data$category)
  ),
  output_files = c("model_results.csv", "model_summary.csv", 
                   "regression_plot.png", "residuals_plot.png", 
                   "category_comparison.png"),
  created_at = Sys.time()
)

# Save model details
model_file <- file.path(output_dir, "model_details.json")
write_json(model_details, model_file, pretty = TRUE)

cat("Model analysis completed!\n")
cat("Output files created:\n")
cat("  -", results_file, "\n")
cat("  -", summary_file, "\n")
cat("  -", plot1_file, "\n")
cat("  -", plot2_file, "\n")
cat("  -", plot3_file, "\n")
cat("  -", model_file, "\n")

# Final summary
cat("\n=== Final Summary ===\n")
cat("Total files in output directory:", length(list.files(output_dir)), "\n")
cat("Output directory contents:\n")
for (file in list.files(output_dir)) {
  file_path <- file.path(output_dir, file)
  file_size <- file.size(file_path)
  cat("  -", file, "(", round(file_size/1024, 2), "KB )\n")
}
