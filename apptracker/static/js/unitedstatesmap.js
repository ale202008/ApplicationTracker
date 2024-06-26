function map(data) {

// =================================
// Create map chart
// =================================

// Create root and chart
var root = am5.Root.new("map"); 
root._logo.dispose()

// Set themes
root.setThemes([
  am5themes_Animated.new(root)
]);

var chart = root.container.children.push(
  am5map.MapChart.new(root, {
    panX: "rotateX",
    projection: am5map.geoAlbersUsa()
  })
);

// Create polygon series
var polygonSeries = chart.series.push(
  am5map.MapPolygonSeries.new(root, {
    geoJSON: am5geodata_usaLow
  })
);

polygonSeries.mapPolygons.template.setAll({
  tooltipText: "{name}"
});

polygonSeries.mapPolygons.template.states.create("hover", {
  fill: am5.color(0x297373)
});

var zoomOut = root.tooltipContainer.children.push(am5.Button.new(root, {
  x: am5.p100,
  y: 0,
  centerX: am5.p100,
  centerY: 0,
  paddingTop: 18,
  paddingBottom: 18,
  paddingLeft: 12,
  paddingRight: 12,
  dx: -20,
  dy: 20,
  themeTags: ["zoom"],
  icon: am5.Graphics.new(root, {
    themeTags: ["button", "icon"],
    strokeOpacity: 0.7,
    draw: function(display) {
      display.moveTo(0, 0);
      display.lineTo(12, 0);
    }
  })
}));

zoomOut.get("background").setAll({
  cornerRadiusBL: 40,
  cornerRadiusBR: 40,
  cornerRadiusTL: 40,
  cornerRadiusTR: 40
});
zoomOut.events.on("click", function() {
  if (currentSeries) {
    currentSeries.hide();
  }
  chart.goHome();
  zoomOut.hide();
  currentSeries = regionalSeries.US.series;
  currentSeries.show();
});
zoomOut.hide();


// =================================
// Set up point series
// =================================

// Load store data
am5.net.load("").then(function(result) {
  setupStores(data);
});

var regionalSeries = {};
var currentSeries;

// Parses data and creats map point series for domestic and state-level
function setupStores(data) {

  // Init country-level series
  regionalSeries.US = {
    markerData: [],
    series: createSeries("stores")
  };
  
  // Set current series
  currentSeries = regionalSeries.US.series;
  
  // Process data
  am5.array.each(data.query_results, function(store) {

    // Get store data
    var store = {
      state: store.MAIL_ST_PROV_C,
      long: am5.type.toNumber(store.LNGTD_I),
      lat: am5.type.toNumber(store.LATTD_I),
      city: store.mail_city_n,
    };
    
    // Process state-level data
    if (regionalSeries[store.state] == undefined) {
      var statePolygon = getPolygon("US-" + store.state);
      if (statePolygon) {
        var centroid = statePolygon.visualCentroid();

        // Add state data
        regionalSeries[store.state] = {
          target: store.state,
          type: "state",
          name: statePolygon.dataItem.dataContext.name,
          stores: 1,
          state: store.state,
          markerData: [],
          geometry: {
            type: "Point",
            coordinates: [centroid.longitude, centroid.latitude]
          }
        };
        regionalSeries.US.markerData.push(regionalSeries[store.state]);


      }
      else {
        // State not found
        return;
      }
    }
    else {
      regionalSeries[store.state].stores++;
    }
    
    // Process city-level data
    if (regionalSeries[store.city] == undefined) {
      regionalSeries[store.city] = {
        target: store.city,
        type: "city",
        name: store.city,
        stores: 1,
        state: store.state,
        markerData: [],
        geometry: {
          type: "Point",
          coordinates: [store.long, store.lat]
        }
      };
      regionalSeries[store.state].markerData.push(regionalSeries[store.city]);
    }
    else {
      regionalSeries[store.city].stores++;
    }

    
  });
  console.log(regionalSeries.US.markerData)
  regionalSeries.US.series.data.setAll(regionalSeries.US.markerData);
}

// Finds polygon in series by its id
function getPolygon(id) {
    var found;
    polygonSeries.mapPolygons.each(function(polygon) {
        if (polygon.dataItem.get("id") == id) {
            found = polygon;
        }
    })
  return found;
}

// Creates series with heat rules
function createSeries(heatfield) {
  
  // Create point series
  var pointSeries = chart.series.push(
    am5map.MapPointSeries.new(root, {
      valueField: heatfield,
      calculateAggregates: true
    })
  );
  
  // Add store bullet
  var circleTemplate = am5.Template.new(root);
  pointSeries.bullets.push(function() {
    var container = am5.Container.new(root, {});
    
    var circle = container.children.push(am5.Circle.new(root, {
      radius: 10,
      fill: am5.color(0x000000),
      fillOpacity: 0.7,
      cursorOverStyle: "pointer",
      tooltipText: "{name}:\n[bold]{stores} applications[/]"
    }, circleTemplate));
    
    var label = container.children.push(am5.Label.new(root, {
      text: "{stores}",
      fill: am5.color(0xffffff),
      populateText: true,
      centerX: am5.p50,
      centerY: am5.p50,
      textAlign: "center"
    }));
    
    // Set up drill-down
    circle.events.on("click", function(ev) {
      
      // Determine what we've clicked on
      var data = ev.target.dataItem.dataContext;

      // No id? Individual store - nothing to drill down to further
      if (!data.target) {
        return;
      }
      
      // Create actual series if it hasn't been yet created
      if (!regionalSeries[data.target].series) {
        regionalSeries[data.target].series = createSeries("cities");
        regionalSeries[data.target].series.data.setAll(data.markerData);
      }

      // Hide current series
      if (currentSeries) {
        currentSeries.hide();
      }
      
      // Control zoom
      if (data.type == "state") {
        var statePolygon = getPolygon("US-" + data.state);
        polygonSeries.zoomToDataItem(statePolygon.dataItem);
      }
      else if (data.type == "city") {
        chart.zoomToGeoPoint({
          latitude: data.geometry.coordinates[1],
          longitude: data.geometry.coordinates[0]
        }, 64, true);
      }
      zoomOut.show();

      // Show new target series
      currentSeries = regionalSeries[data.target].series;
      currentSeries.show();
    });
    
    return am5.Bullet.new(root, {
      sprite: container
    });
  });
  
  // Add heat rule for circles
  pointSeries.set("heatRules", [{
    target: circleTemplate,
    dataField: "value",
    min: 10,
    max: 20,
    key: "radius"
  }])
  
  // Set up drill-down
  // TODO
  
  return pointSeries;
}

    
}