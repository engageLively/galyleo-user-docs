## Filters

A Filter is a user-interface element that selects rows from tables, based on values from an individual, named column.  A *Select* Filter chooses rows whose value in the named column is equal to the filter's value.  For example, a Select Filter over the type column in our example whose value is "H" would select rows:


| name                  | mfr  | type | calories | fiber | rating    |
|-----------------------|------|------|----------|-------|-----------|
| Cream of Wheat (Quick)| N    | H    | 100      | 1     | 64.533816 |
| Maypo                 | A    | H    | 100      | 0     | 54.850917 |


A *Range* filter chooses rows whose value lies between the two values of the filter.  For example, a Range Filter over the calories column whose minimum is 50 and whose maximum is 70 would select the  rows:


| name                     | mfr | type | calories | fiber | rating    |
|--------------------------|-----|------|----------|-------|-----------|
| 100% Bran                | N   | C    | 70       | 10    | 68.402973 |
| All-Bran                 | K   | C    | 70       | 9     | 59.425505 |
| All-Bran with Extra Fiber| K   | C    | 50       | 14    | 93.704912 |


*Range* and *Select* specify the functional properties of filters (whether the filter selects a specific value or all values in a range).  The physical properties of a filter are dependent  on the functional properties of the filter, the data type of the column, and user experience factors.   At this writing, the *current* set of supported filters are:


| Filter        | Filter Type | Column Type |
|---------------|-------------|-------------|
| List          | Select      | any         |
| Dropdown      | Select      | any         |
| Slider        | Select      | Number      |
| Min/Max       | Range       | any         |
| Double Slider | Range       | Number      |
| Toggle        | Select      | Boolean     |
