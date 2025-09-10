# ui.R

# Generic function to install packages if missing
install_packages_if_missing <- function(packages) {
  missing_packages <- packages[!sapply(packages, requireNamespace, quietly = TRUE)]
  if (length(missing_packages) > 0) {
    install.packages(missing_packages)
  }
}

# Define required packages
required_packages <- c("shinythemes")

# Install missing packages
install_packages_if_missing(required_packages)

ui <- fluidPage(
  theme = shinythemes::shinytheme("flatly"),
  titlePanel("🧭 Interactive Parquet Viewer"),
  fluidRow(
    column(
      width = 3,
      wellPanel(
        textInput("parquet_url", "Enter Parquet File URL:", value = ""),
        actionButton("load_data", "📥 Load Data"),
        actionButton("update_map", "🗺️ Put Filtered Data on Map"),
        downloadButton("download_data", "💾 Download CSV"),
        hr(),
        h4("🧬 Metadata Schema"),
        verbatimTextOutput("schema_output")
      )
    ),
    column(
      width = 9,
      tabsetPanel(
        tabPanel("📋 Interactive Table", DTOutput("data_table")),
        tabPanel("🗺️ Map", leafletOutput("map", height = "700px"))
      )
    )
  )
)
