The Halo and the Side Bar
-------------------------
The Halo and the Side Bar are used to configure an object when it's created, and can also be used to configure physical properties of charts and filters.  The Halo automatically appears when an object is clicked on and Selection mode is enabled (the arrow icon in the top bar.  The side bar automatically appears when a shape or text is created, or when the knob in the middle of the sidebar is clicked.  

.. image:: images/halo_sidebar.png

The Halo shows control points and tools around the selected object.  The eight control points in the inner halo are used to change the width and height of the object.  The tool in the bottom-left corner is used to rotate the object.  The cross on the top bar is used to move it.  The trash can on the bottom left is used to delete the object.

The Side bar consists of two parts.  The top one, which we'll return to later, manages Tables, Filters, Views, and Charts.  The bottom part is used to configure objects.  It has three sections, each activated by clicking on the chevron next to the name.

The *Shape* configurer is shown in the image, with its eight components shown.  They are used to configure the fill (color) and opacity of the object, as well as whether the object casts a drop shadow. 

.. image:: images/color_chooser.png

The Color Chooser offers two modes to choose the color of an object.  The first, found by clicking the left-hand rectangle, brings up a palette of colors to choose from.

.. image:: images/color_wheel.png

The second permits a fine-grained choice.  The Hue bar is used to set the area of the rainbow to pick a color from; dragging the dot in the left-hand square gives the user the ability to choose a specific color.  The slider at the bottom controls opacity/transparency of the color (as opposed  to the object itself).  Finally, the text box gives the user the ability to specify an RGB color, entered as six hex digits.

The "Clipmode" menu gives the user the ability to control what happens when the object is too big for its bounding box.  The choices are "visible" (overflows), "hidden" (cut off), "scroll" (scrollbars appear at the right and/or bottom of the object, and "auto" -- the system chooses.

The position is the x,y coordinate of the top-left corner of the object, where (0,0) is the top-left corner of the dashboard; x increases left-to-right, and y top-to-bottom.

.. image:: images/image_url.png

When an image is selected, a dialog appears at the bottom of the Shape configurer, permitting the user to choose the URL for the image.  

.. image:: images/borders.png

The *Borders* configurer, below  the shape configurer, offers the user the ability to control the color, width, and radius of corners, and the type of line that forms the borders (solid, dotted, dashed, ridged, double, groove, or inset). Hidden and none, two other border options, are equivalent to no border.

.. image:: images/text_sidebar.png

The *Text* controller only appears when a Text item is selected, and it is used to control the textual properties of a text object.  These are:

- The font family and weight (fine to extra-bold)
- The font style (bold, italic, underline, hyperlink)
- The font size and color
- Alignment
- Whether and how lines are wrapped (by words, anywhere, only by words (cannot break a word, or by characters)
- Whether the text box size is set by the user or grows and shrinks with the storing
- The padding control gives the spacing between the text boundary and the boundary of the object, in pixels

There are also three buttons, next to the color chooser, which permit a user to copy style (the standard copy icon), paste a copied style (the paste brush), or clear all formatting (the x).
