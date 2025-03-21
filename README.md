
# Iris - Virtual AI Assistant

## Overview
IRIS is a virtual AI assistant that provides various functionalities such as fetching news, checking weather updates, opening applications, searching Wikipedia, and more. The assistant is voice-controlled and uses NLP (Natural Language Processing) to process user queries.
---

## Features
- **Voice Interaction**: Recognizes spoken commands and responds with synthesized speech.
- **Time and Date**: Provides the current time and day of the week.
- **Social Media Access**: Opens websites like Facebook, WhatsApp, Discord, and Instagram.
- **Daily Schedule**: Reads out a pre-defined schedule based on the day of the week.
- **System Control**: Adjusts volume (up, down, mute, unmute) and monitors CPU usage and battery percentage.
- **Application Management**: Opens and closes apps like Calculator, Notepad, and Paint.
- **Web Browsing**: Performs Google searches based on voice input.
- **News Updates**: Fetches the latest news (general or sports) using NewsAPI.
- **Weather Reports**: Provides current weather conditions for a specified location using OpenWeatherMap.
- **Wikipedia Search**: Retrieves summaries from Wikipedia based on user queries.
- **Intent Recognition**: Uses a pre-trained TensorFlow model to classify user intents and provide appropriate responses.

---

## Prerequisites
Before running Iris, ensure you have the following:
1. **Python 3.8+**: Installed on your system.
2. **API Keys**:
   - **ElevenLabs API Key**: For text-to-speech functionality (stored in `api_key.py` as `Voce_api_key`).
   - **NewsAPI Key**: For fetching news (stored in `api_key.py` as `NEWS_API_KEY`).
   - **OpenWeatherMap API Key**: For weather updates (stored in `api_key.py` as `WEATHER_API_KEY`).
3. **Microphone**: For voice input.
4. **Pre-trained Model Files**:
   - `chat_model.h5`: Trained TensorFlow model for intent classification.
   - `tokenizer.pkl`: Tokenizer for text preprocessing.
   - `label_encoder.pkl`: Label encoder for intent tags.
   - `intents.json`: JSON file containing intent patterns and responses.

---

## Installation
1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd iris-assistant
   ```

2. **Install Dependencies**:
   Run the following command to install required Python libraries:
   ```bash
   pip install pynput pyautogui speechrecognition requests tensorflow pygame psutil wikipedia elevenlabs
   ```

3. **Set Up API Keys**:
   Create a file named `api_key.py` in the same directory as the script and add your API keys:
   ```python
   Voce_api_key = "your_elevenlabs_api_key"
   NEWS_API_KEY = "your_newsapi_key"
   WEATHER_API_KEY = "your_openweathermap_api_key"
   ```

4. **Prepare Model Files**:
   Ensure `chat_model.h5`, `tokenizer.pkl`, `label_encoder.pkl`, and `intents.json` are in the same directory as the script. These files must be pre-trained/generated separately (not included in this README).

---

## Usage
1. **Run the Script**:
   ```bash
   python iris.py
   ```
   Iris will initialize and introduce itself with: "Allow me to introduce myself, I am Iris, your virtual AI assistant here to help!"

2. **Interact with Iris**:
   - Speak commands into your microphone (e.g., "What is the time?", "Open Notepad", "Tell me the news").
   - Iris listens, processes the command, and responds via synthesized speech.

3. **Supported Commands**:
   - **Time/Date**: "Tell me the time", "What is the date and time"
   - **Social Media**: "Open Facebook", "Open WhatsApp"
   - **Schedule**: "What’s my schedule?", "Time table"
   - **Volume**: "Volume up", "Mute the volume", "Unmute"
   - **Apps**: "Open Calculator", "Close Notepad"
   - **Google**: "Search on Google"
   - **System**: "System condition"
   - **News**: "Tell me the news", "Sports news"
   - **Weather**: "What’s the weather in [location]?"
   - **Wikipedia**: "Tell me about [topic]", "Search [topic] on Wikipedia"
   - **Exit**: "Exit"

4. **Exit the Program**:
   Say "exit" to terminate Iris.

---

## Dependencies
- `pynput`: For keyboard/mouse control (unused in this script but imported).
- `pyautogui`: For volume control.
- `speech_recognition`: For voice input via microphone.
- `requests`: For API calls (news, weather).
- `tensorflow`: For intent recognition model.
- `pygame`: For playing audio responses.
- `psutil`: For system monitoring (CPU, battery).
- `wikipedia`: For Wikipedia summaries.
- `elevenlabs`: For advanced text-to-speech.
- `json`, `pickle`: For handling data files.

---

## Notes
- **ElevenLabs API**: The script uses ElevenLabs for text-to-speech by default. If you don’t have an API key, uncomment the `pyttsx3`-based code as a fallback (requires `pip install pyttsx3`).
- **Windows-Specific**: Some features (e.g., app opening/closing) use Windows paths (`C:\\Windows\\System32\\`). Modify for other operating systems if needed.
- **Error Handling**: The script includes basic error handling for API calls and speech recognition.
- **Model Training**: The script assumes a pre-trained model (`chat_model.h5`) and related files exist. Training these is beyond this README’s scope.

---

## Future Improvements
- Add support for more applications and websites.
- Implement multi-language support for speech recognition.
- Enhance intent recognition with a larger dataset.
- Add a GUI for visual interaction.
- Include persistent memory for context-aware responses.

---

## License
This project is for educational purposes only. Use responsibly and respect privacy and legal guidelines.

---

## Acknowledgments
- ElevenLabs for text-to-speech.
- NewsAPI and OpenWeatherMap for real-time data.
- TensorFlow for machine learning capabilities.
