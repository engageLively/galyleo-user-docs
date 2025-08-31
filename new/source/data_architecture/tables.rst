Tables
------
An SDML Table is equivalent to  a SQL database table -- a list of columns, each with a type, and (conceptually) a list of rows.  These rows are returned as the result of an API call; they may or may not be physically stored in the SDML Table.  For further information, see the Global Data Plane website at https://global-data-plane.github.io/.

A *schema* is a list of records of the form ``{"name": <name>, "type": <type>}``, where <name> is the column name and type is the column type, which is chosen from the set ``{"number", "string", "boolean", "date", "datetime", "timeofday"}``.  These are captured in the ``galyleoconstants`` library ``SDML_STRING, SDML_NUMBER, SDML_BOOLEAN, SDML_DATE, SDML_DATETIME, SDML_TIME_OF_DAY``.

Tables are loaded through Simple Data Transfer Protocol API calls.  A Simple Data Transfer Protocol server is loaded with every Galyleo Hub.

Here's a simple example of a table, which we'll use throughout this tutorial:

.. csv-table:: Cereal Example
   :file: cereal.csv
   :header-rows: 1

This is a formatted version of the table.  The schema is:
::

   [
       {"name": "name", "type": SDML_STRING},
       {"name": "mfr", "type": SDML_STRING},
       {"name": "type", "type": SDML_STRING},
       {"name": "calories", "type": SDML_NUMBER},
       {"name": "fiber", "type": SDML_NUMBER},
       {"name": "rating", "type": SDML_NUMBER}
   ]

And the first data row is:
::

   ["100% Bran","N","C",70,10,68.402973]