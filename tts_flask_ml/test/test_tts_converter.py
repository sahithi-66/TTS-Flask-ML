import os
import sys

import pytest

sys.path.append(os.getcwd() + os.sep + os.pardir + os.sep + os.pardir)

from tts_flask_ml.main.tts_converter import TTSConverter


def test_convert_single_valid_input():
    converter = TTSConverter()
    text_file = "./words_100.txt"
    output_dir = "../../outputs"
    result = converter.convert_single(text_file, output_dir)
    assert os.path.exists(result)


def test_convert_single_invalid_input_file_not_found():
    converter = TTSConverter()
    text_file = "nonexistent_file.txt"
    output_dir = "../../outputs"
    with pytest.raises(ValueError):
        converter.convert_single(text_file, output_dir)


def test_convert_batch_valid_input():
    converter = TTSConverter()
    text_files = ["./words_100.txt", "./words_9999.txt"]
    output_dir = "../../outputs"
    results = converter.convert_batch(text_files, output_dir)
    assert len(results) == 2
    for result in results:
        assert os.path.exists(result)


def test_convert_batch_invalid_input_empty_list():
    converter = TTSConverter()
    text_files = []
    output_dir = "../../outputs"
    with pytest.raises(ValueError):
        converter.convert_batch(text_files, output_dir)


def test_convert_from_dir_valid_input():
    converter = TTSConverter()
    input_dir = "./"
    output_dir = "../../outputs"
    results = converter.convert_from_dir(input_dir, output_dir)
    assert len(results) >= 2  # Ensure at least two files are converted
    for result in results:
        assert os.path.exists(result)


def test_convert_from_dir_invalid_input_directory_not_found():
    converter = TTSConverter()
    input_dir = "nonexistent_dir"
    output_dir = "../../outputs"
    with pytest.raises(ValueError):
        converter.convert_from_dir(input_dir, output_dir)
