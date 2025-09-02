## Authentication

The Galyleo Service uses the Galyleo Hub as an OAuth2 identity provider, so the Hub's login  also logs the user into the Galyleo service.  

### Authentication to the Web UI
The same cookie is used for the Service as the Hub, and so logging into the Hub automatically logs the user into the Galyleo Service.  Logging out of the Hub logs the user out of the Galyleo Service as well.

### Authentication to the API
Like the Web UI, the API has the same user set and uses the same credentials as the Hub.  All JupyterHubs issue an API key to each user, which serves to identify the user in REST calls.  The Galyleo service uses the same token.  In a Jupyter server, this is available in the environment variable `JUPYTERHUB_API_TOKEN`, and this is the variable used by Galyleo as well. Therefore, the `get_tables` API call on the Hub `https://galyleo-beta.engagelively.com` would be:
```
import requests
import os
headers = {"Authorization": f'token {os.environ[JUPYTERHUB_API_TOKEN]}'}
url = 'https://galyleo-beta.engagelively.com/services/galyleo/get_tables'
response = requests.get(url, headers=headers)
if response.status_code < 400:
  tables = response.json
```
