# Simple Audio Transcription CLI

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Powered by](https://img.shields.io/badge/Powered%20by-faster--whisper-orange)
![CUDA](https://img.shields.io/badge/GPU%20Support-CUDA-green?logo=nvidia)

A fast and easy-to-use Command Line Interface (CLI) application for transcribing audio files using the powerful [faster-whisper](https://github.com/SYSTRAN/faster-whisper) engine. It supports CPU and GPU processing, and handles transcription across dozens of languages.

## 🚀 Installation

1. **Download the project** to your computer.
2. **Install the dependencies**:
   Ensure you have Python installed, then open your terminal in the project folder and run:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: For the best performance on an NVIDIA GPU, ensure your environment has CUDA/PyTorch set up).*

## 📖 How to Use

> **Note**: This application uses a strict folder structure to keep things organized. 
> - 📥 Place your input media inside the **`Audio/`** folder.
> - 📤 Your final transcripts will be saved in the **`Result/`** folder.
> - 🧠 AI models are stored in the **`Model/`** folder. (model will be downloaded automatically, you dont need to download the model manually)

1. **Prepare your audio**: 
   Place the audio or video file you want to transcribe (e.g., `presentation.m4a`, `audio.mp3`) inside the `Audio/` folder.
2. **Run the app**:
   Open your terminal in the project folder and start the script:
   ```bash
   python main.py
   ```
3. **Follow the prompts**:
   - **Audio File**: Type the name of your file (e.g., `presentation.m4a`).
   - **Model**: Choose the transcription accuracy/speed (The default `Turbo` model is highly recommended).
   - **Device**: Select Auto, GPU, or CPU processing.
   - **Language**: Choose the spoken language, or leave it on Auto-detect.
   - **Output**: Choose a name for your final transcript file.
4. **Get your results**:
   Once the transcription finishes, your text file will be saved securely inside the `Result/` folder!
