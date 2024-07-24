import base64
import http
from dataclasses import dataclass
from http import HTTPStatus

import requests
from requests import Response

import annorepo
from annorepo.model import ContainerIdentifier, AnnotationIdentifier


@dataclass
class SearchInfo:
    id: str
    location: str


@dataclass
class ReadAnnotationResult:
    etag: str
    annotation: dict[str, any]


class AnnoRepoClient:
    """
    A class to interact with an annorepo server
    """

    def __init__(self, base_url: str, admin_url: str = None, timeout: int = None, api_key=None, verbose: bool = False):
        """

        :param base_url:
        :param admin_url:
        :param timeout:
        :param api_key:
        :param verbose:
        """
        self.api_key = api_key
        self.base_url = base_url.strip('/')
        self.admin_url = admin_url.strip('/') if admin_url else "http://localhost:8081"
        self.raise_exception = True
        self.timeout = timeout
        self.verbose = verbose
        self.session = requests.Session()

    def __str__(self):
        return f'AnnoRepoClient({self.base_url}, {self.admin_url})'

    def __repr__(self):
        return self.__str__()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        # logger.debug(f"closing session with args: {args}")
        self.session.close()

    def close(self):
        self.__exit__()

    def get_about(self):
        """Read the about info

        :return: The about info as json
        """
        url = f'{self.base_url}/about'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def get_homepage(self):
        """Read the homepage

        :return: The homepage as html
        """
        url = f'{self.base_url}/'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_robots_txt(self):
        """Read the robots.txt

        :return: The contents of the robots.txt file
        """
        url = f'{self.base_url}/robots.txt'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_favicon(self):
        """Read the favicon.ico

        :return:
        """
        url = f'{self.base_url}/favicon.ico'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_swagger_json(self):
        """Read the swagger info (as json)

        :return: The swagger info as json
        """
        url = f'{self.base_url}/swagger.json'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def get_swagger_yaml(self):
        """Read the swagger info (as yaml)

        :return: The swagger info as yaml
        """
        url = f'{self.base_url}/swagger.yaml'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_openapi_json(self):
        """Read the openapi info (as json)

        :return: The openapi info as json
        """
        url = f'{self.base_url}/openapi.json'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def get_openapi_yaml(self):
        """Read the openapi info (as yaml)

        :return: The openapi info as yaml
        """
        url = f'{self.base_url}/openapi.yaml'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_healthcheck(self):
        """Do the healthcheck

        :return: The healthcheck info as json
        """
        url = f'{self.admin_url}/healthcheck'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def has_container(self, name: str) -> bool:
        """Check if a container with the given name exists

        :param name: Name of the container
        :type name: str
        :return: True if a container with the given name exists, False otherwise
        :rtype: bool
        """
        url = f'{self.base_url}/services/{name}/fields'
        response = self._head(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda _: True, HTTPStatus.NOT_FOUND: lambda _: False})

    def create_container(self, name: str = None, label: str = "A Container for Web Annotations") -> ContainerIdentifier:
        """Create a new Annotation Container

        :param name: Optional name for the container (may be overruled)
        :param label: Label for the container (default: "A Container for Web Annotations")
        :return: The ContainerIdentifier
        """
        url = f'{self.base_url}/w3c'
        headers = {}
        if name:
            headers['slug'] = name
        specs = {
            "@context": [
                "http://www.w3.org/ns/anno.jsonld",
                "http://www.w3.org/ns/ldp.jsonld"
            ],
            "type": [
                "BasicContainer",
                "AnnotationCollection"
            ],
            "label": label
        }
        response = self._post(url=url, json=specs, headers=headers)
        # ic(response.headers)
        return self._handle_response(response, {
            HTTPStatus.CREATED: self._as_container_identifier
        })

    def read_container(self, container_name: str) -> ContainerIdentifier:
        """Read information about an existing Annotation Container with the given identifier

        :param container_name: The container name
        :return: Information about the container
        """
        url = f'{self.base_url}/w3c/{container_name}'
        response = self._get(url=url)
        # ic(response)
        return self._handle_response(
            response,
            {
                HTTPStatus.OK: self._as_container_identifier,
                HTTPStatus.NOT_FOUND: lambda r: None
            }
        )

    def delete_container(self, container_name: str, etag: str, force: bool = False):
        """Remove the Annotation Container with the given identifier, provided it is empty

        :param container_name:
        :param etag:
        :param force:
        :return:
        """
        url = f'{self.base_url}/w3c/{container_name}'
        response = self._delete(url=url, etag=etag, params={"force": force})
        return self._handle_response(response, {HTTPStatus.NO_CONTENT: lambda r: True})

    def read_container_metadata(self, container_name: str):
        """Read metadata from the  Annotation Container with the given identifier

        :param container_name: The container name
        :return: A dict containing the metadata
        """
        url = f'{self.base_url}/services/{container_name}/metadata'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def add_annotation(self, container_name: str, content: dict[str, any], name: str = None) -> AnnotationIdentifier:
        """Add an annotation to the given container

        :param container_name: The container name
        :param content: The Web Annotation represented as a dict
        :param name: optional annotation name
        :return: annotation_identifier
        """
        url = f'{self.base_url}/w3c/{container_name}'
        headers = {}
        if name:
            headers['slug'] = name
        response = self._post(url=url, headers=headers, json=content)
        # ic(response.headers)
        return self._handle_response(response, {HTTPStatus.CREATED: self._as_annotation_identifier})

    def add_annotations(self, container_name: str, annotation_list: list[dict[str, any]]):
        """Add annotations to the given container, in bulk

        :param container_name: The container name
        :param annotation_list: a list of Web Annotations, represented as dicts
        :return: list of annotation_identifiers
        """
        url = f'{self.base_url}/services/{container_name}/annotations-batch/'
        headers = {}
        response = self._post(url=url, headers=headers, json=annotation_list)
        return self._handle_response(
            response,
            {
                HTTPStatus.OK: lambda r: r.json(),
                HTTPStatus.INTERNAL_SERVER_ERROR: lambda r: r.json()
            }
        )

    def read_annotation(self, container_name: str, annotation_name: str) -> ReadAnnotationResult:
        """Read information about an existing Annotation Container with the given identifier

        :param container_name: The container name
        :param annotation_name: The annotation name
        :return: Information about the annotation
        """
        url = f'{self.base_url}/w3c/{container_name}/{annotation_name}'
        response = self._get(url=url)
        # ic(response)
        return self._handle_response(response,
                                     {
                                         HTTPStatus.OK: lambda r: ReadAnnotationResult(etag=r.headers['eTag'],
                                                                                       annotation=r.json()),
                                         HTTPStatus.NOT_FOUND: lambda r: None
                                     })

    def update_annotation(self, container_name: str, annotation_name: str, etag: str,
                          content: dict[str, any]) -> ReadAnnotationResult:
        """Update the given annotation

        :param container_name: The container name
        :param annotation_name: The annotation name
        :param etag:
        :param content: The Web Annotation represented as a dict
        :return: the updated annotation
        """
        url = f'{self.base_url}/w3c/{container_name}/{annotation_name}'
        response = self._put(url=url, etag=etag, json=content)
        # ic(response.headers)
        return self._handle_response(
            response,
            {
                HTTPStatus.OK: lambda r: ReadAnnotationResult(etag=r.headers['eTag'], annotation=r.json())
            }
        )

    def delete_annotation(self, container_name: str, annotation_name: str, etag: str):
        """Remove the Annotation with the given name in the container with the given identifier

        :param container_name: the container name
        :param annotation_name: the annotation name
        :param etag: the eTag for this annotation
        :return:
        """
        url = f'{self.base_url}/w3c/{container_name}/{annotation_name}'
        response = self._delete(url=url, etag=etag)
        return self._handle_response(response, {HTTPStatus.NO_CONTENT: lambda r: True})

    def get_ping(self) -> str:
        """Ping the server to see if it's active

        :return:
        """
        url = f'{self.admin_url}/ping'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_users(self):
        """
        :return:
        """
        url = f'{self.base_url}/admin/users'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def add_user(self, user_name: str, api_key: str):
        """
        :param user_name:
        :param api_key:
        :return:
        """
        url = f'{self.base_url}/admin/users'
        user_entry = {"userName": user_name, "apiKey": api_key}
        response = self._post(url=url, json=[user_entry])
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def create_search(self, container_name: str, query: dict[str, any]) -> SearchInfo:
        """

        :param container_name: the container name
        :param query:
        :return:
        """

        def to_search_info(_response: Response) -> SearchInfo:
            location = _response.headers["location"]
            search_id = location.split("/")[-1]
            return SearchInfo(id=search_id, location=location)

        url = f'{self.base_url}/services/{container_name}/search'
        response = self._post(url=url, json=query)
        return self._handle_response(response, {HTTPStatus.CREATED: to_search_info})

    def read_search_result_page(self, container_name: str, search_id: str, page: int = 0):
        """

        :param container_name: the container name
        :param search_id:
        :param page:
        :return:
        """
        url = f'{self.base_url}/services/{container_name}/search/{search_id}'
        params = {"page": page}
        response = self._get(url=url, params=params)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def read_search_info(self, container_name: str, search_id: str):
        """

        :param container_name: the container name
        :param search_id:
        :return:
        """
        url = f'{self.base_url}/services/{container_name}/search/{search_id}/info'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def create_global_search(self, query: dict[str, any]) -> SearchInfo:
        """

        :param query:
        :return:
        """

        def to_search_info(_response: Response) -> SearchInfo:
            location = _response.headers["location"]
            search_id = location.split("/")[-1]
            return SearchInfo(id=search_id, location=location)

        url = f'{self.base_url}/global/search'
        response = self._post(url=url, json=query)
        return self._handle_response(response, {HTTPStatus.CREATED: to_search_info})

    def read_global_search_result_page(self, search_id: str, page: int = 0):
        """

        :param search_id:
        :param page:
        :return:
        """
        url = f'{self.base_url}/global/search/{search_id}'
        params = {"page": page}
        response = self._get(url=url, params=params)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def read_global_search_status(self, search_id: str):
        """

        :param search_id:
        :return:
        """
        url = f'{self.base_url}/global/search/{search_id}/status'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def read_accessible_containers(self) -> dict[str, list[str]]:
        """

        :return:
        """
        url = f'{self.base_url}/my/containers'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def create_index(self, container_name: str, field: str, index_type: str):
        """

        :param container_name:
        :param field:
        :param index_type:
        :return:
        """
        url = f'{self.base_url}/services/{container_name}/indexes/{field}/{index_type}'
        response = self._put(url=url)
        return self._handle_response(response, {HTTPStatus.CREATED: lambda r: r.json()})

    def read_indexes(self, container_name: str):
        """

        :param container_name:
        :return:
        """
        url = f'{self.base_url}/services/{container_name}/indexes'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def read_index_status(self, container_name: str, field: str, index_type: str):
        """

        :param container_name:
        :param field:
        :param index_type:
        :return:
        """
        url = f'{self.base_url}/services/{container_name}/indexes/{field}/{index_type}/status'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def read_distinct_values(self, container_name: str, field: str):
        """

        :param container_name:
        :param field:
        :return:
        """
        url = f'{self.base_url}/services/{container_name}/distinct-values/{field}'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def set_anonymous_user_read_access(self, container_name: str, has_read_access: bool = True):
        """

        :param container_name:
        :param has_read_access:
        :return:
        """
        url = f'{self.base_url}/services/{container_name}/settings/isReadOnlyForAnonymous'
        response = self._put(url=url, json=has_read_access)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: True})

    def create_custom_query(self, name: str, query: dict[str, any], description="", public: bool = True) -> str:
        """

        :param name:
        :param query:
        :param description:
        :param public:
        :return:
        """
        url = f'{self.base_url}/global/custom-query'
        payload = {
            "name": name,
            "query": query,
            "description": description,
            "public": public
        }
        response = self._post(url=url, json=payload)
        return self._handle_response(response, {HTTPStatus.CREATED: lambda r: r.headers["location"]})

    def read_custom_queries(self) -> dict[str, any]:
        """

        :return:
        """
        url = f'{self.base_url}/global/custom-query'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def delete_custom_query(self, query_name: str) -> bool:
        """

        :param query_name:
        :return:
        """
        url = f'{self.base_url}/global/custom-query/{query_name}'
        response = self._delete(url=url)
        return self._handle_response(response, {HTTPStatus.NO_CONTENT: True})

    def read_expanded_custom_query(self, name: str, parameters: dict[str, str]) -> dict[str, any]:
        """

        :param name:
        :param parameters:
        :return:
        :rtype: dict[str, any]
        """
        query_call = self._query_call(name, parameters)
        url = f'{self.base_url}/global/custom-query/{query_call}/expand'
        response = self._get(url=url)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def read_custom_query_result_page(self, container_name: str, query_name: str, parameters: dict[str, str] = {},
                                      page: int = 0):
        """

        :param container_name:
        :param query_name:
        :param parameters:
        :param page:
        :return:
        """
        query_call = self._query_call(query_name, parameters)
        url = f'{self.base_url}/services/{container_name}/custom-query/{query_call}'
        params = {"page": page}
        response = self._get(url=url, params=params)
        return self._handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def container_adapter(self, container_name: str) -> 'ContainerAdapter':
        """

        :param container_name:
        :return:
        :rtype: ContainerAdapter
        """
        return ContainerAdapter(self, container_name)

    def _query_call(self, name: str, parameters: dict[str, str]):
        return f"{name}:{self._encoded_parameters(parameters)}"

    @staticmethod
    def _encoded_parameters(parameters: dict[str, str]) -> str:
        return ",".join([f"{k}={base64.b64encode(str.encode(v)).decode()}" for k, v in parameters.items()])

    def _get(self, url, params=None, **kwargs):
        args = self._set_defaults(kwargs)
        return self.session.get(url, params=params, **args)

    def _head(self, url, params=None, **kwargs):
        args = self._set_defaults(kwargs)
        return self.session.head(url, params=params, **args)

    def _post(self, url, data=None, json=None, **kwargs):
        args = self._set_defaults(kwargs)
        return self.session.post(url, data=data, json=json, **args)

    def _put(self, url, data=None, **kwargs):
        args = self._set_defaults(kwargs)
        return self.session.put(url, data=data, **args)

    def _delete(self, url, **kwargs):
        args = self._set_defaults(kwargs)
        return self.session.delete(url, **args)

    def _set_defaults(self, args: dict):
        # ic(args)
        if 'headers' not in args:
            args['headers'] = {}
        args['headers']['User-Agent'] = f'annorepo-python-client/{annorepo.__version__}'
        if self.api_key:
            args['headers']['Authorization'] = f'Bearer {self.api_key}'
        if self.timeout:
            args['timeout'] = self.timeout
        if 'etag' in args:
            args['headers']["If-Match"] = args.pop('etag')
        return args

    @staticmethod
    def _as_container_identifier(_response: Response) -> ContainerIdentifier:
        return ContainerIdentifier(url=_response.headers["location"], etag=_response.headers["etag"])

    @staticmethod
    def _as_annotation_identifier(_response: Response) -> AnnotationIdentifier:
        return AnnotationIdentifier(url=_response.headers["location"], etag=_response.headers["etag"])

    def _handle_response(self, response: Response, result_producers: dict):
        status_code = response.status_code
        status_message = http.client.responses[status_code]
        # ic(response.request.headers)
        if self.verbose:
            print(f'-> {response.request.method} {response.request.url}')
            print(f'<- {status_code} {status_message}')
        if status_code in result_producers:
            # if (self.raise_exceptions):
            return result_producers[response.status_code](response)
            # else:
            #     return Success(response, result)
        else:
            # if (self.raise_exceptions):
            raise Exception(
                f'{response.request.method} {response.request.url} returned {status_code} {status_message}'
                + f': "{response.text}"')


class ContainerAdapter:
    """
    A class to interact with a given annotation container on an annorepo server
    """

    def __init__(self, ar_client: AnnoRepoClient, container_name: str):
        """

        :param ar_client:
        :type ar_client: AnnoRepoClient
        :param container_name:
        :type container_name: str
        """
        self.client = ar_client
        self.container_name = container_name

    def exists(self) -> bool:
        """

        :return:
        :rtype: bool
        """
        return self.client.has_container(name=self.container_name)

    def create(self, label: str = "") -> ContainerIdentifier:
        """
        :param label:
        :type label: str
        :return:
        """
        if self.exists():
            return self.read()
        return self.client.create_container(name=self.container_name, label=label)

    def read(self) -> ContainerIdentifier:
        """

        :return:
        """
        return self.client.read_container(container_name=self.container_name)

    def delete(self, etag: str, force: bool = False):
        """

        :param etag:
        :param force:
        :return:
        """
        return self.client.delete_container(container_name=self.container_name, etag=etag, force=force)

    def read_metadata(self):
        """

        :return:
        """
        return self.client.read_container_metadata(container_name=self.container_name)

    def add_annotation(self, content: dict[str, any], name: str):
        """

        :param content:
        :param name:
        :return:
        """
        return self.client.add_annotation(container_name=self.container_name, content=content, name=name)

    def add_annotations(self, annotation_list: list[dict[str, any]]):
        """

        :param annotation_list:
        :return:
        """
        return self.client.add_annotations(container_name=self.container_name, annotation_list=annotation_list)

    def read_annotation(self, annotation_name: str):
        """

        :param annotation_name:
        :return:
        """
        return self.client.read_annotation(container_name=self.container_name, annotation_name=annotation_name)

    def update_annotation(self, annotation_name: str, etag: str, content: dict[str, any]):
        """

        :param annotation_name:
        :param etag:
        :param content:
        :return:
        """
        return self.client.update_annotation(container_name=self.container_name, annotation_name=annotation_name,
                                             etag=etag, content=content)

    def delete_annotation(self, annotation_name: str):
        """

        :param annotation_name:
        :return:
        """
        return self.client.delete_annotation(container_name=self.container_name, annotation_name=annotation_name)

    def create_search(self, query: dict[str, any]) -> SearchInfo:
        """

        :param query:
        :return:
        """
        return self.client.create_search(container_name=self.container_name, query=query)

    def read_search_result_page(self, search_id: str, page: int = 0):
        """

        :param search_id:
        :param page:
        :return:
        """
        return self.client.read_search_result_page(container_name=self.container_name, search_id=search_id, page=page)

    def read_search_info(self, search_id: str):
        """

        :param search_id:
        :return:
        """
        return self.client.read_search_info(container_name=self.container_name, search_id=search_id)

    def create_index(self, field: str, index_type: str):
        """

        :param field:
        :param index_type:
        :return:
        """
        return self.client.create_index(container_name=self.container_name, field=field, index_type=index_type)

    def read_indexes(self):
        """

        :return:
        """
        return self.client.read_indexes(container_name=self.container_name)

    def read_index_status(self, field: str, index_type: str):
        """

        :param field:
        :param index_type:
        :return:
        """
        return self.client.read_index_status(container_name=self.container_name, field=field, index_type=index_type)

    def read_distinct_values(self, field: str):
        """

        :param field:
        :return:
        """
        return self.client.read_distinct_values(container_name=self.container_name, field=field)

    def set_anonymous_user_read_access(self, has_read_access: bool = True):
        """

        :param has_read_access:
        :return:
        """
        return self.client.set_anonymous_user_read_access(container_name=self.container_name,
                                                          has_read_access=has_read_access)

    def read_custom_query_result_page(self, query_name: str, parameters: dict[str, str] = {},
                                      page: int = 0):
        """

        :param query_name:
        :param parameters:
        :param page:
        :return:
        """
        return self.client.read_custom_query_result_page(container_name=self.container_name, query_name=query_name,
                                                         parameters=parameters, page=page)
