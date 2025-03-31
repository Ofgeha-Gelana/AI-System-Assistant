# import streamlit as st
# import os
# import random
# import requests
# from datetime import datetime
# from gtts import gTTS
# from io import BytesIO
# import speech_recognition as sr
# import google.generativeai as genai

# # --- App Config ---
# st.set_page_config(
#     page_title="Joke Master 3000 (Gemini)",
#     page_icon="🤖",
#     layout="wide"
# )

# # --- Session State ---
# if 'joke_history' not in st.session_state:
#     st.session_state.joke_history = []

# # --- Gemini Setup ---
# # genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY")))
# # model = genai.GenerativeModel('gemini-1.5-flash')

# #
# api_key = os.getenv("GEMINI_API_KEY")
# client = genai.Client(api_key=api_key)
 
# # Define the model you are going to use
# model =  "gemini-2.0-flash"

# # --- Audio Functions ---
# def text_to_speech(text):
#     """Convert text to speech and play it"""
#     tts = gTTS(text=text, lang='en')
#     audio_bytes = BytesIO()
#     tts.write_to_fp(audio_bytes)
#     return audio_bytes

# def recognize_speech():
#     """Listen to user voice input"""
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Speak now...")
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio)
#             return text
#         except Exception as e:
#             st.error(f"Couldn't understand: {e}")
#             return None

# # --- Joke Functions ---
# def get_dad_joke():
#     """Fetch a random dad joke"""
#     response = requests.get(
#         "https://icanhazdadjoke.com/",
#         headers={"Accept": "text/plain"}
#     )
#     return response.text if response.status_code == 200 else "Why did the joke fail? It didn't GET a response!"

# def roast_me():
#     """Generate a hilarious roast using Gemini"""
#     response = model.generate_content(
#         "Generate a short, funny roast about someone who asked to be roasted. "
#         "Keep it PG-13 and clever. Maximum 2 sentences."
#     )
#     return response.text

# def ai_improv_joke(topic):
#     """Generate an AI-powered joke about any topic"""
#     response = model.generate_content(
#         f"Create a very short, funny joke about {topic}. "
#         "Maximum 2 sentences. Be creative!"
#     )
#     return response.text

# def joke_battle(user_joke):
#     """Battle the AI with jokes"""
#     bot_joke = ai_improv_joke("programming")
#     st.session_state.joke_history.append(f"👨‍💻 You: {user_joke}")
#     st.session_state.joke_history.append(f"🤖 Bot: {bot_joke}")
    
#     # Let Gemini judge who won!
#     judge_prompt = f"""
#     User's joke: "{user_joke}"
#     AI's joke: "{bot_joke}"
    
#     Which joke is funnier? Respond ONLY with either "USER" or "AI" 
#     and a very short (3-5 word) reason why.
#     """
    
#     judge_response = model.generate_content(judge_prompt)
#     decision = judge_response.text.split("\n")[0]
#     st.session_state.joke_history.append(f"🏆 {decision}")
#     return decision

# # --- UI Components ---
# def render_joke_history():
#     """Display joke history in an expandable section"""
#     with st.expander("📜 Joke History", expanded=False):
#         for joke in st.session_state.joke_history[-5:][::-1]:  # Show last 5, newest first
#             st.write(joke)

# def voice_input_button():
#     """Button to trigger voice input"""
#     if st.button("🎤 Use Voice Input"):
#         user_input = recognize_speech()
#         if user_input:
#             st.session_state.voice_input = user_input
#             return user_input
#     return ""

# # --- Main App ---
# def main():
#     st.title("🎤 Joke Master 3000 (Gemini)")
#     st.markdown("### The AI-Powered Comedy Experience 🤖😂")

#     # Sidebar for settings
#     with st.sidebar:
#         st.header("Settings")
#         auto_tts = st.checkbox("🔊 Auto Text-to-Speech", True)
#         st.markdown("---")
#         st.markdown("### Try these commands:")
#         st.code('"Tell me a dad joke"')
#         st.code('"Roast me!"')
#         st.code('"Make a joke about cats"')
#         st.code('"Let\'s battle with jokes"')

#     # Main content area
#     col1, col2 = st.columns([3, 1])

#     with col1:
#         # Input methods
#         user_input = st.text_input(
#             "How can I make you laugh today?",
#             value=st.session_state.get("voice_input", ""),
#             placeholder="Try: 'Tell me a joke about dogs' or 'Roast me!'"
#         )
        
#         # Add voice input option
#         voice_text = voice_input_button()
#         if voice_text:
#             user_input = voice_text

#         # Action buttons
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             if st.button("🤣 Random Joke"):
#                 user_input = "Tell me a random joke"
#         with col2:
#             if st.button("🔥 Roast Me"):
#                 user_input = "Roast me!"
#         with col3:
#             if st.button("🤺 Joke Battle"):
#                 user_input = "Let's battle with jokes"
#         with col4:
#             if st.button("🧔 Dad Joke"):
#                 user_input = "Tell me a dad joke"

#         # Process input
#         if user_input:
#             if "roast" in user_input.lower():
#                 joke = roast_me()
#                 st.error(joke)  # Roasts appear in red for effect
#             elif "battle" in user_input.lower():
#                 battle_input = st.text_input("Tell your joke first:")
#                 if battle_input:
#                     result = joke_battle(battle_input)
#                     st.success(result)
#             elif "dad joke" in user_input.lower():
#                 joke = get_dad_joke()
#                 st.success(joke)
#             elif "joke about" in user_input.lower():
#                 topic = user_input.split("about")[-1].strip()
#                 joke = ai_improv_joke(topic)
#                 st.success(joke)
#             else:
#                 # Let Gemini handle generic requests
#                 response = model.generate_content(
#                     f"User asked: '{user_input}'. Respond with a funny joke or humorous response."
#                 )
#                 joke = response.text
#                 st.success(joke)

#             # Add to history and play audio
#             st.session_state.joke_history.append(joke)
#             if auto_tts:
#                 audio_bytes = text_to_speech(joke)
#                 st.audio(audio_bytes, format='audio/mp3')

#     with col2:
#         st.image("https://i.imgur.com/V7yzU1r.png", width=150)  # Robot comedian image
#         st.markdown("### My Comedy Styles")
#         st.button("🤖 Tech Jokes")
#         st.button("🐶 Animal Jokes")
#         st.button("🍔 Food Jokes")
#         st.button("🎭 Dark Humor")

#     # Display joke history
#     render_joke_history()

#     # Easter egg
#     if st.session_state.get("joke_history") and len(st.session_state.joke_history) % 5 == 0:
#         st.balloons()

# if __name__ == "__main__":
#     main()




# import streamlit as st
# import os
# import random
# import requests
# from datetime import datetime
# from gtts import gTTS
# from io import BytesIO
# import speech_recognition as sr
# import google.generativeai as genai

# # --- App Config ---
# st.set_page_config(
#     page_title="Joke Master 3000 (Gemini)",
#     page_icon="🤖",
#     layout="wide"
# )

# # --- Session State ---
# if 'joke_history' not in st.session_state:
#     st.session_state.joke_history = []

# # --- Gemini Setup ---
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# # --- Audio Functions ---
# def text_to_speech(text):
#     """Convert text to speech and play it"""
#     tts = gTTS(text=text, lang='en')
#     audio_bytes = BytesIO()
#     tts.write_to_fp(audio_bytes)
#     return audio_bytes

# def recognize_speech():
#     """Listen to user voice input"""
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("Speak now...")
#         audio = r.listen(source)
#         try:
#             text = r.recognize_google(audio)
#             return text
#         except Exception as e:
#             st.error(f"Couldn't understand: {e}")
#             return None

# # --- Joke Functions ---
# def get_dad_joke():
#     """Fetch a random dad joke"""
#     response = requests.get(
#         "https://icanhazdadjoke.com/",
#         headers={"Accept": "text/plain"}
#     )
#     return response.text if response.status_code == 200 else "Why did the joke fail? It didn't GET a response!"

# def roast_me():
#     """Generate a hilarious roast using Gemini"""
#     response = model.generate_content("Generate a short, funny roast. Keep it PG-13 and clever.")
#     return response.text

# def ai_improv_joke(topic):
#     """Generate an AI-powered joke about any topic"""
#     response = model.generate_content(f"Create a short, funny joke about {topic}.")
#     return response.text

# def joke_battle(user_joke):
#     """Battle the AI with jokes"""
#     bot_joke = ai_improv_joke("programming")
#     st.session_state.joke_history.append(f"👨‍💻 You: {user_joke}")
#     st.session_state.joke_history.append(f"🤖 Bot: {bot_joke}")
    
#     judge_prompt = f"""
#     User's joke: "{user_joke}"
#     AI's joke: "{bot_joke}"
#     Which joke is funnier? Respond with "USER" or "AI" and a short reason.
#     """
    
#     judge_response = model.generate_content(judge_prompt)
#     decision = judge_response.text.split("\n")[0]
#     st.session_state.joke_history.append(f"🏆 {decision}")
#     return decision

# # --- UI Components ---
# def render_joke_history():
#     """Display joke history"""
#     with st.expander("📜 Joke History", expanded=False):
#         for joke in st.session_state.joke_history[-5:][::-1]:
#             st.write(joke)

# def voice_input_button():
#     """Button to trigger voice input"""
#     if st.button("🎤 Use Voice Input"):
#         user_input = recognize_speech()
#         if user_input:
#             st.session_state.voice_input = user_input
#             return user_input
#     return ""

# # --- Main App ---
# def main():
#     st.title("🎤 Joke Master 3000 (Gemini)")
#     st.markdown("### The AI-Powered Comedy Experience 🤖😂")

#     # Sidebar settings
#     with st.sidebar:
#         st.header("Settings")
#         auto_tts = st.checkbox("🎧 Auto Text-to-Speech", True)
#         st.markdown("---")
#         st.markdown("### Try these commands:")
#         st.code('"Tell me a dad joke"')
#         st.code('"Roast me!"')
#         st.code('"Make a joke about cats"')
#         st.code('"Let\'s battle with jokes"')

#     # Input area
#     user_input = st.text_input(
#         "How can I make you laugh today?",
#         value=st.session_state.get("voice_input", ""),
#         placeholder="Try: 'Tell me a joke about dogs' or 'Roast me!'"
#     )
    
#     # Voice input option
#     voice_text = voice_input_button()
#     if voice_text:
#         user_input = voice_text

#     # Buttons for quick actions
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         if st.button("🤣 Random Joke"):
#             user_input = "Tell me a random joke"
#     with col2:
#         if st.button("🔥 Roast Me"):
#             user_input = "Roast me!"
#     with col3:
#         if st.button("🫃 Joke Battle"):
#             user_input = "Let's battle with jokes"
#     with col4:
#         if st.button("🧔 Dad Joke"):
#             user_input = "Tell me a dad joke"

#     # Process user input
#     if user_input:
#         if "roast" in user_input.lower():
#             joke = roast_me()
#             st.error(joke)
#         elif "battle" in user_input.lower():
#             battle_input = st.text_input("Tell your joke first:")
#             if battle_input:
#                 result = joke_battle(battle_input)
#                 st.success(result)
#         elif "dad joke" in user_input.lower():
#             joke = get_dad_joke()
#             st.success(joke)
#         elif "joke about" in user_input.lower():
#             topic = user_input.split("about")[-1].strip()
#             joke = ai_improv_joke(topic)
#             st.success(joke)
#         else:
#             response = model.generate_content(f"User asked: '{user_input}'. Respond with a joke.")
#             joke = response.text
#             st.success(joke)

#         st.session_state.joke_history.append(joke)
#         if auto_tts:
#             audio_bytes = text_to_speech(joke)
#             st.audio(audio_bytes, format='audio/mp3')

#     render_joke_history()
#     if len(st.session_state.joke_history) % 5 == 0:
#         st.balloons()

# if __name__ == "__main__":
#     main()





# import streamlit as st
# import os
# import random
# import requests
# from datetime import datetime
# from gtts import gTTS
# from io import BytesIO
# import speech_recognition as sr
# import google.generativeai as genai
# from google.generativeai.types import GenerateContentConfig

# # --- App Config ---
# st.set_page_config(
#     page_title="Joke Master 3000 (Gemini FC)",
#     page_icon="🤖",
#     layout="wide"
# )

# # --- Session State ---
# if 'joke_history' not in st.session_state:
#     st.session_state.joke_history = []

# # --- Gemini Setup with Function Calling ---
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Define our tools (functions Gemini can call)
# def get_dad_joke(category: str = "Any") -> str:
#     """Fetches a random dad joke from icanhazdadjoke.com"""
#     response = requests.get(
#         "https://icanhazdadjoke.com/",
#         headers={"Accept": "text/plain"}
#     )
#     return response.text if response.status_code == 200 else "Why did the joke fail? It didn't GET a response!"

# def roast_me(intensity: str = "medium") -> str:
#     """Generates a funny roast at specified intensity level (mild, medium, spicy)"""
#     roasts = {
#         "mild": [
#             "You're like a cloud—when you disappear, it's a beautiful day.",
#             "If laughter is the best medicine, your face must be curing the world."
#         ],
#         "medium": [
#             "You're the human version of a '404 Error'.",
#             "I'd agree with you, but then we'd both be wrong."
#         ],
#         "spicy": [
#             "You're not stupid; you just have bad luck thinking.",
#             "You're the reason the gene pool needs a lifeguard."
#         ]
#     }
#     return random.choice(roasts.get(intensity, roasts["medium"]))

# def save_joke(joke: str, filename: str = "joke.txt") -> None:
#     """Saves a joke to a text file with timestamp"""
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with open(filename, "a") as file:
#         file.write(f"[{timestamp}]\n{joke}\n\n")
#     return f"Joke saved to {filename}"

# def tell_joke(filename: str = "joke.txt") -> str:
#     """Reads the joke aloud using text-to-speech"""
#     try:
#         with open(filename, "r") as file:
#             joke = file.read()
        
#         tts = gTTS(text=joke, lang='en')
#         audio_bytes = BytesIO()
#         tts.write_to_fp(audio_bytes)
#         return "Joke read aloud successfully!"
#     except FileNotFoundError:
#         return "Couldn't find the joke file."

# def joke_battle(user_joke: str) -> str:
#     """Evaluates a joke battle between user and AI"""
#     bot_joke = get_dad_joke()
#     result = f"🤖 Bot's joke: {bot_joke}\n\n"
    
#     # Simple length-based scoring
#     if len(user_joke) > len(bot_joke):
#         result += "🏆 You win! Your joke was longer (and therefore funnier?)"
#     else:
#         result += "🏆 Bot wins! Its joke was longer (and therefore funnier?)"
    
#     return result

# # Configure Gemini with our functions
# tools = [get_dad_joke, roast_me, save_joke, tell_joke, joke_battle]

# config = GenerateContentConfig(
#     system_instruction="You are Jokey, a hilarious AI comedian. Use the provided tools to deliver jokes, roasts, and comedy battles. Be playful and fun!",
#     tools=tools
# )

# model = genai.GenerativeModel('gemini-1.5-flash', generation_config=config)

# # --- UI Components ---
# def render_joke_history():
#     """Displays joke history"""
#     with st.expander("📜 Joke History", expanded=False):
#         for joke in st.session_state.joke_history[-5:][::-1]:
#             st.write(joke)

# def voice_input_button():
#     """Button for voice input"""
#     if st.button("🎤 Use Voice Input"):
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             st.info("Speak now...")
#             audio = r.listen(source)
#             try:
#                 text = r.recognize_google(audio)
#                 st.session_state.voice_input = text
#                 return text
#             except Exception as e:
#                 st.error(f"Couldn't understand: {e}")
#                 return None
#     return ""

# # --- Main App ---
# def main():
#     st.title("🎤 Joke Master 3000 (Gemini FC)")
#     st.markdown("### The Function-Calling Comedy Experience 🤖😂")

#     # Sidebar settings
#     with st.sidebar:
#         st.header("Settings")
#         auto_tts = st.checkbox("🔊 Auto Text-to-Speech", True)
#         st.markdown("---")
#         st.markdown("### Try these commands:")
#         st.code('"Tell me a dad joke"')
#         st.code('"Roast me with medium intensity"')
#         st.code('"Save a joke about cats"')
#         st.code('"Let\'s battle with jokes"')

#     # Main content
#     col1, col2 = st.columns([3, 1])

#     with col1:
#         # Input methods
#         user_input = st.text_input(
#             "How can I make you laugh today?",
#             value=st.session_state.get("voice_input", ""),
#             placeholder="Try: 'Tell me a joke and save it' or 'Roast me hard!'"
#         )
        
#         # Voice input
#         voice_text = voice_input_button()
#         if voice_text:
#             user_input = voice_text

#         # Quick action buttons
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             if st.button("🤣 Random Joke"):
#                 user_input = "Tell me a random joke"
#         with col2:
#             if st.button("🔥 Roast Me"):
#                 user_input = "Roast me with medium intensity"
#         with col3:
#             if st.button("🤺 Joke Battle"):
#                 user_input = "Let's battle with jokes"
#         with col4:
#             if st.button("💾 Save Joke"):
#                 user_input = "Tell me a joke and save it to jokes.txt"

#         # Process input through Gemini with function calling
#         if user_input:
#             response = model.generate_content(user_input)
            
#             # Handle function calls if any
#             if response.candidates and response.candidates[0].content.parts:
#                 result = response.text
                
#                 # If Gemini called a function, execute it
#                 if hasattr(response.candidates[0].content, 'function_call'):
#                     func_name = response.candidates[0].content.function_call.name
#                     args = response.candidates[0].content.function_call.args
                    
#                     # Map function names to our actual functions
#                     func_map = {
#                         "get_dad_joke": get_dad_joke,
#                         "roast_me": roast_me,
#                         "save_joke": save_joke,
#                         "tell_joke": tell_joke,
#                         "joke_battle": joke_battle
#                     }
                    
#                     if func_name in func_map:
#                         try:
#                             # Call the function with provided arguments
#                             func_result = func_map[func_name](**args)
#                             result = f"{result}\n\n{func_result}"
#                         except Exception as e:
#                             result = f"Error executing function: {str(e)}"
                
#                 st.session_state.joke_history.append(result)
#                 st.success(result)
                
#                 # Auto text-to-speech
#                 if auto_tts:
#                     tts = gTTS(text=result, lang='en')
#                     audio_bytes = BytesIO()
#                     tts.write_to_fp(audio_bytes)
#                     st.audio(audio_bytes, format='audio/mp3')

#     with col2:
#         st.image("https://i.imgur.com/V7yzU1r.png", width=150)
#         st.markdown("### Comedy Tools")
#         st.button("🤖 Tech Jokes")
#         st.button("🐶 Animal Jokes")
#         st.button("🍔 Food Jokes")
#         st.button("🎭 Dark Humor")

#     # Display history
#     render_joke_history()

#     # Easter egg
#     if len(st.session_state.joke_history) % 5 == 0 and len(st.session_state.joke_history) > 0:
#         st.balloons()

# if __name__ == "__main__":
#     main()




import streamlit as st
import os
import requests
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai

# --- App Config ---
st.set_page_config(
    page_title="Joke Master 3000 (Gemini)",
    page_icon="🤖",
    layout="wide"
)

# --- Session State ---
if 'joke_history' not in st.session_state:
    st.session_state.joke_history = []

# --- Gemini Setup ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

JOKE_API_URL = "https://v2.jokeapi.dev/joke/"

def get_joke(category: str) -> str:
    """
    Fetches a joke from the API based on the selected category.
    """
    url = f"{JOKE_API_URL}{category}?type=twopart"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{data['setup']} ... {data['delivery']}"
    else:
        return "Oops! Couldn't fetch a joke."

def save_joke(joke: str, filename: str) -> None:
    """Saves the joke to a text file."""
    with open(filename, "w") as file:
        file.write(joke)

def tell_joke(filename: str) -> None:
    """Reads the joke aloud using text-to-speech (TTS)."""
    with open(filename, "r") as file:
        joke = file.read()
    tts = pyttsx3.init()
    tts.say("Here is a joke for you!   ")
    tts.say(joke)
    tts.runAndWait()

def recognize_speech():
    """Listen to user voice input"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except Exception as e:
            st.error(f"Couldn't understand: {e}")
            return None

# Configure Gemini to use functions
tools = [get_joke, save_joke, tell_joke]

def process_with_gemini(user_request: str):
    response = model.generate_content(
        contents=user_request
    )
    return response.text

def main():
    st.title("🎤 Joke Master 3000 (Gemini)")
    st.markdown("### The AI-Powered Comedy Experience 🤖😂")

    user_input = st.text_input("Ask me for a joke!", "Tell me a joke about programming")
    
    if st.button("🤣 Get Joke"):
        response = process_with_gemini(user_input)
        st.session_state.joke_history.append(response)
        st.success(response)
        save_joke(response, "joke.txt")
        tell_joke("joke.txt")

    if st.button("🎤 Use Voice Input"):
        voice_text = recognize_speech()
        if voice_text:
            response = process_with_gemini(voice_text)
            st.session_state.joke_history.append(response)
            st.success(response)
            save_joke(response, "joke.txt")
            tell_joke("joke.txt")

    with st.expander("📜 Joke History", expanded=False):
        for joke in st.session_state.joke_history[-5:][::-1]:
            st.write(joke)

if __name__ == "__main__":
    main()
