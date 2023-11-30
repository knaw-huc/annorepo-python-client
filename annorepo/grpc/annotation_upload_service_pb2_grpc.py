# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import annorepo.grpc.annotation_upload_service_pb2 as annotation__upload__service__pb2


class AnnotationUploadServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddAnnotations = channel.unary_unary(
            '/nl.knaw.huc.annorepo.grpc.v1.AnnotationUploadService/AddAnnotations',
            request_serializer=annotation__upload__service__pb2.AddAnnotationsRequest.SerializeToString,
            response_deserializer=annotation__upload__service__pb2.AddAnnotationsResponse.FromString,
        )


class AnnotationUploadServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AddAnnotations(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AnnotationUploadServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'AddAnnotations': grpc.unary_unary_rpc_method_handler(
            servicer.AddAnnotations,
            request_deserializer=annotation__upload__service__pb2.AddAnnotationsRequest.FromString,
            response_serializer=annotation__upload__service__pb2.AddAnnotationsResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'nl.knaw.huc.annorepo.grpc.v1.AnnotationUploadService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class AnnotationUploadService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AddAnnotations(request,
                       target,
                       options=(),
                       channel_credentials=None,
                       call_credentials=None,
                       insecure=False,
                       compression=None,
                       wait_for_ready=None,
                       timeout=None,
                       metadata=None):
        return grpc.experimental.unary_unary(request, target,
                                             '/nl.knaw.huc.annorepo.grpc.v1.AnnotationUploadService/AddAnnotations',
                                             annotation__upload__service__pb2.AddAnnotationsRequest.SerializeToString,
                                             annotation__upload__service__pb2.AddAnnotationsResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)