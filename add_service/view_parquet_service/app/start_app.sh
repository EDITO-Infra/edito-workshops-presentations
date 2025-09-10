#!/bin/bash
# This script shows where app is running and starts the shiny server
echo "🌐 App running at: http://localhost:3838/"
exec shiny-server --port 3838 --host 0.0.0.0