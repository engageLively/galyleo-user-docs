The Galyleo Interchange Format
==============================
The Galyleo Interchange Format is the wire protocol between the galyleo module and a  dashboard and the disk format of a Galyleo Dashboard file.  The extension of the file is .gd.json
Overall Structure
-----------------
The Galyleo Interchange Format is simply the JSONified form of the data structure underlying a Galyleo Dashboard.  Its overall structure is:
::

  {
     "tables": <dictionary of tables>,
     "filters" <dictionary of filters>,
     "views": <dictionary of views>,
     "charts": <dictionary of charts>,
     "morphs": <klist of morphs>
  }

where each dictionary is of the form {<objectNMame>: <structure>}.

Morphic Properties
------------------
All physical objects (filters, charts, text, shapes, and images) have a field ``"morphIndex"`` and a  substructure ``"morphicProperties"``.  The morphIndex gives the z-order of the morph; 0 is the rearmost morph, n the frontmost. The morphicProperties structure  describes its physical properties.  The fields of the ``"morphicProperties"`` structure are:

+==========+==================+==================================================================+=============+=============================+
| Field    | Structure        | Purpose                                                          | Example     | Note                        |
+==========+==================+==================================================================+=============+=============================+
| fill     | Color string     | Fill color                                                       | '#FF0000'   | Red = 255, Blue = Green = 0 |
+----------+------------------+------------------------------------------------------------------+-------------+-----------------------------+
| position | Coordinate       | position of the top-left corner of the object                    | pt(128, 73) | x = 128, y = 73             |
+----------+------------------+------------------------------------------------------------------+-------------+-----------------------------+
| extent   | Coordinate       | width and height of the object's bounding box                    | pt(10, 5)   | width = 10, height = 5      |
+----------+------------------+------------------------------------------------------------------+-------------+-----------------------------+
| rotation | real             | Rotation of the object in radians, measured clockwise            | 1.57        | rotated 90° clockwise       |
+----------+------------------+------------------------------------------------------------------+-------------+-----------------------------+
| border   | Border structure | Substructure with border properties.  See below for details and example                                      |
+----------+------------------+------------------------------------------------------------------+-------------+-----------------------------+
| opacity  | real             | Opacity vs transparency of the object, 1 = opaque, 0 = invisible | 0.5         | semi-transparent            | 
+----------+------------------+------------------------------------------------------------------+-------------+-----------------------------+
| Clipmode | Clip enum        | Appearance when the object is too big for its bounding box       | scroll      | scroll bars appear          |
+==========+==================+==================================================================+=============+=============================+

A Color string is a 7-digit string of the form '#RRGGBB', where each R, G, and B are a character in the range 0-9, a-f, to be read as three integers in the range 0-255.  The first integer specfies the saturation of red, the second green, the third blue.
A Coordinate is a structure of the form 'pt(x, y)', where x and y are reals.

The Clip enum is one of visible, scroll, or auto.  Visible is overflow the bounds, hidden is do not show the overflow, scroll is show scrollbars


A border structure is a dictionary with four entries: "top", "bottom", "right", "left".  These specify the properties of the border along each side of the object.  Each field is a structure of the form:
+========+==============+==================================================================+============+=============================================+
| Field  | Structure    | Purpose                                                          | Example   | Note                                         |
+========+==============+==================================================================+============+=============================================+
| Width  | Real         | Width of the border in pixels                                    | 2         | Must be > 0                                  | 
+--------+--------------+------------------------------------------------------------------+-----------+----------------------------------------------+
| Radius | Real         | radius of the arc at the corner, as a percentage of border length| 10        | 0 = square corners, 100 = completely rounded |
+--------+--------------+------------------------------------------------------------------+-----------+----------------------------------------------+
| Type   | BorderType   | style of the border line                                         | dotted    | the border is composed of dots               |
+--------+--------------+------------------------------------------------------------------+-----------+----------------------------------------------+
| Color  | Color string | color of the border line                                         | "#00ff00" | a green border                               |
+========+==============+==================================================================+============+=============================================+

A BorderType is an enum (as a string).  It is one of: none, hidden, solid, dotted, dashed, ridged, double, groove, or inset
         
Tables
------

A table is a dictionary with two entries, columns and rows.  A column is a list of entries of the form ``{"name": <columnName>, "type": <columnType>}`` where column type must be one of 
'string', 'number', 'boolean', 'date', 'datetime', 'timeofday'.

The rows field is a list of lists, where each list represents a row of the table.  Each component list *must*:

- Be of the same length as the list of columns
- Be type-compliant with the list of columns.  The ith entry in the list must be of the type specified in the ith entry of the column list


Filters
-------
A Filter is a structure of the form: ``{"savedFilter": <filterSpecification>, "morphicIndex": <index>, "morphicProperties": <properties>}``.  See the discussion above for morphicIndex and morphicProperties.


Views
-----
Charts
------
Morphs
------