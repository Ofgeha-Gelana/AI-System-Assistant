import os
import requests
import pyttsx3
from datetime import datetime
from google import genai
from google.genai.types import GenerateContentConfig

# API setup
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini client setup
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-2.0-flash"

def get_weather(city: str) -> dict:
    """
    Fetches current weather data for a given city.

    Args:
        city (str): The city name (e.g., "London").

    Returns:
        dict: Weather info (temp in Celsius, description), or fallback if API fails.
    """
    try:
        url = f"{WEATHER_API_URL}?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"]
            }
        else:
            return {"temp": 20, "description": "clear skies"}
    except Exception:
        return {"temp": 20, "description": "clear skies"}

def generate_weather_story(weather: dict) -> str:
    """
    Uses Gemini to generate a short story based on the weather.

    Args:
        weather (dict): Weather data with temp and description.

    Returns:
        str: A creative weather-based story.
    """
    prompt = f"Write a short, imaginative 2-sentence story about a day with {weather['description']} and a temperature of {weather['temp']}°C."
    config = GenerateContentConfig(
        system_instruction="You are a creative storyteller who turns weather into fun narratives."
    )
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            config=config,
            contents=prompt
        )
        return response.text.strip()
    except Exception:
        return f"The {weather['description']} draped the land in mystery, as {weather['temp']}°C whispered secrets to the wind."

def save_story(story: str, filename: str = "weather_tales.txt") -> None:
    """
    Saves the weather story to a file with a timestamp.

    Args:
        story (str): The story to save.
        filename (str): The file to append the story to.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {story}\n"
    with open(filename, "a") as file:
        file.write(entry)
    print(f"Story saved to {filename}")

def set_volume(level: int) -> None:
    """
    Sets the system volume using pactl (Linux-specific).

    Args:
        level (int): Volume level in percentage (0-100).
    """
    try:
        os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")
        print(f"Volume set to {level}%")
    except Exception:
        print("Volume adjustment skipped.")

def tell_story(story: str) -> None:
    """
    Reads the weather story aloud using text-to-speech.

    Args:
        story (str): The story to read aloud.
    """
    try:
        tts = pyttsx3.init()
        tts.setProperty("rate", 140)  # Slightly slower for dramatic effect
        tts.say("Here’s today’s weather tale:")
        tts.say(story)
        tts.runAndWait()
    except Exception:
        print("Text-to-speech failed. Here’s the story:", story)

def weather_storyteller(city: str) -> None:
    """
    Orchestrates the weather storytelling process.

    Args:
        city (str): The city to fetch weather for.
    """
    # Fetch weather
    weather = get_weather(city)
    print(f"Weather in {city}: {weather['temp']}°C, {weather['description']}")

    # Generate a story with Gemini
    story = generate_weather_story(weather)
    print(f"Story: {story}")

    # Save the story
    save_story(story)

    # Set volume
    set_volume(60)

    # Tell the story aloud
    tell_story(story)

# Run it
if __name__ == "__main__":
    weather_storyteller("New York")