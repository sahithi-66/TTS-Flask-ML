from flask_ml.flask_ml_client import MLClient

TTS_CONVERTER_URL = "http://127.0.0.1:5000/tts_converter_files"  # The URL of the server
client = MLClient(TTS_CONVERTER_URL)  # Create an instance of the MLClient object

## Update inputs before testing
inputs = {
    "input_files": {
        "files": [
            { "path": "./tts_flask_ml/test/words_100.txt" },
            { "path": "./tts_flask_ml/test/words_9999.txt" }
        ]
    },
    "output_dir": { "path": "./outputs" }
}  # The inputs to be sent to the server
parameters = { "audio_format": "mp3" }  # The parameters to be sent to the server

response = client.request(inputs, parameters)  # Send a request to the server
print(response)  # Print the response

# Excepcted response
# {
#     'output_type': 'batchfile',
#     'files': [
#         {
#             'output_type': 'file',
#             'file_type': 'audio',
#             'path': './outputs/words_100.mp3',
#             'title': 'words_100.mp3',
#             'subtitle': None
#         },
#         {
#             'output_type': 'file',
#             'file_type': 'audio',
#             'path': './outputs/words_9999.mp3',
#             'title': 'words_9999.mp3',
#             'subtitle': None
#         }
#     ]
# }
