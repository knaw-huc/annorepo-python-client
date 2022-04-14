Usage
====

initializing the client
----

Initialize the client with the base URL of the annorepo server to connect to.

.. code-block:: python

    from annorepo.client import AnnoRepoClient

    client = AnnoRepoClient("http://localhost:8080/")

optional extra parameters are:

- `timeout` (int): to set a custom timeout (in seconds) for all requests
- `api_key` (str): the api key to use as authentication for all requests
- `verbose` (bool / default: False): return extra information when a request fails

getting some basic information about the server
----

.. code-block:: python

    about = client.get_about()

swagger info
====

getting the swagger info as json
----

.. code-block:: python

    swagger_json = client.get_swagger_json()

getting the swagger info as yaml
----

.. code-block:: python

    swagger_yaml = client.get_swagger_yaml()

W3C Web Application Protocol
====

Annotation Containers
----

Creating an annotation container with a generated name
****

.. code-block:: python

    container_identifier = client.create_container()

Creating an annotation container with a custom name
****

.. code-block:: python

    container_identifier = client.create_container("custom_name")

Reading some information about an annotation container with the given name
****

.. code-block:: python

    container_info = client.get_container("custom_name")

Removing an annotation container with the given name, will fail when the container still contains annotations
****

.. code-block:: python

    client.delete_container("custom_name")
