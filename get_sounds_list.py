#!/usr/bin/env python
import argparse
import logging
import os
import sys

from faster_whisper import WhisperModel

logging.basicConfig(
    level=logging.INFO,  # Set the logging level (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log message format
)


def recognize_speech(model, audio_file):
    segments, _ = model.transcribe(audio_file, language="en", beam_size=5)
    return " ".join([s.text for s in segments])


def process_ogg_files(model, directory, output_directory):
    # Create the output directory if it does not exist
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(directory):
        if filename.endswith(".ogg"):
            ogg_path = os.path.join(directory, filename)

            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".txt")
            if not os.path.exists(output_path):
                text = recognize_speech(model, ogg_path)

                with open(output_path, "w") as output_file:
                    output_file.write(text)

                logging.info(f"text from {filename} saved to `{output_path}`")
            else:
                logging.info(f"`{output_path}` file already exists")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process OGG files and generate text using Whisper.")

    parser.add_argument(
        "--ogg_directory", default="data/original/EN", help="Path to the directory containing OGG files."
    )
    parser.add_argument(
        "--output_directory", default="data/original/EN_text", help="Path to the directory to store text output."
    )
    parser.add_argument("--model_size", default="large-v3", help="Size of the Whisper model.")
    parser.add_argument(
        "--device", default="cpu", help="Device used in WhisperDevice to use for computation ('cpu', 'cuda', 'auto')."
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        help="""Type to use for computation.
        See https://opennmt.net/CTranslate2/quantization.html.""",
    )

    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger("faster_whisper").setLevel(logging.ERROR)

    # Run on GPU with FP16
    model = WhisperModel(args.model_size, device=args.device, compute_type=args.compute_type)
    # model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # or run on GPU with INT8
    # or run on CPU with INT8
    # model = WhisperModel(model_size, device="cpu", compute_type="int8")

    process_ogg_files(model, args.ogg_directory, args.output_directory)
