# Interactive Parquet Viewer Service

This project provides an interactive tool to read and visualize Parquet files using R and Shiny. The service is containerized using Docker for easy deployment or can be run locally in RStudio.

## Updated Features

- **Interactive Table**: View and filter data from Parquet files.
- **Map Visualization**: Plot spatial data with geometry columns on an interactive map.
- **Metadata Schema**: Display the schema of the Parquet file.
- **CSV Export**: Download filtered data as a CSV file.
- **Custom Parquet URL Input**: Users can now input their own Parquet file URL directly in the app.

## Modularized Structure

The app is organized into three main components:
- **UI (`ui.R`)**: Defines the user interface layout and components.
- **Server (`server.R`)**: Implements the server-side logic for data processing and visualization.
- **Global (`global.R`)**: Contains shared resources and configurations used across the app.

## Requirements

### Local Use
To run the app locally in RStudio:
1. Install **R** (version 4.0 or higher) and **RStudio**.
2. Install the required R packages:
   ```R
   install.packages(c("shiny", "arrow", "leaflet", "DT", "dplyr", "sf", "leaflet.extras", "shinythemes"))
   ```
3. Clone this repository:
   ```bash
   git clone https://github.com/EDITO-Infra/edito-workshops-presentations.git
   cd edito-workshops-presentations/add_service/view_parquet_service
   ```
4. Run the app using the provided R script:
   ```R
   library(shiny)
   runApp('run_local.R')
   ```

### Docker Use
To run the app using Docker:
1. Install **Docker** on your system.
2. Build the Docker image:
   ```bash
   docker build -t interactive-parquet-viewer .
   ```
3. Run the Docker container:
   ```bash
   docker run -p 3838:3838 interactive-parquet-viewer
   ```
4. Access the app in your browser at `http://localhost:3838/`.

## File Descriptions

- **`ui.R`**: Defines the layout and components of the user interface.
- **`server.R`**: Implements the logic for loading, filtering, and visualizing Parquet data.
- **`global.R`**: Contains shared resources and configurations used across the app.
- **`run_local.R`**: Script to run the app locally in RStudio.
- **`Dockerfile`**: Sets up the environment to run the Shiny app in a Docker container.

## Notes
- Ensure your Parquet file is accessible via a public URL if hosted remotely.
- The app supports spatial data with geometry columns for map visualization.

## Authors and Contributors

generic.email@example.com

## License

This project is licensed under the MIT License.