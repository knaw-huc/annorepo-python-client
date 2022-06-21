import http
from http import HTTPStatus
from typing import Dict, Any

import requests
from requests import Response

import annorepo


class AnnoRepoClient:
    def __init__(self, base_url: str, admin_url: str = None, timeout: int = None, api_key=None, verbose: bool = False):
        self.api_key = api_key
        self.base_url = base_url.strip('/')
        self.admin_url = admin_url.strip('/') if admin_url else "http://localhost:8081"
        self.raise_exception = True
        self.timeout = timeout
        self.verbose = verbose

    def __str__(self):
        return f'AnnoRepoClient({self.base_url}, {self.admin_url})'

    def __repr__(self):
        return self.__str__()

    def get_about(self):
        """Read the about info

        :return: The about info as json
        """
        url = f'{self.base_url}/about'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def get_homepage(self):
        """Read the homepage

        :return: The homepage as html
        """
        url = f'{self.base_url}/'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_robots_txt(self):
        """Read the robots.txt

        :return: The contents of the robots.txt file
        """
        url = f'{self.base_url}/robots.txt'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_favicon(self):
        """Read the favicon.ico

        :return:
        """
        url = f'{self.base_url}/favicon.ico'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_swagger_json(self):
        """Read the swagger info (as json)

        :return: The swagger info as json
        """
        url = f'{self.base_url}/swagger.json'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def get_swagger_yaml(self):
        """Read the swagger info (as yaml)

        :return: The swagger info as yaml
        """
        url = f'{self.base_url}/swagger.yaml'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_openapi_json(self):
        """Read the openapi info (as json)

        :return: The openapi info as json
        """
        url = f'{self.base_url}/openapi.json'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def get_openapi_yaml(self):
        """Read the openapi info (as yaml)

        :return: The openapi info as yaml
        """
        url = f'{self.base_url}/openapi.yaml'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_healthcheck(self):
        """Do the healthcheck

        :return: The healthcheck info as json
        """
        url = f'{self.admin_url}/healthcheck'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def create_container(self, name: str = None):
        """Create a new Annotation Container

        :param name: Optional name for the container (may be overruled)
        :return: The Container
        """
        url = f'{self.base_url}/w3c'
        headers = {}
        if name:
            headers['slug'] = name
        response = self.__post(url=url, headers=headers)
        # ic(response.headers)
        return self.__handle_response(response, {HTTPStatus.CREATED: lambda r: r.json()})

    def read_container(self, container_name: str):
        """Read information about an existing Annotation Container with the given identifier

        :param container_name: The container name
        :return: Information about the container
        """
        url = f'{self.base_url}/w3c/{container_name}'
        response = self.__get(url=url)
        # ic(response)
        return self.__handle_response(response,
                                      {
                                          HTTPStatus.OK: lambda r: r.json(),
                                          HTTPStatus.NOT_FOUND: lambda r: None
                                      })

    def delete_container(self, container_name: str):
        """Remove the Annotation Container with the given identifier, provided it is empty

        :param container_name:
        :return:
        """
        url = f'{self.base_url}/w3c/{container_name}'
        response = self.__delete(url=url)
        return self.__handle_response(response, {HTTPStatus.NO_CONTENT: lambda r: True})

    def add_annotation(self, container_name: str, content: Dict[str, Any], name: str = None):
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
        response = self.__post(url=url, headers=headers, json=content)
        # ic(response.headers)
        return self.__handle_response(response, {HTTPStatus.CREATED: lambda r: r.json()})

    def add_annotations(self, container_name: str, annotation_list: list):
        """Add annotations to the given container, in bulk

        :param container_name: The container name
        :param annotation_list: a list of Web Annotations, represented as dicts
        :return: list of annotation_identifiers
        """
        url = f'{self.base_url}/batch/{container_name}/annotations/'
        headers = {}
        response = self.__post(url=url, headers=headers, json=annotation_list)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.json(),
                                                 HTTPStatus.INTERNAL_SERVER_ERROR: lambda r: r.json()})

    def read_annotation(self, container_name: str, annotation_name: str):
        """Read information about an existing Annotation Container with the given identifier

        :param container_name: The container name
        :param annotation_name: The annotation name
        :return: Information about the annotation
        """
        url = f'{self.base_url}/w3c/{container_name}/{annotation_name}'
        response = self.__get(url=url)
        # ic(response)
        return self.__handle_response(response,
                                      {
                                          HTTPStatus.OK: lambda r: r.json(),
                                          HTTPStatus.NOT_FOUND: lambda r: None
                                      })

    def delete_annotation(self, container_name: str, annotation_name: str):
        """Remove the Annotation with the given name in the container with the given identifier

        :param container_name: the container name
        :param annotation_name: the annotation name
        :return:
        """
        url = f'{self.base_url}/w3c/{container_name}/{annotation_name}'
        response = self.__delete(url=url)
        return self.__handle_response(response, {HTTPStatus.NO_CONTENT: lambda r: True})

    def get_ping(self):
        url = f'{self.admin_url}/ping'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def __get(self, url, params=None, **kwargs):
        args = self.__set_defaults(kwargs)
        return requests.get(url, params=params, **args)

    def __post(self, url, data=None, json=None, **kwargs):
        args = self.__set_defaults(kwargs)
        return requests.post(url, data=data, json=json, **args)

    def __put(self, url, data=None, **kwargs):
        args = self.__set_defaults(kwargs)
        return requests.put(url, data=data, **args)

    def __delete(self, url, **kwargs):
        args = self.__set_defaults(kwargs)
        return requests.delete(url, **args)

    def __set_defaults(self, args: dict):
        if 'headers' not in args:
            args['headers'] = {}
        args['headers']['User-Agent'] = f'annorepo-python-client/{annorepo.__version__}'
        if self.api_key:
            args['headers']['Authorization'] = f'Basic {self.api_key}'
        if self.timeout:
            args['timeout'] = self.timeout
        return args

    def __handle_response(self, response: Response, result_producers: dict):
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
