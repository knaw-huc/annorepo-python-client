## usage

### initializing the client

```python
from annorepo.client import AnnoRepoClient

client = AnnoRepoClient("http://localhost:8080/")
```

### verifying the annorepo server is up and can be reached

```python
server_is_up = client.server_is_ok()
```
