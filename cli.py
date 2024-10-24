# cli.py

import argparse

from flask_ml.flask_ml_cli import MLCli
from tts_flask_ml.server.server import server

def main():
    parser = argparse.ArgumentParser(description="Convert text files to audio files")
    cli = MLCli(server, parser)
    cli.run_cli()


if __name__ == "__main__":
    main()