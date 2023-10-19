#!/usr/bin/env python3
import json

import grpc
from icecream import ic

from annorepo.grpc.annotation_upload_service_pb2 import AddAnnotationsRequest
from annorepo.grpc.annotation_upload_service_pb2_grpc import AnnotationUploadServiceStub
from annorepo.grpc.hello_service_pb2 import SayHelloRequest
from annorepo.grpc.hello_service_pb2_grpc import HelloServiceStub


def web_annotation(id: int):
    return {
        "id": f"annotation-{id}",
        "body": f"body-{id}",
        "target": f"target-{id}"
    }


def main():
    with grpc.insecure_channel('localhost:8000') as channel:
        stub = HelloServiceStub(channel)
        response = stub.SayHello(SayHelloRequest(name="me", api_key="bla"))
        ic(response)
        response = stub.SayHello(SayHelloRequest(name="world", api_key="bla"))
        ic(response)

        stub = AnnotationUploadServiceStub(channel)
        anno1 = json.dumps(web_annotation(1))
        anno2 = json.dumps(web_annotation(2))
        anno3 = json.dumps(web_annotation(3))
        req1 = AddAnnotationsRequest(api_key="", container_name="A", annotation=[anno1])
        req2 = AddAnnotationsRequest(api_key="", container_name="b", annotation=[anno1, anno2, anno3])
        response = stub.AddAnnotations(req1)
        ic(response)
        response = stub.AddAnnotations(req2)
        ic(response)


if __name__ == '__main__':
    main()
