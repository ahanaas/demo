import streamlit as st
import torch
from transformers     import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from rake_nltk import Rake
import matplotlib.pyplot as plt
import numpy as np
import io
import librosa

# Load Wav2Vec2 model and tokenizer for speech-to-text
model_name = "facebook/wav2vec2-large-960h"
tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)

def audio_to_text(audio_file):
    # Load audio file
    audio, sr = librosa.load(audio_file, sr=16000)
    # Convert audio to tensor
    input_values = tokenizer(audio, return_tensors="pt").input_values
    # Forward pass
    with torch.no_grad():
        logits = model(input_values).logits
    # Decode logits to text
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    return transcription

def extract_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases_with_scores()

def plot_keywords(keywords):
    # Extract top 5 keywords
    top_keywords = sorted(keywords, key=lambda x: x[1], reverse=True)[:5]
    phrases, scores = zip(*top_keywords)
    
    fig, ax = plt.subplots()
    ax.barh(phrases, scores, color='skyblue')
    ax.set_xlabel('Importance')
    ax.set_title('Top 5 Keywords')
    
    # Show plot in Streamlit
    st.pyplot(fig)

def main():
    st.title('Audio Keyword Detection System')

    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    
    if audio_file:
        st.audio(audio_file, format='audio/wav')
        
        # Convert audio to text
        with st.spinner("Converting audio to text..."):
            transcription = audio_to_text(audio_file)
            st.write("Transcription:", transcription)
        
        # Extract keywords
        st.spinner("Extracting keywords...")
        keywords = extract_keywords(transcription)
        
        if keywords:
            st.write("Keywords and their importance:")
            for phrase, score in keywords:
                st.write(f"- {phrase}: {score:.4f}")
            
            # Plot keywords
            plot_keywords(keywords)
        else:
            st.write("No keywords found.")

if __name__ == "__main__":
    main()
