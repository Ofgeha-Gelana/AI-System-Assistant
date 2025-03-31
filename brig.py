# def set_brightness(percentage):
#     """
#     Adjust screen brightness on Ubuntu by percentage (0-100)
    
#     Args:
#         percentage (int): Desired brightness level (0-100)
    
#     Returns:
#         bool: True if successful, False if failed
#     """
#     try:
#         # Validate input
#         if not 0 <= percentage <= 100:
#             raise ValueError("Brightness must be between 0 and 100")

#         # Common path for backlight control (might vary by hardware)
#         backlight_path = "/sys/class/backlight/intel_backlight/"
        
#         # Some systems might use different backlight drivers
#         import os
#         if not os.path.exists(backlight_path):
#             # Try AMD GPU path
#             backlight_path = "/sys/class/backlight/amdgpu_bl0/"
        
#         if not os.path.exists(backlight_path):
#             print("Could not find backlight control path")
#             return False

#         # Get maximum brightness value
#         with open(f"{backlight_path}max_brightness", "r") as f:
#             max_brightness = int(f.read().strip())

#         # Calculate target brightness
#         target_brightness = int((percentage / 100) * max_brightness)

#         # Set brightness
#         with open(f"{backlight_path}brightness", "w") as f:
#             f.write(str(target_brightness))

#         return True

#     except PermissionError:
#         print("Permission denied: Try running with sudo")
#         return False
#     except FileNotFoundError:
#         print("Backlight control files not found - hardware may not support this method")
#         return False
#     except Exception as e:
#         print(f"Error setting brightness: {str(e)}")
#         return False

# # Example usage
# if __name__ == "__main__":
#     # Set brightness to 75%
#     success = set_brightness(10)
#     if success:
#         print("Brightness adjusted successfully")





import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",
    layout="centered",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-flash')

# Brightness control functions
def set_brightness(percentage):
    """
    Adjust screen brightness on Ubuntu by percentage (0-100)
    """
    try:
        if not 0 <= percentage <= 100:
            raise ValueError("Brightness must be between 0 and 100")

        backlight_path = "/sys/class/backlight/intel_backlight/"
        if not os.path.exists(backlight_path):
            backlight_path = "/sys/class/backlight/amdgpu_bl0/"
        
        if not os.path.exists(backlight_path):
            return "Could not find backlight control path", False

        with open(f"{backlight_path}max_brightness", "r") as f:
            max_brightness = int(f.read().strip())

        target_brightness = int((percentage / 100) * max_brightness)
        with open(f"{backlight_path}brightness", "w") as f:
            f.write(str(target_brightness))
        
        return f"Brightness set to {percentage}%", True
    
    except PermissionError:
        return "Permission denied: Run with sudo", False
    except Exception as e:
        return f"Error: {str(e)}", False

def get_current_brightness():
    try:
        backlight_path = "/sys/class/backlight/intel_backlight/"
        if not os.path.exists(backlight_path):
            backlight_path = "/sys/class/backlight/amdgpu_bl0/"
        
        if not os.path.exists(backlight_path):
            return 50  # Default fallback

        with open(f"{backlight_path}max_brightness", "r") as f:
            max_brightness = int(f.read().strip())
        with open(f"{backlight_path}brightness", "r") as f:
            current = int(f.read().strip())
        
        return int((current / max_brightness) * 100)
    except:
        return 50  # Fallback value

# Command handler for brightness
def handle_brightness_command(prompt):
    current_brightness = get_current_brightness()
    
    if "increase brightness" in prompt.lower():
        new_brightness = min(current_brightness + 10, 100)
        msg, success = set_brightness(new_brightness)
        return msg if success else f"Failed: {msg}"
    
    elif "decrease brightness" in prompt.lower():
        new_brightness = max(current_brightness - 10, 0)
        msg, success = set_brightness(new_brightness)
        return msg if success else f"Failed: {msg}"
    
    return None

# Translate roles for Streamlit
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display title
st.title("🤖 Gemini Pro - ChatBot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro... (Try 'increase brightness' or 'decrease brightness')")
if user_prompt:
    # Add user's message to chat
    st.chat_message("user").markdown(user_prompt)

    # Check for brightness commands
    brightness_response = handle_brightness_command(user_prompt)
    if brightness_response:
        with st.chat_message("assistant"):
            st.markdown(brightness_response)
    else:
        # Fallback to Gemini-Pro response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# Sidebar note
st.sidebar.markdown("**Note:** If brightness adjustments fail, run with `sudo streamlit run script.py`")