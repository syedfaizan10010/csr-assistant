import grpc
from grpc_service import speech_service_pb2, speech_service_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = speech_service_pb2_grpc.SpeechServiceStub(channel=channel)

    response = stub.ExecuteConversation(speech_service_pb2.SpeechRequest(input = "test"))
    print("Response:",response.text)

if __name__ =="__main__":
    run()