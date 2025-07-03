import streamlit as st
import whisper
from whisper.utils import get_writer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import io
import tempfile
import os

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
    st.success("✅ File uploaded successfully!")

    if st.button("Generate Subtitles & Titles"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            tmp_audio.write(audio_file.read())
            tmp_audio_path = tmp_audio.name

        try:
            # Transcription in English
            result = whisper_model.transcribe(tmp_audio_path, language="en")
            transcript = result["text"]

            if not transcript.strip():
                st.error("❌ No speech detected in the audio.")
            else:
                # Save subtitles to string buffer
                srt_buffer = io.StringIO()
                writer = get_writer("srt", ".")
                writer.write_result(result, srt_buffer)
                srt_content = srt_buffer.getvalue()

                st.success("✅ Subtitles generated!")

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

                # Subtitles download button
                st.markdown("### 📄 Download Subtitles (.srt):")
                st.download_button("📥 Download .srt file", srt_content, file_name="subtitles.srt")

                # Show titles
                st.markdown("### 📝 Generated Video Titles:")
                for i, title in enumerate(titles, 1):
                    st.write(f"{i}. {title}")

        finally:
            # Ensure file is removed even if errors occur
            if os.path.exists(tmp_audio_path):
                os.remove(tmp_audio_path)
