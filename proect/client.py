import grpc
from generated import example_pb2
from generated import example_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = example_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(example_pb2.HelloRequest(name='Dmitry'))
    print(f"Response received: {response.message}")

if __name__ == '__main__':
    run()
