import grpc
from concurrent import futures
from grpc_service import speech_service_pb2_grpc
from Controller.TranscribeGenerateController import TranscribeGenerateController

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    speech_service_pb2_grpc.add_SpeechServiceServicer_to_server(TranscribeGenerateController(),server=server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server Running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

