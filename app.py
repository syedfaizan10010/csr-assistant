from Controller.TranscribeGenerateController import TranscribeGenerateController
from flask import Flask,jsonify, request
import asyncio


app = Flask(__name__)
loop = asyncio.get_event_loop()


@app.route('/execute', methods=['Post'])
def execute_conversation():
    controller = TranscribeGenerateController()
    result = loop.run_until_complete(controller.ExecuteConversation())
    return jsonify({"response":result})

@app.route('/azure_STT', methods=['GET'])
def speech_to_text():
    controller = TranscribeGenerateController()
    response = loop.run_until_complete(controller.speech_to_text())
    return jsonify({"Response": response})

@app.route('/azure_TTS', methods=['POST'])
def text_to_speech():
    controller = TranscribeGenerateController()
    data = request.get_json()
    prompt = data.get('prompt')
    voice_type = data.get('voice_type')
    if not prompt or not voice_type:
        return jsonify({"error":"Please provide prompt and voice type"}),400
    response = loop.run_until_complete(controller.text_to_speech(prompt=prompt, language=voice_type))
    return jsonify({"status":response}), 200

@app.route('/speech_HF', methods =['POST'])
def tts_hugging_face():
    controller = TranscribeGenerateController()
    data = request.get_json()
    text = data.get('text')
    response = loop.run_until_complete(controller.text_to_speech_hugging_face(text=text))
    return jsonify({"status":response}), 200

@app.route('/analyse_sentiment_HF', methods =['POST'])
def analyse_sentiment():
    controller = TranscribeGenerateController()
    data = request.get_json()
    texts = data.get('texts',[])
    processed_texts = [text.upper() for text in texts]  # Example processing
    response = loop.run_until_complete(controller.analyse_sentiment_hugging_face(text=processed_texts))
    return jsonify({"status":response}), 200





if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000)