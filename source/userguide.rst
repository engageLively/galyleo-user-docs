**************
USER GUIDE

Launching A Dashboard
=====================
A new Galyleo Dashboard can be launched from the JupyterLab launcher or from the File>New menu:
.. image:: images/new_dashboard_.png
An existing dashboard is saved as a .gd.json file, and is denoted with the Galyleo star logo:
.. image:: images/open.png
It can be opened in the usual way, with a double-click.

The Galyleo User Interface
==========================
The Galyleo User interface consists of three components: the top bar, the side bar, and the Halo and Context Menu.  We discuss each of these in turn.  The mission of the Top Bar is to switch between global modes (interacting and selecting) and added non-chart elements (shapes, images, and text) to the dashboard.  The Halo and Side Bar is where individual objects are positioned and configured: where shape and text properties are set, borders defined, and images chosen.  The  Halo   permits the copying, deletion, resizing, and rotation rotation,  of objects front-to-back.  The Context Menu, brought up by a right-click on the object, permits its reordering.

The Top Bar
-----------
The top bar controls are in the top left of the dashboard.  They are primarily used to choose between selection mode (when the user is designing the dashboard) and interaction mode (when the user is interacting with the dashboard, e.g, manipulating a slider).  The practical difference is that when the user is in interaction mode (the arrow is highlighted) a Halo appears over the clicked item and the sidebar is shown; when in interaction mode (the hand is selected) the object is manipulated on click.
When Text (the A) is selected, a user click brings up a text box.  When a shape is selected (one of Rectangle, Ellipse, Image, or Label) the appropriate shape is drawn in response to a user click.
The last item on the top bar is a lifesaver icon, which brings up a bug-report dialog.
.. image:: images/topbar.png
The Halo and the Side Bar
-------------------------
The Halo and the Side Bar are used to configure an object when it's created, and can also be used to configure physical properties of charts and filters.  The Halo automatically appears when an object is clicked on and Selection mode is enabled (the arrow icon in the top bar.  The side bar automatically appears when a shape or text is created, or when the knob in the middle of the sidebar is clicked.  
..image:: images/halo_sidebar.png
The Halo shows control points and tools around the selected object.  The eight control points in the inner halo are used to change the width and height of the object.  The tool in the bottom-left corner is used to rotate the object.  The cross on the top bar is used to move it.  The trash can on the bottom left is used to delete the object.
The Side bar consists of two parts.  The top one, which we'll return to later, manages Tables, Filters, Views, and Charts.  The bottom part is used to configure objects.  It has three sections, each activated by clicking on the chevron next to the name.

The *Shape* configurer is shown in the image, with its eight components shown.  They are used to configure the fill (color) and opacity of the object, as well as whether the object casts a drop shadow. 

..image:: images/color_choose.png
The Color Chooser offers two modes to choose the color of an object.  The first, found by clicking the left-hand rectangle, brings up a palette of colors to choose from.
..image:: images/color_wheel.png
The second permits a fine-grained choice.  The Hue bar is used to set the area of the rainbow to pick a color from; dragging the dot in the left-hand square gives the user the ability to choose a specific color.  The slider at the bottom controls opacity/transparency of the color (as opposed  to the object itself).  Finally, the text box gives the user the ability to specify an RGB color, entered as six hex digits.
The "Clipmode" gives the user the ability to control what happens when the object is too big for its bounding box.  The choices are "visible" (overflows), "hidden" (cut off), "scroll" (scrollbars appear at the right and/or bottom of the object, and "auto" -- the system chooses.
The position is the x,y coordinate of the top-left corner of the object, where (0,0) is the top-left corner of the dashboard; x increases left-to-right, and y top-to-bottom.
..image:: images/image_url.png
When an image is selected, a dialog appears at the bottom of the Shape configurer, permitting the user to choose the URL for the image.  
..image:: images/borders.png
The *Borders* configurer, below  the shape configurer, offers the user the ability to control the color, width, and radius of corners, and the type of line that forms the borders (solid, dotted, or dashed).
..image:: images/text_sidebar.png
The *Text* controller only appears when a Text item is selected, and it is used to control the textual properties of a text object.  These are:
- The font family and weigt (fine to extra-bold)
- The font style (bold, italic, underline, hyperlink)
- The font size and color
- Alignment
- Whether and how lines are wrapped (by words, anywhere, only by words (cannot break a word, or by characters)
- Whether the text box size is set by the user or grows and shrinks with the storing
- The padding control gives the spacing between the text boundary and the boundary of the object, in pixels

There are also two buttons, next to the color chooser, which permit a user to copy style (the standard copy icon), or paste a copied style (the paste brush).



The Context Menu 
-----------------------------
..image:: images/context_menu.png
The context menu appears when the object is right-clicked and selection mode is enabled.  It controls the ordering of objects, front-to-back.

Galyleo Data Architecture
=========================
Tables
------
Filters
-------
Views
-----
Charts
------

Using Galyleo
=============
Sending Tables to the Dashboard
--------------------------------
Adding a Filter
---------------
Creating a View
---------------
Drawing a Chart
---------------
Adding Text, Images, and Shapes
--------------------------------

