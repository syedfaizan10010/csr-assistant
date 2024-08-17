import azure.cognitiveservices.speech as speech_sdk
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

class TranscribeService:
    def __init__(self):
        self.speech_key = os.environ["SPEECH_KEY"]
        self.region = os.environ["SPEECH_REGION"]

    async def ConfigureSpeech(self, type, voice_type=None):
        speech_key = self.speech_key
        region = self.region
        speech_config = speech_sdk.SpeechConfig(subscription=speech_key, region=region)
        #speech_config.set_property(speech_sdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "10000")
        
        if type == "Recognizer":
            # Use microphone
            audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
            speech_recognizer = speech_sdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
            return speech_recognizer
        elif type == "Synthesizer":
            if voice_type is None:
                voice_type = os.environ["ENGLISH"]  # default voice type -> english neutral
            speech_config.speech_synthesis_voice_name = voice_type
            speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config=speech_config)
            return speech_synthesizer
        else:
            return None

    async def RecognizeSpeech(self):
        print("Starting continuous recognition. Speak into your microphone.")
        speech_recognizer = await self.ConfigureSpeech(type="Recognizer")
        
        # Store recognized text
        recognized_text = []

        # Event handler for recognized speech
        def recognized(evt):
            if evt.result.reason == speech_sdk.ResultReason.RecognizedSpeech:
                print(f"Recognized: {evt.result.text}")
                recognized_text.append(evt.result.text)
                
            elif evt.result.reason == speech_sdk.ResultReason.NoMatch:
                print("No speech could be recognized.")

        # Connect the event handler to the recognized event
        speech_recognizer.recognized.connect(recognized)
        
        # Start continuous recognition
        speech_recognizer.start_continuous_recognition_async()
        
        # Keep the recognition going until user stops it manually
        print("Press Enter to stop...")
        input()  # Wait for user input to stop recognition
        
        # Stop recognition
        speech_recognizer.stop_continuous_recognition_async()
        print("Recognition stopped.")
        
        # Return the concatenated recognized text
        recognized_text = ' '.join(recognized_text)
        return recognized_text

    async def SynthesizeSpeech(self, voice_type, text=None):
        speech_synthesizer = await self.ConfigureSpeech(type="Synthesizer", voice_type=voice_type)
        res = speech_synthesizer.speak_text_async(text).get()
        return res

# # Example usage
# async def main():
#     ser = TranscribeService()
#     recognized_text = await ser.RecognizeSpeechContinuously()
#     print(f"Full recognized text: {recognized_text}")

# asyncio.run(main())
