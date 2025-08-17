import json
import wave
import numpy as np
import soundfile as sf
import librosa
import pyttsx3
from vosk import Model, KaldiRecognizer

# --- Text-to-speech setup ---
engine = pyttsx3.init()

def speak(text):
    print(f"[System]: {text}")
    engine.say(text)
    engine.runAndWait()

# --- Inventory ---
with open("inventory.json") as f:
    inventory = json.load(f)

cart = {}

number_map = {
    "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10
}

def word_to_number(word):
    word = word.lower()
    if word in number_map:
        return number_map[word]
    elif word.isdigit():
        return int(word)
    return 1

# --- Convert audio to mono PCM 16kHz ---
def convert_wav(file_path):
    data, sr = sf.read(file_path)
    if sr != 16000:
        data = librosa.resample(data.T, orig_sr=sr, target_sr=16000)
        data = data.T
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    sf.write(file_path, data, 16000, subtype='PCM_16')

# --- Transcribe audio ---
def transcribe_audio(file_path):
    model = Model("models/vosk-model-small-en-us-0.15")
    wf = wave.open(file_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text += json.loads(result).get("text", "")
    final = rec.FinalResult()
    text += json.loads(final).get("text", "")
    return text.strip().lower()

# --- Parse items ---
def parse_command(text):
    items = {}
    words = text.split()
    i = 0
    while i < len(words):
        qty = 1
        name = None
        if words[i] in number_map or words[i].isdigit():
            qty = word_to_number(words[i])
            i += 1
        if i < len(words):
            for item in inventory:
                if item['name'] in words[i]:
                    name = item['name']
                    break
        if name:
            items[name] = items.get(name, 0) + qty
        i += 1
    return items

# --- Add to cart ---
def add_to_cart(items):
    for item, qty in items.items():
        cart[item] = cart.get(item, 0) + qty
    print(f"Added items: {items}")

# --- Checkout ---
def checkout():
    print("\n=== Checkout ===")
    total = 0
    for item_name, qty in cart.items():
        price = next(item['price'] for item in inventory if item['name'] == item_name)
        item_total = price * qty
        total += item_total
        print(f"{item_name.capitalize()}: {qty} x ${price} = ${item_total}")
    print(f"Total: ${total}")
    speak(f"Your total is {total} dollars.")

# --- Main ---
if __name__ == "__main__":
    # Step 1: Ask for file name
    speak("Please say your order file name.")
    print("Waiting for input... (For demo we will use 'order.wav')")

    # For now, we directly use order.wav
    wav_file = "add_coffee.wav"

    # Step 2: Convert audio
    convert_wav(wav_file)

    # Step 3: Transcribe
    speak("Listening to your order now.")
    text = transcribe_audio(wav_file)
    print(f"You said: {text}")

    # Step 4: Parse + checkout
    items = parse_command(text)
    if items:
        add_to_cart(items)
        checkout()
    else:
        speak("Sorry, I could not recognize any items.")
