import os
import platform
import sys

from typing import TypedDict
from flask_ml.flask_ml_server import MLServer
from flask_ml.flask_ml_server.models import (
    ResponseBody,
    BatchFileInput,
    DirectoryInput,
    FileResponse,
    FileType,
    BatchFileResponse,
    TaskSchema,
    InputSchema,
    InputType,
    ParameterSchema,
    EnumParameterDescriptor,
    EnumVal
)

sys.path.append(os.getcwd() + os.sep + os.pardir + os.sep + os.pardir)
from tts_flask_ml.main.tts_converter import TTSConverter

tts = TTSConverter()
server = MLServer(__name__)

class FilesInputs(TypedDict):
    input_files: BatchFileInput
    output_dir: DirectoryInput

class DirectoryInputs(TypedDict):
    input_dir: DirectoryInput 
    output_dir: DirectoryInput

class Parameters(TypedDict):
    audio_format: str

def create_tts_task_schema(files_as_input) -> TaskSchema:
    input_schemas = [
        InputSchema(
            key="input_files" if files_as_input else "input_dir",
            label="Text Files to Convert" if files_as_input else "Input Directory",
            input_type=InputType.BATCHFILE if files_as_input else InputType.DIRECTORY,
        ),
        InputSchema(
            key="output_dir",
            label="Output Directory",
            input_type=InputType.DIRECTORY,
        )
    ]
    parameter_schemas = [
        ParameterSchema(
            key="audio_format",
            label="Audio Format",
            value=EnumParameterDescriptor(
                enum_vals=[
                    EnumVal(key="mp3", label="MP3"),
                    EnumVal(key="aiff", label="AIFF"),
                    EnumVal(key="wav", label="WAV"),
                ],
                default="aiff" if platform.system() == "Darwin" else "mp3",
            )
        )
    ]
    return TaskSchema(
        inputs = input_schemas,
        parameters = parameter_schemas
    )

@server.route("/tts_converter_files", task_schema_func=lambda: create_tts_task_schema(True), short_title="Text Files to Audio Files Converter", order=0)
def tts_converter_files(inputs: FilesInputs, parameters: Parameters) -> ResponseBody:
    print("Inputs:", inputs)
    print("Parameters:", parameters)

    files = [file.path for file in inputs["input_files"].files]
    output_dir = inputs["output_dir"]

    tts.set_audio_format(parameters["audio_format"])

    res = [
        FileResponse(path=r, title=os.path.basename(r), file_type=FileType.AUDIO)
        for r in tts.convert_batch(files, output_dir.path)
    ]
    return ResponseBody(root=BatchFileResponse(files=res))

@server.route("/tts_converter_dir", task_schema_func=lambda: create_tts_task_schema(False), short_title="Directory of Text Files to Audio Files Converter", order=1)
def tts_converter_dir(inputs: DirectoryInputs, parameters: Parameters) -> ResponseBody:
    print("Inputs:", inputs)
    print("Parameters:", parameters)

    input_dir = inputs["input_dir"]
    output_dir = inputs["output_dir"]

    tts.set_audio_format(parameters["audio_format"])

    res = [
        FileResponse(path=r, title=os.path.basename(r), file_type=FileType.AUDIO)
        for r in tts.convert_from_dir(input_dir.path, output_dir.path)
    ]
    return ResponseBody(root=BatchFileResponse(files=res))


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
