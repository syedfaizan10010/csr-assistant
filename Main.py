from Service.Transcribe_Service import TranscribeService
from Service.AIGeneration_Service import AIGeneration_Service
import asyncio
class Main():

    async def execute(self):

        transcribe_service = TranscribeService()
        aigeneration_service = AIGeneration_Service()

        user_input = await transcribe_service.RecognizeSpeech()

        if user_input:
            response_text = await aigeneration_service.GenerateResponse(user_input)
            await transcribe_service.SynthesizeSpeech(response_text)

service = Main()
asyncio.run(service.execute())