import pyttsx3
import helper as h
import os
import platform

class TTSConverter:
    def __init__(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1)
        self.engine = engine
        self.audio_format = ".aiff" if platform.system() == "Darwin" else ".mp3"
    

    def write_to_audio_file(self, text: str, audio_file: str) -> str:
        self.engine.save_to_file(text, audio_file)
        self.engine.runAndWait()
        self.engine.stop()
        return audio_file


    def convert_single(self, text_file: str, out_dir: str=None) -> str:
        text = h.extract_text_from_file(text_file)
        if text is None:
            raise ValueError("Input text file not found or could not be read")
        
        if out_dir is None:
            os.makedirs(out_dir)
        else:
            out_dir = h.extract_directory(text_file)

        return self.write_to_audio_file(text, out_dir + h.extract_file_name(text_file) + self.audio_format)
    
    def convert_batch(self, text_files: list[str], out_dir: str=None) -> list[str]:
        if text_files is None or len(text_files) == 0:
            raise ValueError("Input can not be empty")
        
        return [self.convert_single(file, out_dir) for file in text_files]
    
    def convert_from_dir(self, input_dir: str, out_dir: str=None) -> list[str]:
        text_files = h.extract_text_files_from_dir(input_dir)

        if text_files is None:
            raise ValueError("Input path not found or could not be read")
        
        return self.convert_batch(text_files, out_dir)
        

