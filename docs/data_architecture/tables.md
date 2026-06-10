## Tables

An SDML Table is equivalent to  a SQL database table.  It consists of a list of columns, each with a type, and (conceptually) a list of rows.  These rows are returned as the result of an API call; they may or may not be physically stored in the SDML Table.  For further information, see the Global Data Plane website at https://global-data-plane.github.io/.

A *schema* is a list of records of the form `{"name": <name>, "type": <type>}`, where `<name>` is the column name and `<type>` is the column type, which is chosen from the set `{"number", "string", "boolean", "date", "datetime", "timeofday"}`.  

Tables are loaded through Simple Data Transfer Protocol API calls.  A Simple Data Transfer Protocol server is loaded with every Galyleo Hub.

Here's a simple example of a table:

name | mfr | type | calories | fiber | rating |
-----|-----|-----|-----|-----|-----|
100% Bran | N | C | 70 | 10 | 68.402973 |
100% Natural Bran | Q | C | 120 | 2 | 33.983679 |
All-Bran | K | C | 70 | 9 | 59.425505 |
All-Bran with Extra Fiber | K | C | 50 | 14 | 93.704912 |
Almond Delight | R | C | 110 | 1 | 34.384843 |
Apple Cinnamon Cheerios | G | C | 110 | 1.5 | 29.509541 |
Apple Jacks | K | C | 110 | 1 | 33.174094 |
Basic 4 | G | C | 130 | 2 | 37.038562 |
Bran Chex | R | C | 90 | 4 | 49.120253 |
Bran Flakes | P | C | 90 | 5 | 53.313813 |
Cap'n'Crunch | Q | C | 120 | 0 | 18.042851 |
Cheerios | G | C | 110 | 2 | 50.764999 |
Cream of Wheat (Quick) | N | H | 100 | 1 | 64.533816 |
Maypo | A | H | 100 | 0 | 54.850917 |

This is a formatted version of the table.  The schema is:
```
   [
       {"name": "name", "type": "string"},
       {"name": "mfr", "type": "string"},
       {"name": "type", "type": "string"},
       {"name": "calories", "type": "number"},
       {"name": "fiber", "type": "number"},
       {"name": "rating", "type": "number"}
   ]
```
And the first data row is:
```
   ["100% Bran","N","C",70,10,68.402973]
```
Tables available to the user can be found by Clicking the Galyleo Service item on the menu bar, which will bring up the Galyleo Service in a new JupyterLab tab.  The tables available to the user are also always displayed in the Tables tab in the side bar.