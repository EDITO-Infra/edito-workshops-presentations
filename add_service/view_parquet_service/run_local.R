# Load required libraries
if (!requireNamespace("shiny", quietly = TRUE)) install.packages("shiny")
if (!requireNamespace("arrow", quietly = TRUE)) install.packages("arrow")
if (!requireNamespace("leaflet", quietly = TRUE)) install.packages("leaflet")
if (!requireNamespace("DT", quietly = TRUE)) install.packages("DT")
if (!requireNamespace("dplyr", quietly = TRUE)) install.packages("dplyr")
if (!requireNamespace("sf", quietly = TRUE)) install.packages("sf")
if (!requireNamespace("leaflet.extras", quietly = TRUE)) install.packages("leaflet.extras")
if (!requireNamespace("shinythemes", quietly = TRUE)) install.packages("shinythemes")

# Source the app components
source("app/global.R")
source("app/ui.R")
source("app/server.R")

# Run the app
shinyApp(ui = ui, server = server)
