// Create root element
// https://www.amcharts.com/docs/v5/getting-started/#Root_element
function heatmap(data) {

var root = am5.Root.new("heatmap");
root._logo.dispose()


// Set themes
// https://www.amcharts.com/docs/v5/concepts/themes/
root.setThemes([
  am5themes_Animated.new(root),
]);


// Create chart
// https://www.amcharts.com/docs/v5/charts/xy-chart/
var chart = root.container.children.push(am5xy.XYChart.new(root, {
  panX: false,
  panY: false,
  wheelX: "none",
  wheelY: "none",
  paddingLeft: 0,
  layout: root.verticalLayout
}));

// Create axes and their renderers
var yRenderer = am5xy.AxisRendererY.new(root, {
  visible: false,
  minGridDistance: 20,
  inversed: true,
  minorGridEnabled: true
});

yRenderer.grid.template.set("visible", false);

yRenderer.labels.template.setAll({
    fill: am5.color(0xffffff),
    fontSize: 10,
})

var yAxis = chart.yAxes.push(am5xy.CategoryAxis.new(root, {
  maxDeviation: 0,
  renderer: yRenderer,
  categoryField: "week",
}));

var xRenderer = am5xy.AxisRendererX.new(root, {
  visible: false,
  minGridDistance: 30,
  opposite:true,
  minorGridEnabled: true
});

xRenderer.grid.template.set("visible", false);

xRenderer.labels.template.setAll({
    fill: am5.color(0xffffff),
})

var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
  renderer: xRenderer,
  categoryField: "weekday"
}));

// Create series
// https://www.amcharts.com/docs/v5/charts/xy-chart/#Adding_series
var series = chart.series.push(am5xy.ColumnSeries.new(root, {
  calculateAggregates: true,
  stroke: am5.color(0xffffff),
  clustered: false,
  xAxis: xAxis,
  yAxis: yAxis,
  categoryXField: "weekday",
  categoryYField: "week",
  valueField: "value"
}));


series.columns.template.setAll({
  tooltipText: "{value}",
  strokeOpacity: 1,
  strokeWidth: 1,
  width: am5.percent(100),
  height: am5.percent(100)
});

series.columns.template.events.on("pointerover", function(event) {
  var di = event.target.dataItem;
  if (di) {
    heatLegend.showValue(di.get("value", 0));
  }
});

series.events.on("datavalidated", function() {
  heatLegend.set("startValue", series.getPrivate("valueHigh"));
  heatLegend.set("endValue", series.getPrivate("valueLow"));
});


// Set up heat rules
// https://www.amcharts.com/docs/v5/concepts/settings/heat-rules/
series.set("heatRules", [{
  target: series.columns.template,
  min: am5.color(0x32292F),
  max: am5.color(0x8256AE),
  dataField: "value",
  key: "fill"
}]);

// Add heat legend
// https://www.amcharts.com/docs/v5/concepts/legend/heat-legend/
var heatLegend = chart.bottomAxesContainer.children.push(am5.HeatLegend.new(root, {
  orientation: "horizontal",
  endColor: am5.color(0x32292F),
  startColor: am5.color(0x8256AE),
  startText: "Highest",
  endText: "Lowest",
  stepCount: data.max_value
}));

heatLegend.startLabel.setAll({
    fontSize: 16,
    fill: am5.color(0xffffff),
});
  
heatLegend.endLabel.setAll({
    fontSize: 16,
    fill: am5.color(0xffffff),
});


// Set data
// https://www.amcharts.com/docs/v5/charts/xy-chart/#Setting_data
series.data.setAll(data.applications_by_date);

yAxis.data.setAll(data.week_periods);

xAxis.data.setAll([
    { weekday: "Sunday" },
    { weekday: "Monday" },
    { weekday: "Tuesday" },
    { weekday: "Wednesday" },
    { weekday: "Thursday" },
    { weekday: "Friday" },
    { weekday: "Saturday" }
]);

// Make stuff animate on load
// https://www.amcharts.com/docs/v5/concepts/animations/#Initial_animation
chart.appear(1000, 100);

}