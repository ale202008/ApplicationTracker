function chart(data) {

    // Create root element
    // https://www.amcharts.com/docs/v5/getting-started/#Root_element
    var root = am5.Root.new("chartdiv");
    root._logo.dispose()
    
    
    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    root.setThemes([
      am5themes_Animated.new(root)
    ]);
    
    
    // Create series
    // https://www.amcharts.com/docs/v5/charts/flow-charts/
    var series = root.container.children.push(am5flow.Sankey.new(root, {
      sourceIdField: "from",
      targetIdField: "to",
      valueField: "value",
      paddingRight: 50
    }));
    
    series.nodes.get("colors").set("step", 2);
    
    
    // Set data
    // https://www.amcharts.com/docs/v5/charts/flow-charts/#Setting_data
    series.data.setAll(data);
    
    
    // Make stuff animate on load
    series.appear(1000, 100);
    
    }; // end am5.ready()