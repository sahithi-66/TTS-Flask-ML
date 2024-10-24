import os
import platform

import pyttsx3
from tts_flask_ml.main.helper import *

class TTSConverter:
    def __init__(self):
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 1)
        self.engine = engine
        self.audio_format = ".aiff" if platform.system() == "Darwin" else ".mp3"

    def set_audio_format(self, audio_format: str) -> None:
        self.audio_format = "." + audio_format

    def write_to_audio_file(self, text: str, audio_file: str) -> str:
        self.engine.save_to_file(text, audio_file)
        self.engine.runAndWait()
        print(f"Audio file created: {os.path.basename(audio_file)}")
        return audio_file

    def convert_single(self, text_file: str, output_dir: str) -> str:
        text = extract_text_from_file(text_file)
        if text == '':
            raise ValueError("Input text file not found or could not be read")

        os.makedirs(output_dir, exist_ok=True)

        file_name = extract_file_name(text_file)
        print(f"Processing file: {file_name}")
        return self.write_to_audio_file(
            text, os.path.join(output_dir, file_name + self.audio_format)
        )

    def convert_batch(self, text_files: list[str], output_dir: str) -> list[str]:
        if len(text_files) == 0:
            raise ValueError("Input can not be empty")

        print(f"Processing {len(text_files)} files....")
        return [self.convert_single(file, output_dir) for file in text_files]

    def convert_from_dir(self, input_dir: str, output_dir: str) -> list[str]:
        text_files = extract_text_files_from_dir(input_dir)
        if len(text_files) == 0:
            raise ValueError("Input path not found or no text files found")

        print(f"Found {len(text_files)} text files in the input directory")
        return self.convert_batch(text_files, output_dir)
