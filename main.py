import os
import sys

# Workaround for CTranslate2 missing CUDA 12 libraries on Windows
if os.name == "nt":
    import importlib.util
    torch_spec = importlib.util.find_spec("torch")
    if torch_spec and torch_spec.submodule_search_locations:
        torch_lib_path = os.path.join(torch_spec.submodule_search_locations[0], "lib")
        if os.path.exists(torch_lib_path):
            os.environ["PATH"] = torch_lib_path + os.pathsep + os.environ.get("PATH", "")
            os.add_dll_directory(torch_lib_path)

from faster_whisper import WhisperModel
from faster_whisper.tokenizer import _LANGUAGE_CODES
import time
# ==========================
# Available Models
# ==========================
MODELS = {
    "1": ("tiny", "Fastest, Lowest Accuracy"),
    "2": ("base", "Fast"),
    "3": ("small", "Good"),
    "4": ("medium", "Very Good"),
    "5": ("large-v3", "Best Accuracy"),
    "6": ("turbo", "Turbo v3 (Recommended)"),
}

DEFAULT_MODEL = "6"


def choose_device():
    print("\n========== Device Selection ==========")
    print("1. Auto (Recommended)")
    print("2. GPU")
    print("3. CPU")
    
    choice = input("\nChoose device [Press Enter = Auto]: ").strip()
    
    if choice == "" or choice == "1":
        return "auto"
    elif choice == "2":
        return "cuda"
    elif choice == "3":
        return "cpu"
    else:
        print("Invalid choice, defaulting to Auto.")
        return "auto"


def choose_language():
    print("\n========== Language Selection ==========")
    print("1. Auto")
    print("2. English")
    print("3. Indonesia")
    print("\nOther supported language codes:")
    
    codes = [c for c in _LANGUAGE_CODES if c not in ('en', 'id')]
    for i in range(0, len(codes), 12):
        print("  " + ", ".join(codes[i:i+12]))
        
    choice = input("\nChoose language (1/2/3) or type 2-letter code [Press Enter = Auto]: ").strip().lower()
    
    if choice in ("", "1", "auto"):
        return None
    elif choice in ("2", "en", "english"):
        return "en"
    elif choice in ("3", "id", "indonesia", "indonesian"):
        return "id"
    elif choice in _LANGUAGE_CODES:
        return choice
    else:
        print("Invalid language code, defaulting to Auto.")
        return None


def choose_model():
    print("\n========== Faster Whisper Models ==========")

    for key, (name, desc) in MODELS.items():
        default = " (Default)" if key == DEFAULT_MODEL else ""
        print(f"{key}. {name:<10} - {desc}{default}")

    choice = input("\nChoose model [Press Enter = Turbo]: ").strip()

    if choice == "":
        choice = DEFAULT_MODEL

    while choice not in MODELS:
        choice = input("Invalid choice. Choose again: ").strip()

    return MODELS[choice][0]


def main():
    print("========================================")
    print(" Faster Whisper Audio Transcription")
    print("========================================\n")

    # ------------------------------
    # Setup Directories
    # ------------------------------
    os.makedirs("Audio", exist_ok=True)
    os.makedirs("Result", exist_ok=True)

    # ------------------------------
    # Audio File
    # ------------------------------
    while True:
        audio_file_input = input("Audio file name (include extension): ").strip()
        audio_file = os.path.join("Audio", audio_file_input)

        if os.path.exists(audio_file):
            break

        print("File not found in Audio folder.\n")

    # ------------------------------
    # Model
    # ------------------------------
    model_name = choose_model()

    # ------------------------------
    # Device
    # ------------------------------
    device_choice = choose_device()

    # ------------------------------
    # Language
    # ------------------------------
    language_choice = choose_language()

    # ------------------------------
    # Output File
    # ------------------------------
    output_file_input = input(
        "\nTranscript output filename [default=result.txt]: "
    ).strip()

    if output_file_input == "":
        output_file_input = "result.txt"

    if not output_file_input.endswith(".txt"):
        output_file_input += ".txt"
        
    output_file = os.path.join("Result", output_file_input)

    print("\nLoading model...")
    start = time.time()

    model = WhisperModel(
        model_name,
        device=device_choice,
        compute_type="default",
    )

    print(f"Model loaded in {time.time()-start:.2f} sec")
    print("\nTranscribing...\n")

    segments, info = model.transcribe(
        audio_file,
        language=language_choice,
        beam_size=5,
        vad_filter=True,
        word_timestamps=False,
    )

    with open(output_file, "w", encoding="utf-8") as f:

        for segment in segments:

            line = (
                f"[{segment.start:8.2f} - "
                f"{segment.end:8.2f}] "
                f"{segment.text}"
            )

            print(line)
            f.write(line + "\n")

    print("\n========================================")
    print("Finished!")
    print(f"Language : {info.language}")
    print(f"Output   : {output_file}")
    print("========================================")


if __name__ == "__main__":
    main()