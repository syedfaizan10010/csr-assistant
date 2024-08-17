from AIGeneration_Service import AIGenerationService
from utils.Transcribe_Service_trial import TranscribeService
import asyncio
import os
async def exec():
    trans_service = TranscribeService()
    ai_service = AIGenerationService()

    user_ip =await trans_service.RecognizeSpeech()
    response_text = await ai_service.GenerateResponse(user_ip)
    await trans_service.SynthesizeSpeech(voice_type= os.environ['ARABIC'],text=response_text)

asyncio.run(exec())
