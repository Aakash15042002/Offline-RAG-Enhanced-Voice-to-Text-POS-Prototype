from vosk import Model,KaldiRecognizer
import pyaudio

model = Model("./Vosk/vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(rate=16000, channels=1, format=pyaudio.paInt16,input=True, frames_per_buffer=8000)
stream.start_stream()
while True:
    data = stream.read(4096)
    # iflen(data) == 0:
    #break
    if recognizer.AcceptWaveform(data):
        print(recognizer.Result())
        