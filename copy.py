import os
import requests
import pyttsx3

JOKE_API_URL = "https://v2.jokeapi.dev/joke/"

def get_joke(category: str) -> str:
    """
    Fetches a joke from the API based on the selected category.

    Args:
        category (str): The category of the joke (e.g., 'Programming', 'Pun').

    Returns:
        str: The joke in the format "Setup ... Delivery".
    """
    url = f"{JOKE_API_URL}{category}?type=twopart"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return f"{data['setup']} ... {data['delivery']}"
    else:
        return "Oops! Couldn't fetch a joke."
    
get_joke("programming")




def save_joke(joke: str, filename: str) -> None:
    """
    Saves the joke to a text file.

    Args:
        joke (str): The joke text.
        filename (str): The name of the file to save the joke in. Default is 'joke.txt'.
    """
    with open(filename, "w") as file:
        file.write(joke)
    print(f"Joke saved to {filename}")

save_joke("This is a joke", "joke.txt")



def set_volume(level: int) -> None:
    """
    Sets the system volume using pactl.
    
    Args:
        level (int): Volume level in percentage (0-100).
    """
    os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")
    print(f"Volume set to {level}%")



set_volume(45)

def tell_joke(filename: str) -> None:
    """
    Reads the joke aloud using text-to-speech (TTS).

    Args:
        filename (str): The file from which the joke will be read. Default is 'joke.txt'.
    """
    with open(filename, "r") as file:
        joke = file.read()

    tts = pyttsx3.init()
    tts.say("Here is a joke for you!   ")
    tts.say(joke)
    tts.runAndWait()


tell_joke("joke.txt")

from google.genai.types import GenerateContentConfig

from google import genai
 
# create client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
 
# Define the model you are going to use
model_id =  "gemini-2.0-flash"




 
# Generation Config
config = GenerateContentConfig(
    system_instruction="You are a helpful assistant that use tools to provide jokes to the user", # to give the LLM context.
    tools=[get_joke, save_joke, set_volume, tell_joke, ], # define the functions that the LLM can use
)



r = client.models.generate_content(
    model=model_id,
    config=config,
    contents='tell me a joke about programming, and save it in a file named "joke.txt", then read it aloud'
)

# set the volume "50" percent
# tell me a joke about programming
# tell me a joke about programming, and save it in a file named "joke.txt", then read it aloud


print(r.text)