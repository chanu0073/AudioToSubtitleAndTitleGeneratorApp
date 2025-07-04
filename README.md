# 🎙️ Audio To Subtitle And Title Generator App

A Streamlit web app that transcribes audio files into subtitles and generates engaging video titles using Generative AI models. Built with Whisper (OpenAI) for transcription and FLAN-T5 for title generation via HuggingFace Transformers.

---

## 📌 Features

- 🎧 **Upload audio files** (`.mp3`, `.wav`, `.m4a`)
- 📑 **Generate subtitles (.srt format)** using Whisper
- 📝 **Generate 5 creative video titles** based on the audio transcription
- ⏳ **Progress bar** while processing
- 📥 **Download the generated subtitles**
- 🎛️ Clean and intuitive **Streamlit web UI**

---

## 🚀 How to Run Locally

1️⃣ **Clone the repository**
git clone https://github.com/chanu0073/AudioToSubtitleAndTitleGeneratorApp.git

cd AudioToSubtitleAndTitleGeneratorApp

2️⃣ Create and activate a virtual environment

python -m venv venv

venv\Scripts\activate    # On Windows

or

source venv/bin/activate # On Mac/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Streamlit app
streamlit run app.py

Development Container Support:

This project includes a .devcontainer/ folder for optional use with VS Code Remote Containers or GitHub Codespaces.
It ensures a consistent Python 3.11 environment, automatically installs dependencies, and runs the Streamlit app on container startup.
If you're using VS Code, you can simply "Reopen in Container" to get started.

📄 Sample Files
Check out the sample_files/ folder:

test_audio.mp3 — A sample audio file for quick testing.

test_audio_subtitles.srt — Subtitles generated for the sample audio.

You can try running the app with this file to instantly see how it works.

📦 Dependencies

streamlit

openai-whisper

transformers

torch

ffmpeg (must be available in system PATH)


Install them via:

pip install -r requirements.txt

🌐 Deployment

The app is deployed on Streamlit Community Cloud.

Visit: https://audiotosubtitleandtitlegeneratorapp-n8gpnjkugs5araesn7rap3.streamlit.app/

## 📌 Future Work

While the project successfully implements an Audio to Subtitle and Title Generator system using Whisper and FLAN-T5 models, there are several promising directions for future enhancement:

• Multi-language Transcription Support:
Extend the application to support transcription and title generation in multiple languages by integrating multilingual Whisper models and appropriate language-specific title generation models. This would make the application globally adaptable for diverse content creators.

• Enhanced Description Generation:
Currently, the application generates video titles based on the transcribed audio. Future versions could include the generation of detailed video descriptions and hashtags, making the tool more comprehensive for YouTube and general video content optimization.

• Phonetic and Translated Subtitle Options:
Add functionality to generate subtitles not just in the original language, but also translated into multiple target languages. Additionally, for each target language, provide a phonetic version of the subtitles which spells out how the original spoken words would sound in the target language script. This would greatly enhance accessibility for viewers who may not read the script but can follow phonetics in their native language.

📜 License
This project is open source and available under the MIT License.

✨ Acknowledgements
OpenAI Whisper : https://github.com/openai/whisper

HuggingFace Transformers : https://huggingface.co/docs/transformers/index

Streamlit : https://streamlit.io/

