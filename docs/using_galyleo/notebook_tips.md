# Working in the Notebook
Most Galyleo work starts in a Jupyter notebook, where you prepare the data that a dashboard will use.  This page describes JupyterLab features that make that work easier.  They are standard JupyterLab features, not Galyleo features, so the full JupyterLab documentation applies to them as well.

## Contextual Help
Contextual Help shows the documentation for whatever is under your cursor in a notebook cell, so you can check what a function does, or what arguments it takes, without leaving the notebook.

### Turning it on
Choose **Help > Show Contextual Help**.  A Contextual Help panel opens beside the notebook.  At first it reads "No Documentation"; that is normal, and it changes as soon as you put the cursor on something it can look up.

### Using it
Run a cell, then click on, or move the cursor onto, a function, module or variable in that cell.  The panel shows its documentation: its type, its signature, and its description.  For example, after running

```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2]})
df.head()
```

the panel shows documentation when the cursor is on `pd.DataFrame`, on `df`, or on `df.head`.

### If the panel says "No Documentation"
Contextual Help does not read your code itself.  It asks the kernel that is running your notebook, so it can only describe things the kernel knows about.  The usual reasons it comes up empty are:

* **The cell has not been run.**  Names that a cell defines or imports do not exist for the kernel until the cell runs.  Run the cell, then move the cursor again.
* **The cursor is on a Python keyword**, such as `import`, `for` or `if`.  Keywords have no documentation to show.  Move the cursor onto a name instead, such as `df.head` in the example above.
* **The name comes after a function call.**  Dotted names such as `df.head` work, but a name reached through a call, such as the `split` in `text.strip().split()`, cannot be looked up.  Put the cursor on `strip` instead, or assign the result of the call to a variable first (`s = text.strip()`) and put the cursor on `s.split`.
* **The kernel is not running.**  Check the kernel name and status indicator at the top right of the notebook.  If the kernel has stopped, choose **Kernel > Restart Kernel**, then run the cell again.
