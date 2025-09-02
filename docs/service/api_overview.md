## The Galyleo Service API

The Galyleo Service API is an implementation of the Simple  Data Transfer Protocol API, with additional methods to permit the publication and sharing of data and tables.  It is a standard REST API.

### Base URL
All methods are formed from the base URL, which is _jupyter-hub-url_/services/galyleo.  So, for example, if the Hub was at https://galyleo-beta.engagelively.com/, the base URL for the Galyleo service is https://galyleo-beta.engagelively.com/services/galyleo.  And a request to list tables from this url would be:
```
curl https://galyleo-beta.engagelively.com/services/galyleo/get_table_names
```

### Supported API Methods
| Route |	Method |	Parameters	| Description | SDTP Method |
|-------|--------|---------------|-------------|-------------| 
| dashboards/_owner_/_dashboard_	| GET |		None | Return the dashboard owned by _owner_ named _dashboard_ | No |
| table/_owner_/_table_	| GET |		None | Return the table owned by _owner_ named _table_| No | 
| publish_data	| POST | -table, a table in SDML format <br> -name, which _must end in .sdml_. <br> -Optionally, share_list, the list of users with access to the table	| Publish the table to tables/_owner_/_name_ | No |
| publish	| POST |	-dashboard, a dashboard in Galyleo format <br> -name, _which must end in .gd.json_. <br> -Optionally, share_list, the list of users with access to the dashboard | 	Publish the dashboard as dashboards/_owner_/_name_ | No |
| get_table_names	| GET |		None | Get the tables (as a list of URLs) accessible by this user| Yes |
| get_table_schemas	| GET |	None |	Get the schemas of tables accessible by this user|  Yes |
| get_table_schema	| GET |	None | table, the name of the table to get the schema for. |	Get the schema of the table|  Yes |
| get_range_spec	| GET |	-table, the name of the table <br>-column, the name of the column |	Get the max and min of the column, as a list |  Yes |
| get_all_values	| GET |	- table, the name of the table, <br>-column, the name of the column	| Get the distinct values of the column, as a JSON list|  Yes |
| get_column	| GET |	-table, the name of the table <br>- column, the name of the column |	Get the column, as a JSON list|  Yes |
| get_filtered_rows	| POST |	table, the name of the table <br>- Optional: columns, a list of columns to get, <br> - Optional: filter_spec, a filter in SDQL format |	A list of rows which match the filter, or all rows if the filer is not present|  Yes |

### Authentication
Authentication is by Bearer Token; see the Authentication section below.  All methods except `publish_data` and `publish` permit anonymous access, but only tables and dashboards shared with the public will be available to the user

### Successful Returns
Data is _always_ returned as a JSON list of values, for easy parsing.

### Errors
Standard errors (400, 401, 403) are returned with an explanatory error message.