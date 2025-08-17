# Offline-RAG-Enhanced-Voice-to-Text-POS-Prototype
# Voice-based POS System

This project is a simple **Voice-Enabled Point of Sale (POS)** application built with:
- **Vosk** (offline speech recognition)
- **SpeechRecognition + Google API** (for detecting "order")
- **Pyttsx3** (text-to-speech)
- **Python JSON** (inventory management)

The system allows users to **speak an order** (e.g., *"1 coffee 2 milk 3 bread"*), which is recognized from an audio file (`order.wav`), parsed, added to a cart, and summarized with pricing.

---

## 🔹 Architecture

**Modules:**
1. **Voice Command Listener** – Listens via microphone until the user says "order".
2. **Audio Preprocessing** – Converts `order.wav` into 16kHz mono PCM format.
3. **Speech Recognition** – Uses Vosk to transcribe spoken order.
4. **Order Parsing** – Maps words/numbers into inventory items and quantities.
5. **Cart & Checkout** – Computes totals and speaks the final bill.

**Workflow:**

---

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install vosk SpeechRecognition pyttsx3 librosa soundfile
mkdir models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip

### 2. Inventory File

Create a file named inventory.json:
[
  {"name": "coffee", "price": 5},
  {"name": "milk", "price": 3},
  {"name": "bread", "price": 2}
]
### 3. Run the Program
python voice_pos.py

### 🎤 Sample Run

Step 1: System prompts
[System]: What do you want to eat sir?
Step 2: User says → "order"

Step 3: System processes order.wav containing:
"I want 1 coffee "
 ## Expected Output:
You said: at one coffee
Added items: {'coffee': 1}

=== Checkout ===
Coffee: 1 x $3 = $3
Total: $3
[System]: Your total is 3 dollars.

### ✅ Testing
Sample Audio Inputs

order.wav – "I want 1 coffee 2 milk 3 bread"
→ Expected output: Coffee=1, Milk=2, Bread=3, Total=$17

order2.wav – "Please give me two coffee and one bread"
→ Expected output: Coffee=2, Bread=1, Total=$12

order3.wav – "Can I get 3 milk"
→ Expected output: Milk=3, Total=$9
### 🚀 Future Improvements

Continuous conversation (multiple orders in one session).

Noise handling and confidence scoring.

Larger vocabulary / menu expansion.

Direct microphone order capture instead of static .wav.


---

## 📝 **Short Report (1–2 pages)**

### **Voice-based POS System – Challenges, Trade-offs, and Improvements**

#### **Introduction**
This project develops a simple **voice-based POS system** that takes customer orders via speech, converts them into structured items, and calculates billing totals. The system leverages offline speech recognition (Vosk), text-to-speech (pyttsx3), and Python for parsing and inventory management.

---

#### **Challenges Faced**
1. **Audio Format Compatibility**  
   - Vosk requires **WAV mono PCM 8kHz/16kHz**. Most recordings were stereo or MP3.  
   - We solved this by adding a preprocessing step with **Librosa + SoundFile** to resample and convert audio.

2. **Recognition Accuracy**  
   - Free-form natural speech like *“can I get”* or *“please give me”* caused extra words in transcription.  
   - We implemented **keyword-based parsing** to detect only item names and numbers.

3. **Inventory Mapping**  
   - Users may say *“coffees”* instead of *“coffee”*. Handling plural and variations was a challenge.  
   - Trade-off: Limited grammar rules vs. large NLP models. We chose a **lightweight parser** for simplicity.

4. **Voice Command Trigger**  
   - Always listening wastes CPU and risks false triggers.  
   - Solution: Use Google’s API (via SpeechRecognition) just to detect the keyword **"order"**, then switch to offline Vosk for detailed parsing.

---

#### **Trade-offs**
- **Offline vs Online Recognition**  
  - Vosk works offline (faster, no internet needed) but is less accurate than cloud-based APIs.  
  - Trade-off: **Privacy & speed vs accuracy**.

- **Static Audio (`order.wav`) vs Live Mic**  
  - Using `.wav` makes testing reproducible but less natural.  
  - Trade-off: **Consistency vs Realism**.

- **Lightweight Parsing vs NLP Models**  
  - Regex + keyword-based parsing is simple but limited for complex sentences.  
  - Larger NLP models (e.g., GPT, spaCy) would be more accurate but heavier.

---

#### **Possible Improvements**
1. **Continuous Dialogue** – Allow customers to add multiple items interactively.  
2. **Noise Robustness** – Apply noise reduction filters for real-world use.  
3. **Expanded Vocabulary** – Handle synonyms, plurals, and custom menu items.  
4. **GUI Integration** – Display cart visually alongside voice output.  
5. **Multilingual Support** – Add support for local languages via Vosk multilingual models.

---

#### **Conclusion**
This project demonstrates a **functional end-to-end voice ordering system** with offline recognition and cart management. While challenges around audio quality and recognition accuracy remain, the system can be extended into a practical solution for small cafés, kiosks, or restaurants with further improvements.

---

👉 Would you like me to also **generate a ready-made `order.wav` sample file** (synthetic voice saying *"I want 1 coffee 2 milk 3 bread"*) so you can test immediately?
