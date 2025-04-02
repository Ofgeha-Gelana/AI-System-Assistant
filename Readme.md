# AI System Assistant

## 🚀 Overview
AI System Assistant is a smart AI-powered tool that helps manage system settings, launch applications, recommend music based on mood, and send SMS messages via an external API. It integrates **Google Gemini AI**, **Spotify API**, and **System Controls** to provide an interactive assistant.

## 🛠 Features
- **System Control**: Adjust brightness, volume, toggle Wi-Fi, enable/disable dark mode, and perform system operations (lock, shutdown, restart).
- **Application Launcher**: Open common applications like Chrome, VS Code, Spotify, and more.
- **Mood-Based Music Recommendation**: Uses text sentiment analysis to recommend Spotify playlists.
- **SMS Sending**: Sends SMS messages via a configurable SMS Gateway API.
- **Chat Interface**: Powered by **Streamlit**, enabling a dynamic user experience.

## 🏗 Tech Stack
- **Python**
- **Streamlit** (For interactive UI)
- **Spotipy** (Spotify API Integration)
- **TextBlob** (For sentiment analysis)
- **Google Gemini AI** (For AI interactions)
- **Requests** (For API calls)
- **Dotenv** (For environment variable management)

## 🔧 Installation
### Prerequisites
- Python 3.8+
- Pip
- A Spotify Developer Account (for API access)
- Google Gemini API Key

### Setup
1. Clone the repository:
   ```bash
   https://github.com/Ofgeha-Gelana/AI-System-Assistant.git
   cd AI-System-Assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your API keys:
   ```ini
   GEMINI_API_KEY=your_gemini_api_key
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 📡 Usage
- Open the Streamlit web interface.
- Type commands like:
  - **"Set brightness to 50%"**
  - **"Open Chrome"**
  - **"Play music for my mood"**
  - **"Send SMS to +251912345678: Hello!"**

## 📬 API Usage: Sending SMS
To send an SMS, the app makes a **POST request** to the SMS Gateway API.


```




---

🔹 **Developed with ❤️ by [Ofgeha]**
