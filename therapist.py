import gradio as gr
import pyttsx3
import openai, config, subprocess
from pydub import AudioSegment

openai.api_key = config.OPENAI_API_KEY

messages = [{"role": "system", "content": 'You are a therapist. Respond to all input in 25 words or less.'}]

def transcribe(audio):
    global messages

    audio_segment = AudioSegment.from_file(audio).export("converted_audio.wav", format="wav")
    print(audio_segment)
    
    with open("converted_audio.wav", "rb") as audio:
        transcript = openai.Audio.transcribe('whisper-1', audio)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": system_message})
    
     #python speech module
    engine = pyttsx3.init()
        # set female voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate+10)

    engine.say(system_message)
    engine.runAndWait()

    chat_transcript = ""
    for message in messages:
        if message["role"] != 'system':
            chat_transcript += message["role"] + ": " + message["content"] + "\n\n"

    return chat_transcript



ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone",type="filepath"), outputs="text")

ui.launch(share=True)
