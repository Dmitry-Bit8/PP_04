import sys
import os

# Добавляем корневую директорию проекта в путь поиска модулей, 
# чтобы Python видел папку 'generated'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generated import example_pb2
from generated import example_pb2_grpc


# Реализуем сервис
class GreeterServicer(example_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        # request.name — поле из HelloRequest
        message = f"Hello, {request.name}!"
        return example_pb2.HelloReply(message=message)

def serve():
    # Создаём gRPC сервер
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Регистрируем наш сервис
    example_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)

    # Запускаем на порту 50051 (стандартный порт gRPC)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")

    # Держим сервер запущенным
    try:
        while True:
            time.sleep(86400)  # 1 день
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
