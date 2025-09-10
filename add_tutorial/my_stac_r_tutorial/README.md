# STAC R Tutorial

This repository contains the `stac_r_tutorial.Rmd`, a tutorial designed to help users interact with SpatioTemporal Asset Catalogs (STAC) using R. The tutorial demonstrates how to query and visualize geospatial data efficiently.

## Requirements

To run this tutorial, you will need the following:

- **R and RStudio**: Ensure you have R (version 4.0 or higher) and RStudio installed.
- **R Packages**: The following R packages are required:
  - `rstac`
  - `ggplot2`
  - `dplyr`
  - `sf`
- **Docker**: Install Docker and Docker Compose if you prefer running the tutorial in a containerized environment.

## Getting Started

### Running Locally

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd my_stac_r_tutorial
   ```

2. Install the required R packages:
   ```R
   install.packages(c("rstac", "ggplot2", "dplyr", "sf"))
   ```

3. Open `stac_r_tutorial.Rmd` in RStudio and run the code chunks interactively.

### Running with Docker

### Running with Docker Compose

1. Start the services:
   ```bash
   docker compose up
   ```

2. Access RStudio in your browser at `http://localhost:8787` and log in with:
   - Username: `rstudio`
   - Password: `rstudiodemo`

## Credits

This tutorial was developed as part of the EDITO project. Special thanks to the contributors and the geospatial data community for their support.

## License

This project is licensed under the MIT License. See the LICENSE file for details.