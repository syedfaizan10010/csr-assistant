import azure.cognitiveservices.speech as speech_sdk
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


class TranscribeService:
    def __init__(self) -> None:
        pass

    async def ConfigureSpeech(self,type = None):
        speech_key =os.environ["SPEECH_KEY"]
        region = os.environ["SPEECH_REGION"]
        speech_config = speech_sdk.SpeechConfig(subscription =speech_key, region = region )
        if type == "Recognizer":
             #Use microphone 
            audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
            speech_recognizer = speech_sdk.SpeechRecognizer(speech_config = speech_config, audio_config = audio_config )
            return speech_recognizer
        elif type =="Synthesizer":
            #speech_config.speech_synthesis_voice_name = "en-US-EmmaMultilingualNeural" # english
            
            #speech_config.speech_synthesis_voice_name = "ar-KW-FahedNeural" #Arabic

            speech_config.speech_synthesis_voice_name = "es-AR-TomasNeural" #Spanish


            speech_recognizer = speech_sdk.SpeechSynthesizer(speech_config = speech_config )
            return speech_recognizer
        else:
            return ""

    
    async def RecognizeSpeech(self):
        print("Ask Something...")
        speech_config = await self.ConfigureSpeech(type="Recognizer")
        result = speech_config.recognize_once_async().get()
        if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
            print(f"Recognized speech:{result.text}")
            return result.text
        else:
            print("Speech Not Recognized")
            return None
    
    async def SynthesizeSpeech(self, text = None):
        speech_config = await self.ConfigureSpeech(type="Synthesizer")
        result = speech_config.speak_text_async(text).get()
        return result
