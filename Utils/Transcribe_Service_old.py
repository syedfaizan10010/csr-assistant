import azure.cognitiveservices.speech as speech_sdk
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


class TranscribeService:
    def __init__(self):
        self.speech_key = os.environ["SPEECH_KEY"]
        self.region = os.environ["SPEECH_REGION"]
        pass

    async def ConfigureSpeech(self, type,voice_type = None):
        speech_key =self.speech_key
        region = self.region
        speech_config = speech_sdk.SpeechConfig(subscription =speech_key, region = region )
        speech_config.set_property(speech_sdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "10000")
        if type == "Recognizer":
             #Use microphone 
            audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
            speech_recognizer = speech_sdk.SpeechRecognizer(speech_config = speech_config, audio_config = audio_config )
            return speech_recognizer
        elif type =="Synthesizer":
            if voice_type is None:
                voice_type = os.environ["ENGLISH"] #default voice type -> english neutral
            speech_config.speech_synthesis_voice_name = voice_type 

            speech_recognizer = speech_sdk.SpeechSynthesizer(speech_config = speech_config )
            return speech_recognizer
        else:
            return ""

    
    async def RecognizeSpeech(self):
        print("Ask Something...")
        done = False
        speech_config = await self.ConfigureSpeech(type="Recognizer")
        result = speech_config.recognize_once_async().get()
        if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
            #print(f"Recognized speech:{result.text}")
            return result.text
        else:
            print("Speech Not Recognized")
            return None
    
    async def SynthesizeSpeech(self, voice_type, text = None):
        speech_config = await self.ConfigureSpeech(type="Synthesizer", voice_type=voice_type )
        res = speech_config.speak_text_async(text).get()
        return res

    def speech_recognize_continuous_async_from_microphone(self):
        """performs continuous speech recognition asynchronously with input from microphone"""
        speech_config = speech_sdk.SpeechConfig(subscription=self.speech_key, region=self.region)
        audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
        # The default language is "en-us".
        speech_recognizer = speech_sdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        done = False

        def recognizing_cb(evt: speech_sdk.SpeechRecognitionEventArgs):
            print('RECOGNIZING: {}'.format(evt))

        def recognized_cb(evt: speech_sdk.SpeechRecognitionEventArgs):
            print('RECOGNIZED: {}'.format(evt))

        def stop_cb(evt: speech_sdk.SessionEventArgs):
            """callback that signals to stop continuous recognition"""
            print('CLOSING on {}'.format(evt))
            nonlocal done
            done = True

        # Connect callbacks to the events fired by the speech recognizer
        speech_recognizer.recognizing.connect(recognizing_cb)
        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Perform recognition. `start_continuous_recognition_async asynchronously initiates continuous recognition operation,
        # Other tasks can be performed on this thread while recognition starts...
        # wait on result_future.get() to know when initialization is done.
        # Call stop_continuous_recognition_async() to stop recognition.
        result_future = speech_recognizer.start_continuous_recognition_async()

        result_future.get()  # wait for voidfuture, so we know engine initialization is done.
        print('Continuous Recognition is now running, say something.')

        while not done:
            # No real sample parallel work to do on this thread, so just wait for user to type stop.
            # Can't exit function or speech_recognizer will go out of scope and be destroyed while running.
            print('type "stop" then enter when done')

            stop = input()
            if (stop.lower() == "stop"):
                print('Stopping async recognition.')
                speech_recognizer.stop_continuous_recognition_async()
                break

        print("recognition stopped, main thread can exit now.")
ser = TranscribeService()
#test = "Virat Kohli is a renowned Indian cricketer who is considered one of the best batsmen in the world. He has achieved significant success in international cricket, particularly in One Day Internationals (ODIs) and Test matches. Kohli has led the Indian cricket team as captain and has received numerous awards and accolades for his exceptional performances on the field."
asyncio.run(ser.speech_recognize_continuous_async_from_microphone())


