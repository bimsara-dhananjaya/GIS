import streamlit as st
from gtts import gTTS
from io import BytesIO


def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)
    return audio_stream


st.title('Text-to-Speech App')

# Input text using a text area
input_text = st.text_area("Enter text:", "Hello, how are you?")

# Language and gender selection
language_options = {
    "English (Male)": "en-us",   # Male voice
    "English (Female)": "en-uk",  # Female voice
    "Spanish (Male)": "es-us",   # Male voice
    "Spanish (Female)": "es",     # Female voice
}

selected_language = st.selectbox(
    "Select language and gender:", list(language_options.keys()))

# Button to convert text to speech
if st.button("Convert to Speech"):
    language_code = language_options[selected_language]
    audio_stream = text_to_speech(input_text, language=language_code)
    st.audio(audio_stream, format="audio/mp3", start_time=0)

# Download button for the audio file
if st.button("Download as MP3"):
    language_code = language_options[selected_language]
    audio_stream = text_to_speech(input_text, language=language_code)
    st.download_button("Download", data=audio_stream.read(),
                       file_name="output.mp3", mime="audio/mp3")

# Note: The audio will be played when you click the "Convert to Speech" button, and you can download the generated MP3 file.
