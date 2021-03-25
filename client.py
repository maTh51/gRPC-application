from __future__ import print_function
import sys
import grpc

import services_informer_pb2, services_informer_pb2_grpc

def run():
    if len(sys.argv) < 3:
        sys.exit("error: missing args - client <addr:port> <service_name>")

    channel = grpc.insecure_channel(sys.argv[1])

    stub = services_informer_pb2_grpc.CommunicationStub(channel)

    #primeiro request - porta
    response = stub.get_port(services_informer_pb2.ServName(name=sys.argv[2]))
    print("GRPC client received 'port' of service: '{}'\nport: {}\n".format(sys.argv[2], response.port))

    #segundo request - descrição
    response = stub.get_desc(services_informer_pb2.ServName(name=sys.argv[2]))
    print("GRPC client received 'desc' of service '" + sys.argv[2] + "':")
    print("Name: {}\nPort: {}\nProtocol: {}\nAliases: {}\nComment: {}\n".format(
        response.name, response.port, response.protocol, response.aliases, response.comment
    ))
    
    channel.close()


if __name__ == '__main__':
    run()
