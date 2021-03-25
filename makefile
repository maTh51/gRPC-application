generate_protos:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. services_informer.proto

clear:
	rm services_informer_pb2_grpc.py && rm services_informer_pb2.py

run_server:
	python3 server.py $(arg1) $(arg2)
 
run_client:
	python3 client.py $(arg1) $(arg2)

