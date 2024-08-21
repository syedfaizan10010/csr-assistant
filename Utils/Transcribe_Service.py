import azure.cognitiveservices.speech as speech_sdk
import os
import asyncio
from dotenv import load_dotenv
from transformers import pipeline
import numpy
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from datasets import load_dataset
from pydub import AudioSegment
from pydub.playback import play
import logging

load_dotenv()
logging.basicConfig(
    filename="postcall_transcript_sentiment_analysis.log",
    level=logging.INFO,
    format='%(message)s'
)

class TranscribeService:
  
    def __init__(self):
        self.speech_key = os.environ.get("SPEECH_KEY","4fa331f9902a491680842e1189b868f6")
        self.region = os.environ.get("SPEECH_REGION","eastus")
    

    async def ConfigureSpeech(self, type, voice_type=None, audio_file =None):
        speech_key = self.speech_key
        region = self.region
        speech_config = speech_sdk.SpeechConfig(subscription=speech_key, region=region)
        #speech_config.set_property(speech_sdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "10000")
        
        if type == "Recognizer":
            # Use microphone
            file ="speech-text.wav"
            if audio_file:
                audio_config = speech_sdk.AudioConfig(filename=file)
            else:
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
        print("Ask Something...")
        speech_config = await self.ConfigureSpeech(type="Recognizer", audio_file= False)
        result = speech_config.recognize_once_async().get()
        if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
            #print(f"Recognized speech:{result.text}")
            return result.text
        else:
            print("Speech Not Recognized")
            return None


    async def SynthesizeSpeech(self, voice_type, text=None):
        speech_synthesizer = await self.ConfigureSpeech(type="Synthesizer", voice_type=voice_type)
        res = speech_synthesizer.speak_text_async(text).get()
        return res
    
    async def TTS_hugging_face(self, text):
        
        TTS_Model = os.environ.get('HUGGING_FACE_TTS','microsoft/speecht5_tts')
        VO_coder = os.environ.get('HUGGING_FACE_VOCODER','microsoft/speecht5_hifigan')
        processor = SpeechT5Processor.from_pretrained(TTS_Model)
        model = SpeechT5ForTextToSpeech.from_pretrained(TTS_Model)
        vocoder = SpeechT5HifiGan.from_pretrained(VO_coder)

        inputs = processor(text=text, return_tensors="pt")

        # load xvector containing speaker's voice characteristics from a dataset
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        output_file ="speech.wav"
        sf.write(output_file, speech.numpy(), samplerate=16000)
        sound = AudioSegment.from_wav(output_file)
        play(sound)
        return "Done"
    
    def analyse_sentiment(self, texts):
        sentiment_analysis= pipeline(
            "sentiment-analysis",
            model = "nlptown/bert-base-multilingual-uncased-sentiment",
        )
       
        results = sentiment_analysis(texts)
        sentiment_results =[]
        for text, sentiment in zip(texts, results):
            sentiment_results.append({
                "Text": text,
                "Sentiment": sentiment
            })
            # print(f"Text:{text}\n Sentiment: {sentiment}")
        return sentiment_results
    


    async def RecognizeSpeech_cont(self):
        print("Starting continuous recognition. Speak into your microphone.")
        speech_recognizer = await self.ConfigureSpeech(type="Recognizer", audio_file= False)
        
        # Store recognized text
        recognized_text = []

        # Event handler for recognized speech
        def recognized(evt):
            if evt.result.reason == speech_sdk.ResultReason.RecognizedSpeech:
                #print(f"Recognized: {evt.result.text}")
                current_text = evt.result.text
                recognized_text.append(current_text)
                # print(recognized_text)
                # recognized_text.append(evt.result.text)
                sentiment = self.analyse_sentiment([current_text])
                logging.info(sentiment)
                print(sentiment)
                
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
        sentiment = self.analyse_sentiment([recognized_text])
        logging.info(sentiment)
        print(sentiment)
        return recognized_text
        

##Example usage
ser = TranscribeService()
asyncio.run(ser.RecognizeSpeech_cont())
 # texts =[
        #     "I Hate programming!",           # English
        #     "La vida es bella.",             # Spanish
        #     "Je déteste ce produit.",        # French
        #     "Das ist wunderbar!",            # German
        #     "これは素晴らしいです！",      # Japanese
        #     "ನನಗೆ ಇದು ಬಹಳ ಇಷ್ಟವಾಗಿದೆ", #kannada
        #     "أنا سعيد جدا." #arabic 

        # ]