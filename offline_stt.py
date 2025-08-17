import speech_recognition as sr
import pyttsx3
import sys
import re

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# Initialize recognizer
recognizer = sr.Recognizer()

# Inventory with prices
inventory = {
    "coffee": 3,
    "milk": 2
}

# Cart to store counts
cart = {}

# Mapping numbers in words to digits
number_words = {
    "one": 1,
    "to": 2,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10
}

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen for voice input
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='en_US')
        return text.lower()
    except:
        return ""

# Parse commands like "2 coffee" or "two coffee"
def parse_command(text):
    text = text.lower()
    # Replace number words with digits
    for word, digit in number_words.items():
        text = re.sub(r"\b" + word + r"\b", str(digit), text)

    match = re.match(r"(\d+)\s*(coffee|milk)", text)
    if match:
        count = int(match.group(1))
        item = match.group(2)
        return item, count
    return None, None

# Main POS workflow
def run_pos():
    speak("Voice POS started. Say your order like '2 coffee' or 'three milk'. Say 'checkout' or 'total' to finish.")
    while True:
        text = listen()
        if not text:
            print("Couldn't understand. Please repeat.")
            continue

        print("You said:", text)

        if "checkout" in text or "total" in text:
            speak("Checking out...")
            print("\n=== Checkout ===")
            total_price = 0
            for item, count in cart.items():
                price = inventory[item] * count
                total_price += price
                print(f"{item.capitalize()}: {count} x ${inventory[item]} = ${price}")
            print(f"Total: ${total_price}")
            speak(f"Your total is {total_price} dollars")
            break

        item, count = parse_command(text)
        if item:
            if item in cart:
                cart[item] += count
            else:
                cart[item] = count
            speak(f"Added {count} {item}(s) to cart")
            print(f"Cart updated: {cart}")
        else:
            speak("Command not recognized. Try saying '2 coffee' or 'three milk'.")

# Wake word system
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for wake word 'sonic'...")
        while True:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language='en_US').lower()
                if "sonic" in text:
                    speak("Hi! How can I help you?")
                    return
            except:
                pass

# Run assistant
while True:
    listen_for_wake_word()
    run_pos()
