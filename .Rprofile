# EDITO Workshops - R Profile
# This file is automatically loaded when R starts in this project

# Load renv for package management
if (file.exists("renv.lock")) {
  source("renv/activate.R")
}

# Set project-specific options
options(
  repos = c(CRAN = "https://cran.rstudio.com/"),
  scipen = 999,
  digits = 4,
  stringsAsFactors = FALSE
)

# Load common packages for EDITO workshops
if (interactive()) {
  message("🌊 Welcome to EDITO Workshops!")
  message("📚 Loading common packages...")
  
  # Check if packages are available
  required_packages <- c("arrow", "dplyr", "ggplot2", "sf", "rstac")
  missing_packages <- required_packages[!sapply(required_packages, requireNamespace, quietly = TRUE)]
  
  if (length(missing_packages) > 0) {
    message("⚠️  Missing packages: ", paste(missing_packages, collapse = ", "))
    message("💡 Install with: install.packages(c('", paste(missing_packages, collapse = "', '"), "'))")
  } else {
    message("✅ All required packages available!")
  }
  
  message("🚀 Ready to explore marine data with EDITO!")
}
