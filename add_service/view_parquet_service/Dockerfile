FROM rocker/shiny:4.5.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libudunits2-dev \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libfontconfig1-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    && rm -rf /var/lib/apt/lists/*

# Install required R packages
RUN R -e "install.packages(c('shiny', 'arrow', 'leaflet', 'DT', 'dplyr', 'sf', 'leaflet.extras', 'shinythemes'))"

# Create app folder and copy files
RUN mkdir -p /srv/shiny-server
COPY app/ui.R app/server.R app/global.R /srv/shiny-server/

# Copy the startup script
COPY app/start_app.sh /start.sh
RUN chmod +x /start.sh

# Expose port
EXPOSE 3838

# Start Shiny server
CMD ["/start.sh"]
