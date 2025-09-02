## Charts
-
Charts are, well, charts.  Each chart takes its input data from a View or a Table.  The category, or X axis (place on geocharts, X axis on column charts or line charts, Y axis on bar charts, wedge labels on donut or pie charts) is the first column in the view or table.  This is why an important part of constructing a view is reoordering columns.
The current set of Chart types supported by Galyleo are Google Charts; however, we intend to extend these chart types in the near future, to include OpenLayers, Leaflet.js, Chart.js, Cytoscape.js, and others.   It is the intent of the Galyleo system that *any* JavaScript/HTML5-hosted charts be available under Galyleo.

### Charts as Filters

One common operation in Dashboards is to use Charts as filters.  This enables drill-down and detail operations on particular categories.  Consider, for example, a table that gives average rating by manufacturer on the cereals example, where the data is shown on the dashboard as a column chart.  What we'd like is to see the detailed rating, by cereal brand, on another chart, filtered by manufacturer, and when the user clicks on the bar for a particular manufacturer on the average-rating chart the detail for that manufacturer is shown on the detail-rating chart.
Or consider the Presidential Election database example; when we click on a state, we see the vote for that state for the chosen year and the voting history for that state.
In both these cases, the chart is being used as a filter; it selects the manufacturer for the rating-detail chart and the state in the vote-history and vote-detail charts.
This is such a common use case that it is made a feature in Galyleo: every chart is a filter.  Specifically, it is a select filter on the category column of the View or Table that is input to the chart.  As we'll see below, charts show up in the same UI sections as filters.

### Names and Namespaces

References are by name in Galyleo; each object (Table, Filter, View, or Chart)  has a name.  Since a Chart can take input from a View or a Table, Views and Tables share the same namespace (Data Source) and a Table cannot have the same name as a View.  Similarly, since every Chart is also a Filter, Charts and Filters share the same namespace (Data Selectors), and a Chart cannot have the same name as a Filter or another Chart.  
Objects in different namespaces can share a name.  For example, it's quite common for a View and a Chart to share a name, when the View is the data source for the Chart and isn't otherwise used.

|---------------|-----------------|
| Namespace     | Objects         |
|---------------|-----------------|
| Data Source   | Tables, Views   |
| Data Selector | Charts, Filters |
|---------------|-----------------|