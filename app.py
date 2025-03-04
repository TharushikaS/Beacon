import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading
import logging
import traceback
from llm import invoke_llm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceChatbot:
    def __init__(self):
        # Speech recognition setup
        self.listener = sr.Recognizer()
        
        # Thread lock for text-to-speech synchronization
        self.tts_lock = threading.Lock()
        
        # Streamlit configuration
        st.set_page_config(page_title="Voice Chatbot", page_icon="🤖")
        st.title("Voice Chatbot")
        
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

    def configure_voice(self, voice_id=1, rate=150):
        """Configure voice properties for text-to-speech."""
        with self.tts_lock:
            player = pyttsx3.init()
            voices = player.getProperty('voices')
            player.setProperty('voice', voices[voice_id].id)  # Select voice
            player.setProperty('rate', rate)  # Adjust speech rate
            return player

    def listen_voice(self):
        """Capture voice input using Google Speech Recognition."""
        try:
            with sr.Microphone() as input_device:
                st.info("Adjusting for ambient noise... Speak now")
                self.listener.adjust_for_ambient_noise(input_device, duration=1)
                
                audio = self.listener.listen(input_device, timeout=5, phrase_time_limit=5)
                text_command = self.listener.recognize_google(audio)
                
                st.success(f"Recognized: {text_command}")
                return text_command
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            st.error(f"Voice input error: {e}")
            logger.error(f"Voice input error: {traceback.format_exc()}")
            return None

    def speak_response(self, text):
        """Threaded text-to-speech to prevent blocking."""
        def _speak():
            try:
                # Create a new pyttsx3 instance for this thread
                player = self.configure_voice()
                player.say(text)
                player.runAndWait()
            except Exception as e:
                st.error(f"Speech error: {e}")
                logger.error(f"Speech error: {traceback.format_exc()}")
        
        # Run speech in a separate thread
        threading.Thread(target=_speak, daemon=True).start()

    def process_input(self, user_input):
        """Process user input and generate response."""
        if not user_input:
            return None

        try:
            # Generate LLM response with chat history
            response = invoke_llm(user_input, st.session_state.chat_history)
            
            # Update and display chat
            st.session_state.chat_history.append({
                "user": user_input, 
                "bot": response
            })
            
            # Speak response
            self.speak_response(response)
            
            return response
        except Exception as e:
            st.error(f"Processing error: {e}")
            logger.error(f"Processing error: {traceback.format_exc()}")
            return None

    def run(self):
        """Main Streamlit app interface."""
        # Sidebar for settings
        with st.sidebar:
            st.header("Settings")
            voice_id = st.selectbox("Select Voice", options=[0, 1], format_func=lambda x: "Male" if x == 0 else "Female")
            speech_rate = st.slider("Speech Rate", min_value=100, max_value=200, value=150)
            self.configure_voice(voice_id=voice_id, rate=speech_rate)

            if st.button("Clear Chat"):
                st.session_state.chat_history = []
                st.experimental_rerun()

        # Display chat history
        for chat in st.session_state.chat_history:
            st.chat_message("human").write(chat['user'])
            st.chat_message("assistant").write(chat['bot'])

        # Input section
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Voice Input"):
                voice_input = self.listen_voice()
                if voice_input:
                    self.process_input(voice_input)
        with col2:
            text_input = st.text_input("Type your message here...")
            if text_input:
                self.process_input(text_input)

def main():
    chatbot = VoiceChatbot()
    chatbot.run()

if __name__ == "__main__":
    main()