import requests


class ContainerIdentifier:
    def __init__(self, url: str, etag: str):
        if not url.endswith('/'):
            url = f"{url}/"
        self.url = url
        self.uuid = url.split('/')[-2]
        self.etag = etag

    def __str__(self):
        return f"ContainerIdentifier:\n  url = {self.url}\n  uuid = {self.uuid}\n  etag = {self.etag}"

    def __repr__(self):
        return self.__str__()


class AnnotationIdentifier:
    def __init__(self, url: str, etag: str):
        self.url = url
        url_split = url.split('/')
        self.uuid = url_split[-1]
        self.container_uuid = url_split[-2]
        self.etag = etag

    def __str__(self):
        return f"AnnotationIdentifier:\n  url = {self.url}\n  container_uuid = {self.container_uuid}\n  uuid = {self.uuid}\n  etag = {self.etag}"

    def __repr__(self):
        return self.__str__()

    def container_identifier(self) -> ContainerIdentifier:
        container_url = self.url.replace(self.uuid, '')
        return ContainerIdentifier(container_url)


class AnnotationCollection:
    def __init__(self, total, id: str, first_page: dict, label: str):
        self.total = total
        self.id = id
        self.first_page = first_page
        self.label = label
        self.page = 0
        self.url_extend_character = self._url_extend_character()

    def reset(self):
        self.page = 0

    def annotations_as_json(self):
        if 'items' not in self.first_page:
            raise StopIteration
        annotations = self.first_page['items']
        annotations_yielded = 0
        while annotations_yielded < self.total:
            yield from annotations
            annotations_yielded += len(annotations)
            if self.total > annotations_yielded:
                self.page += 1
                next_page_url = f"{self.id}{self.url_extend_character}page={self.page}"
                result = requests.get(url=next_page_url)
                json = result.json()
                if 'items' in json:
                    annotations = result.json()['items']
                else:
                    raise StopIteration

    def _url_extend_character(self):
        if '?' in self.id:
            return '&'
        else:
            return '?'
