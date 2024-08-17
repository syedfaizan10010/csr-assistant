
from grpc_service import speech_service_pb2
from grpc_service import speech_service_pb2_grpc
from utils.Transcribe_Service_trial import TranscribeService
from utils.AIGeneration_Service import AIGenerationService
import os
class TranscribeGenerateController(speech_service_pb2_grpc.SpeechServiceServicer):
    

    def __init__(self):
        self.transcribe_service = TranscribeService()
        self.generation_service = AIGenerationService()

    async def ExecuteConversation(self):
        while True:
            
            
            user_input = await self.transcribe_service.RecognizeSpeech()
            if user_input:
                    response_text = await self.generation_service.GenerateResponse(user_input)
                    await self.transcribe_service.SynthesizeSpeech(voice_type=os.environ['ENGLISH'], text = response_text)

                    await self.transcribe_service.SynthesizeSpeech(voice_type=os.environ['ENGLISH'], text = "Do you need more help?")
                    follow_up = await self.transcribe_service.RecognizeSpeech()

                    if "no" in follow_up:
                        await self.transcribe_service.SynthesizeSpeech(voice_type=os.environ['ARABIC'], text = "Okay, ending the conversation.. have a good day")
                        break
                    else:
                        response_text = await self.generation_service.GenerateResponse(follow_up)
                        await self.transcribe_service.SynthesizeSpeech(voice_type=os.environ['ARABIC'], text = response_text)
                        break

            return "Conversation Ended."

    async def speech_to_text(self):
        text = await  self.transcribe_service.RecognizeSpeech()
        return text
    
    async def text_to_speech(self, prompt, language):
         voice_types = self.get_voice_types()
         #voice_type= voice.get(voice_type)
         voice_type =next((type[language] for type in voice_types if language in type ), None)
         await self.transcribe_service.SynthesizeSpeech(text=prompt, voice_type=voice_type)
         return "Done"
    
    def get_voice_types(self):
      voice_types =[{"ENGLISH": os.environ['ENGLISH']},
              {"ARABIC": os.environ['ARABIC']},
              {"SPANISH": os.environ['SPANISH']},
              {"KANNADA": os.environ['KANNADA']}]
      return voice_types

        


        


