import os

# Set FFmpeg binary path manually if not in system PATH
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

import streamlit as st
import whisper
from whisper.utils import get_writer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import subprocess

# Check FFmpeg availability
try:
    subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
except FileNotFoundError:
    st.error("FFmpeg not found! Please install FFmpeg and add it to your system PATH.")

# Load models
@st.cache_resource
def load_models():
    whisper_model = whisper.load_model("base")
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
    title_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
    return whisper_model, tokenizer, title_model

whisper_model, tokenizer, title_model = load_models()

st.title("🎙️ Audio to Subtitle & Title Generator")

# Upload audio file
audio_file = st.file_uploader("Upload your audio file (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    with open(audio_file.name, "wb") as f:
        f.write(audio_file.read())

    st.success("✅ File uploaded successfully!")

    if st.button("Generate Subtitles & Titles"):
        # Load audio and check for empty content
        audio = whisper.load_audio(audio_file.name)
        if len(audio) == 0:
            st.error("❌ The uploaded audio file is empty. Please upload a valid audio.")
        else:
            # Transcription in English
            result = whisper_model.transcribe(audio_file.name, language="en")
            transcript = result["text"]

            # Save subtitles (.srt)
            srt_path = "subtitles.srt"
            with open(srt_path, "w", encoding="utf-8") as f:
                writer = get_writer("srt", ".")
                writer.write_result(result, f)

            st.success("Subtitles generated!")

            # Title generation
            prompt = f"Generate 5 engaging YouTube video titles for this video transcript:\n\n{transcript}\n\nTitles:"
            inputs = tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True)
            outputs = title_model.generate(
                **inputs,
                max_length=30,
                num_return_sequences=5,
                do_sample=True,
                temperature=0.9,
                top_p=0.95,
                top_k=50,
                early_stopping=True
            )
            titles = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

            # Subtitles download
            st.markdown("### Generated Subtitles (.srt):")
            with open(srt_path, "rb") as f:
                st.download_button("Download .srt file", f, file_name="subtitles.srt")

            # Show titles
            st.markdown("### Generated Video Titles:")
            for i, title in enumerate(titles, 1):
                st.write(f"{i}. {title}")

            # Clean up temp files
            os.remove(audio_file.name)
            os.remove(srt_path)
