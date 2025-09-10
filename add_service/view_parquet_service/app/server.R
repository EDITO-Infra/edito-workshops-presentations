# server.R
server <- function(input, output, session) {
  parquet_data <- reactiveVal(NULL)
  filtered_data <- reactiveVal(NULL)
  map_data <- reactiveVal(NULL)

  observeEvent(input$load_data, {
    req(input$parquet_url)
    tryCatch({
      dataset <- open_my_parquet(input$parquet_url)
      parquet_data(dataset)
      output$schema_output <- renderPrint({ dataset$schema })
      small_df <- dataset %>% head(100000) %>% collect()
      filtered_data(small_df)
    }, error = function(e) {
      showNotification(paste("Error loading dataset:", e$message), type = "error")
    })
  })

  observeEvent(input$update_map, {
    map_data(table_selected_data())
  })

  output$data_table <- renderDT({
    req(filtered_data())
    df <- filtered_data()
    if ("geometry" %in% colnames(df) && inherits(df$geometry[[1]], "raw")) {
      df$geometry <- vapply(
        df$geometry,
        function(x) st_as_text(st_as_sfc(list(x), EWKB = TRUE)),
        character(1)
      )
    }
    datatable(df, options = list(pageLength = 10, scrollX = TRUE),
              filter = "top", selection = "multiple", rownames = FALSE)
  })

  table_filtered_data <- reactive({
    req(filtered_data())
    df <- filtered_data()
    if (!is.null(input$data_table_rows_all)) {
      df[input$data_table_rows_all, ]
    } else {
      df
    }
  })

  table_selected_data <- reactive({
    rows <- input$data_table_rows_selected
    if (!is.null(rows) && length(rows) > 0) {
      table_filtered_data()[rows, ]
    } else {
      table_filtered_data()
    }
  })

  output$map <- renderLeaflet({
    req(map_data())
    df <- map_data()

    if ("geometry" %in% colnames(df)) {
      if (is.character(df$geometry)) {
        sf_data <- st_as_sf(df, wkt = "geometry")
      } else if (inherits(df$geometry[[1]], "raw")) {
        df$geometry <- lapply(df$geometry, function(x) {
          st_as_text(st_as_sfc(list(x), EWKB = TRUE))
        })
        sf_data <- st_as_sf(df, wkt = "geometry")
      } else {
        return(leaflet() %>% addTiles() %>%
                 addPopups(lng = 0, lat = 0, "Unsupported geometry format."))
      }

      sf_data <- st_simplify(sf_data, dTolerance = 0.01)
      popup_text <- apply(
        sf_data %>% st_drop_geometry(),
        1,
        function(row) paste0("<b>", names(row), ":</b> ", as.character(row), collapse = "<br>")
      )
      polygon_data <- sf_data[st_geometry_type(sf_data) %in% c("POLYGON", "MULTIPOLYGON"), ]
      point_data <- sf_data[st_geometry_type(sf_data) %in% c("POINT", "MULTIPOINT"), ]

      leaflet_map <- leaflet() %>% addTiles()

      if (nrow(polygon_data) > 0) {
        leaflet_map <- leaflet_map %>%
          addPolygons(data = polygon_data,
                      color = "blue", 
                      weight = 1, 
                      fillOpacity = 0.5, 
                      group = "Polygons",
                      popup = popup_text[match(st_as_text(st_geometry(polygon_data)), st_as_text(st_geometry(sf_data)))])
      }

      if (nrow(point_data) > 0) {
        leaflet_map <- leaflet_map %>%
          addCircleMarkers(data = point_data, 
                           radius = 5, 
                           color = "red", 
                           group = "Points",
                           popup = popup_text[match(st_as_text(st_geometry(point_data)), st_as_text(st_geometry(sf_data)))])
      }

      leaflet_map %>%
        addLayersControl(
          overlayGroups = c("Polygons", "Points"),
          options = layersControlOptions(collapsed = FALSE)
        ) %>%
        addDrawToolbar(targetGroup = "Selected") %>%
        addMeasure(
          position = "topright",
          primaryLengthUnit = "meters",
          primaryAreaUnit = "sqmeters",
          activeColor = "#3D535D",
          completedColor = "#7D4479"
        )
    } else {
      leaflet() %>% addTiles() %>% addPopups(lng = 0, lat = 0, "No geometry column found.")
    }
  })

  output$download_data <- downloadHandler(
    filename = function() {
      paste0("filtered_selection_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write.csv(table_selected_data(), file, row.names = FALSE)
    }
  )
}

