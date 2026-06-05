import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generated import example_pb2
from generated import example_pb2_grpc

class GreeterServicer(example_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
    
        message = f"Hello, {request.name}!"
        return example_pb2.HelloReply(message=message)

def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

 
    example_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)

   
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
