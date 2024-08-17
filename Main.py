from utils.Transcribe_Service_trial import TranscribeService
from utils.AIGeneration_Service import AIGenerationService
#import grpc
#from concurrent import futures
from grpc_service import speech_service_pb2_grpc
#from Controller import TranscribeGenerateController
import asyncio
import os
class Main():

    async def execute(self,):

        transcribe_service = TranscribeService()
        aigeneration_service = AIGenerationService()

        while True:
            user_input = await transcribe_service.RecognizeSpeech()

            if user_input:
                response_text = await aigeneration_service.GenerateResponse(user_input)
                await transcribe_service.SynthesizeSpeech(voice_type=os.environ['ENGLISH'], text = response_text)

                # await transcribe_service.SynthesizeSpeech(voice_type=os.environ['ARABIC'], text = "Do you need more help?")
                # follow_up = await transcribe_service.RecognizeSpeech()

                # if "no" in follow_up:
                #     await transcribe_service.SynthesizeSpeech(voice_type=os.environ['ARABIC'], text = "Okay, ending the conversation.. have a good day")
                #     break
                # else:
                #     response_text = await aigeneration_service.GenerateResponse(follow_up)
                #     await transcribe_service.SynthesizeSpeech(voice_type=os.environ['ARABIC'], text = response_text)
                #     break

    
#     def serve():
#         server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#         speech_service_pb2_grpc.add_SpeechServiceServicer_to_server(TranscribeGenerateController(),server=server)
#         server.add_insecure_port('[::]:50051')
#         server.start()
#         print("Server Running on port 50051")
#         server.wait_for_termination()

#     # if __name__ == "__main__":
#     #     serve()
service = Main()
asyncio.run(service.execute())
                

# service = Main()
# asyncio.run(service.execute())