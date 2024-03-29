# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import annorepo.grpc.hello_service_pb2 as hello__service__pb2


class HelloServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SayHello = channel.unary_unary(
            '/nl.knaw.huc.annorepo.grpc.v1.HelloService/SayHello',
            request_serializer=hello__service__pb2.SayHelloRequest.SerializeToString,
            response_deserializer=hello__service__pb2.SayHelloResponse.FromString,
        )


class HelloServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SayHello(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HelloServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'SayHello': grpc.unary_unary_rpc_method_handler(
            servicer.SayHello,
            request_deserializer=hello__service__pb2.SayHelloRequest.FromString,
            response_serializer=hello__service__pb2.SayHelloResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'nl.knaw.huc.annorepo.grpc.v1.HelloService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class HelloService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SayHello(request,
                 target,
                 options=(),
                 channel_credentials=None,
                 call_credentials=None,
                 insecure=False,
                 compression=None,
                 wait_for_ready=None,
                 timeout=None,
                 metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nl.knaw.huc.annorepo.grpc.v1.HelloService/SayHello',
                                             hello__service__pb2.SayHelloRequest.SerializeToString,
                                             hello__service__pb2.SayHelloResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
