The Galyleo Python Client
=========================

The Galyleo Python client is a module designed to convert Python structures into Galyleo Tables, and send them to dashboards for use with the Galyleo editor.  It consists of four components:

- galyleo.galyleo_table: classes and methods to create GalyleoTables, convert Python data structures into them, and produce and read JSON versions of the tables.
- galyleo.galyleo_jupyterlab_client: classes and methods to send Galyleo Tables to Galyleo dashboards runniung under JupyterLab clients
- galyleo.galyleo_constants: Symbolic constants used by these packages and the code which uses them
- galyleo.galyleo_exceptions; Exceptions thrown by the package

Test 2
  
Installation
------------

The galyleo module can be installed using ``pip``:
::

  pip install --extra-index-url https://pypi.engagelively.com galyleo  

When the module is more thoroughly tested, it will be put on the standard pypi servers.

License
-------

``galyleo`` is released under a standard BSD 3-Clause licence by engageLively

Galyleo Table
--------------

.. automodule:: galyleo.galyleo_table
   :members:


JupyterLab Client
-----------------

*class* **GalyleoClient**                                                      

The Dashboard Client.  This is the client which sends the tables to the  dashboard and handles requests coming from the dashboard for tables.     

method **GalyleoClient.__init__()**

Initialize the client.  No parameters.  This initializes communications with the JupyterLab Galyleo Communications Manager 

**GalyleoClient.send_data_to_dashboard(galyleo_table, dashboard_name:str = None)**

The routine to send a GalyleoTable to the dashboard, optionally specifying a specific 
dashboard to send the data to.  If None is specified, sends to all the dashboards.
The table must not have more than galyleo_constants.MAX_NUMBER_ROWS, nor be (in JSON form) > galyleo_constants.MAX_DATA_SIZE. 

If either of these conditions apply, a DataSizeExceeded exception is thrown.
NOTE: this sends data to one or more open dashboard editors in JupyterLab.  If there are no dashboard editors open, it will have no effect.

*Args:*
- galyleo_table: the table to send to the dashboard
- dashboard_name: name of the dashboard editor to send it to (if None, sent to all)
  
*Returns:*
- None

*Raises:*
- galyleo_exceptions.DataSizeExceeded

Galyleo Exceptions
------------------

.. automodule:: galyleo.galyleo_exceptions
   :members:

Galyleo Constants
------------------

.. automodule:: galyleo.galyleo_constants
   :members:


