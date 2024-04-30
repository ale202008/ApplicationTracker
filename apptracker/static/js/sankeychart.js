function chart(data) {

    // Create root element
    // https://www.amcharts.com/docs/v5/getting-started/#Root_element
    var root = am5.Root.new("chartdiv");
    root._logo.dispose()
    
    // Exporting
    var exporting = am5plugins_exporting.Exporting.new(root, {
      menu: am5plugins_exporting.ExportingMenu.new(root, {
        align: "left",
        valign: "bottom",
        container: document.getElementById("exportdiv"),
        fill: am5.color(0xffffff),
      })
    });

    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    root.setThemes([
      am5themes_Animated.new(root)
    ]);
    
    
    // Create series
    // https://www.amcharts.com/docs/v5/charts/flow-charts/
    var series = root.container.children.push(
      am5flow.Sankey.new(root, {
        sourceIdField: "from",
        targetIdField: "to",
        valueField: "value",
        paddingRight: 150,
        nodeWidth: 5,
        nodePadding: 150,
        paddingBottom: 50,
    }));
    
    series.nodes.get("colors").set("step", 2);
    
    
    
    // Set data
    // https://www.amcharts.com/docs/v5/charts/flow-charts/#Setting_data
    series.data.setAll(data);
    
    // Set styling
    series.nodes.rectangles.template.setAll({
      fillOpacity: 0.5,
      cornerRadiusTL: 4,
      cornerRadiusTR: 4,
      cornerRadiusBL: 4,
      cornerRadiusBR: 4
    });

    series.nodes.labels.template.setAll({
      text: "[bold]{name}[/] ({sumIncoming})",
      fontSize: 15,
      maxWidth: 140,
      oversizedBehavior: "wrap",
      brightness: 1,
      fill: am5.color(0xffffff),
      centerX: true,
    });

    series.nodes.rectangles.template.setAll({
      tooltipText: "[bold]{name}[/]\nOutgoing: {sumOutgoing}\nIncoming: {sumIncoming}"
    });
    
    // Make stuff animate on load
    series.appear(1000, 100);
    
    }; // end am5.ready()