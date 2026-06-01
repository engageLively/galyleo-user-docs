Galyleo User Documentation
------------------------------
This is the user guide for the Galyleo Service

# Examples and Tutorials
There are a number of examples and tutorials designed to help new users quickly get started with Galyleo.

### Examples
Some example dashboards built with Galyleo can be found here:

- [Presidential Elections](https://storage.googleapis.com/user-galyleo-dashboards/published/index.html?dashboard=https://storage.googleapis.com/user-galyleo-dashboards/dashboards/1/elections.gd.json)

- [UFOs](https://storage.googleapis.com/user-galyleo-dashboards/published/index.html?dashboard=https://storage.googleapis.com/user-galyleo-dashboards/dashboards/1/ufos.gd.json)

- [Sea Ice Coverage](https://galyleo.app/published/index.html?dashboard=https://storage.googleapis.com/user-galyleo-dashboards/dashboards/0/seaice.gd.json)

### Building the Examples
The examples (and the data that drives them) can be found in the Galyleo Examples github repository at [Galyleo Examples](https://github.com/engageLively/galyleo-examples).  The typical workflow to build a dashboard is to create a data set in [SDML](https://global-data-plane.github.io/sdtp/sdml_reference/) format and then publish that to a Galyleo data repository (one is hosted with every Galyleo Hub), and then use the builtin editor to construct the dashboard.  Dashboards can be published directly from the editor.

### Quickstart
A quickstart mini-tutorial can be found at: [Quickstart](https://github.com/engageLively/galyleo-examples/tree/main/quickstart).  A quickstart to the data service can be found at [Quickstart Data](https://github.com/engageLively/galyleo-examples/tree/main/quickstart-data-service)

### Tutorials
Bundled in the examples repository is a set of tutorials, which walk the user through the steps of creating a dashbaord.  The tutorials are at [Galyleo Tutorials](https://github.com/engageLively/galyleo-examples/tree/main/tutorials).    They are:

1. **create-table**: learn how to create a Galyleo Table from a CSV file or PANDAS frame

2. **publish-table**: Publish a table so it can be used in a dashboard.

3. **filter-table**: learn how to filter the columns of a table by value or range

4. **create-view**: use filters, column selection and ordering to prepare the data for a dynamic chart

5. **create-chart**: create a chart that takes as its inputs a view

6. **use-chart-as-filter**: Every chart is also a filter; use this to do data drill-downs

7. **add-images-text-and-shapes**: Add images, text, and shapes, and style them



### The Data Service
A full introduction to the data service Galyleo uses can be found here: [Global Data Plane](https://global-data-plane.github.io/sdtp/).