import os
import speech_recognition as sr
from gtts import gTTS
import pygame
import openai
import uuid


# Inicializar a API OpenAI
def chat_with_gpt(prompt):
    openai.api_key = "sua-key" #informe aqui sua key da openai
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response["choices"][0]["text"].strip()

def text_to_speech(text):
    path = "output"
    if not os.path.exists(path):
        os.makedirs(path)

    filename = os.path.join(path, str(uuid.uuid1()) + ".mp3")
    tts = gTTS(text=text, lang="pt-BR")
    tts.save(filename)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def transcribe_speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Diga algo:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="pt-BR")
        print("Você disse: {}".format(text))
        response = chat_with_gpt(format(text))
        print(response)
        text_to_speech(response)
        return text
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        text_to_speech("Não entendi o que você disse, pode repetir?")
    except sr.RequestError as e:
        text_to_speech("Falha na execução no serviço de reconhecimento de fala")
        print("Erro ao chamar o serviço de reconhecimento de fala; {0}".format(e))

if __name__ == "__main__":
    while True:
     transcribe_speech_to_text()
