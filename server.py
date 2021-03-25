from concurrent import futures 

import grpc
import sys

import services_informer_pb2, services_informer_pb2_grpc

#dicionário global para guardar informações dos servidos lidos, com key = nome do serviço
# (para não ler a cada chamada de função)
all_services = {}

class Communication(services_informer_pb2_grpc.CommunicationServicer):

    def get_port(self, request, context):
        if request.name in all_services:
            s_port = all_services[request.name][1]
        else:
            s_port = -1
        print("[log] The client {} wants to 'get port' of service '{}'.\nResponde: {}\n".format(
            context.peer(), request.name, s_port
        ))
        return services_informer_pb2.PortReply(port=s_port)

    def get_desc(self, request, context):
        if request.name in all_services:
            s_name = all_services[request.name][0]
            s_port = all_services[request.name][1]
            s_protocol = all_services[request.name][2]
            s_aliases = all_services[request.name][3]
            s_comment = all_services[request.name][4]
        else:
            s_name = ""
            s_port = -1
            s_protocol = ""
            s_aliases = ""
            s_comment = ""
        print("[log] The client {} wants to 'get_desc' of service {}.\nResponde: {} | {} | {} | {} | {}\n".format(
            context.peer(), request.name, s_name, s_port, s_protocol, s_aliases, s_comment
        ))
        return services_informer_pb2.DescReply(
            name=s_name, port=s_port, protocol = s_protocol, aliases = s_aliases, comment = s_comment
        )

def serve():
    if len(sys.argv) < 3:
        sys.exit("error: missing args - server <port> <services_file>")
    
    try:
        file = open(sys.argv[2], 'r')
    except:
        sys.exit("error: cannot open the file")
    
    lines = file.readlines()

    #gerar dicionário desorganizado
    count = 0
    for line in lines:
        if line[0] != '#' and line[0] != '\n':
            words = line.split()
            if words[0] not in all_services:
                    all_services[words[0]] = words

    #organizar dicionário modelo /etc/services
    # nome(string) - porta(int) - protocolo(string) - aliases(string) - comment(string) 
    for key, values in all_services.items():
        name = values[0]
        port, protocol = values[1].split('/')
        port = int(port)
        aliases = ''
        comment = ''
        if len(values) > 2:
            comment_flag = False
            for i in range(2, len(values)):
                if values[i] == '#':        #Verificar se começou o comentário
                    comment_flag = True

                if comment_flag == False:
                    if aliases == "":  #para string não ir com ' ' no começo
                        aliases = values[i]
                    else:
                        aliases = aliases + " " + values[i]
                else:
                    if comment == "":
                        comment = values[i]
                    else:
                        comment = comment + " " + values[i]
        
        all_services[key] = [name, port, protocol, aliases, comment]
   
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_informer_pb2_grpc.add_CommunicationServicer_to_server(Communication(), server)

    addr_and_port = '0.0.0.0:' + sys.argv[1]
    server.add_insecure_port(addr_and_port)

    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
