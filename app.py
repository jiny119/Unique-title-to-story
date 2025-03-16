import streamlit as st
from transformers import pipeline
from gtts import gTTS
import os
import time
from pydub import AudioSegment
from pydub.playback import play

# ----- Streamlit UI -----
st.title("📖 Urdu Story Generator with Voiceover & Music")
story_title = st.text_input("Enter a Story Title:", "")

if st.button("Generate Story & Voiceover"):
    if not story_title:
        st.warning("Please enter a story title.")
    else:
        st.info("Generating story... Please wait!")

        # ----- Generate Story -----
        generator = pipeline("text-generation", model="facebook/opt-1.3b")
        story_prompt = f"Ek {story_title} par ek lambi kahani likho jo 30 minutes tak chale."
        story_text = generator(story_prompt, max_length=1024, do_sample=True)[0]['generated_text']
        
        # Display story
        st.subheader("Generated Story:")
        st.write(story_text)

        # ----- Convert to Voiceover -----
        tts = gTTS(text=story_text, lang="ur", slow=False)
        audio_file = "story.mp3"
        tts.save(audio_file)
        
        # ----- Add Background Music -----
        story_audio = AudioSegment.from_mp3(audio_file)
        background_music = AudioSegment.from_file("bg_music.mp3")  # Make sure to add a background music file

        final_audio = background_music.overlay(story_audio, position=0)
        final_audio.export("final_story.mp3", format="mp3")

        # Play and Download Option
        st.audio("final_story.mp3", format="audio/mp3")
        st.success("✅ Story & Voiceover Generated!")
        st.download_button("Download Story Audio", "final_story.mp3")
