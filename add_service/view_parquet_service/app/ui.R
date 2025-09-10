# ui.R
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
