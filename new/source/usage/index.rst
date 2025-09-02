Using Galyleo
=============
This section covers the library and user interface elements for sending Tables from Jupyter Notebooks to Galyleo Dashboards, and using the Galyleo UI to add Filters, Views, Charts, and explanatory elements (Text, Shapes, and Images) to the Dashboard.  The UI for Shapes, Images, and Text was largely covered above, so we'll focus on tables, filters, views, and charts here.

The Galyleo UI
--------------
Key elements of the Galyleo UI can be seen in the Tables section of the sidebar, shown here with annotations.

.. image:: images/tables-edit.png

The tab selectors choose the category of item being viewed.  Here, it is the list of Tables (the Tables tab is highlighted in orange).  To the right of each Table name is an inspection icon. Clicking on this gives a preview of the selected table in a popup window.  *Warning:* this should be done carefully, since viewing large tables can cause performance issues.  Clicking on the "Add Table" button brings up a popup, inviting a load of a Table in intermediate form from an URL. 

The sidebar is closed either by clicking on the orange triangle in the center of the sidebar's left edge, or on the close button on the top right.

Clicking on the pen icon on the top right of the Table list toggles between inspection mode and edit mode.

.. image:: images/edit-mode.png

When in edit mode, clicking on the circle to the  left of a table name deletes the circle.  Clicking on the pen icon again restores inspection mode.

Every element of the Table UI is present for all classes of element, (Tables, Filters, Views, and Charts).  The pen is present in all lists to switch between inspection/configuration mode for all classes, each class has an Add button, and the close-sidebar buttons are always present.

.. toctree::
   :maxdepth: 1

   adding_tables
   adding_filters
   creating_views
   creating_charts
   images_shapes_text
   publishing_dashboards