## Views

A _View_ is a subset of a table; a selection (and, potentially, a reordering) of the columns of a table, and a subset of its rows, chosen by one or more Filters.  While a chart can take as input a _Table_, such a chart wouldn't respond to user inputs (because a user selects the rows he's interested in by adjusting a Filter, and filters only affect the rows in Views).  
A View is chosen with:
- a source table;
- a fixed subset (and potential reordering) of columns
- a set of filters which select the rows of the table.  The filters are considered to have acted in sequence, and thus the rows preserved are the logical AND of the applied filters.
For example, suppose we wanted to construct a View with columns name, rating from our table, and had a range filter on column calories and a select filter on column mfr.  The View would be:
```
  {
    "table": "cereal",
    "columns": ["name", "rating"],
    "filters": ["mfrFilter", "calorieFilter"]
  }
```
And, if mfrFilter was set to "N" (Nabisco) and calorieFilter to [50, 90], the data in the view would be:


| name     | rating   |
|----------|----------|
| 100% Bran| 68.402973|
