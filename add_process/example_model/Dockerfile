FROM rocker/r-ver:4.3.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install R packages
RUN R -e "install.packages(c('dplyr', 'ggplot2', 'readr', 'jsonlite', 'arrow'), repos='https://cran.r-project.org/')"

# Copy R scripts
COPY Scripts/ ./Scripts/

# Create directories
RUN mkdir -p /input-data /output-data

# Set environment variables
ENV EDITO_INFRA_OUTPUT=/output-data
ENV EDITO_INFRA_INPUT=/input-data

# Default command (will be overridden by Helm chart)
CMD ["Rscript", "/Scripts/01_data_preparation.R"]
