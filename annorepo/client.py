import http
from http import HTTPStatus

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
        url = f'{self.base_url}/about'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def get_homepage(self):
        url = f'{self.base_url}/'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_robots_txt(self):
        url = f'{self.base_url}/robots.txt'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_favicon(self):
        url = f'{self.base_url}/favicon.ico'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_swagger_json(self):
        url = f'{self.base_url}/swagger.json'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

    def get_swagger_yaml(self):
        url = f'{self.base_url}/swagger.yaml'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.text})

    def get_healthcheck(self):
        url = f'{self.admin_url}/healthcheck'
        response = self.__get(url=url)
        return self.__handle_response(response, {HTTPStatus.OK: lambda r: r.json()})

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
