#!/usr/bin/env python
import argparse
import logging
import os
import sys

from faster_whisper import WhisperModel
from pydub import AudioSegment

logging.basicConfig(
    level=logging.INFO,  # Set the logging level (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log message format
)


def cut_audio(input_file, output_file, start_time_ms, end_time_ms):
    audio = AudioSegment.from_wav(input_file)
    cut_audio = audio[start_time_ms:end_time_ms]

    logging.info(f"`Cutting audio to {output_file}`")
    cut_audio.export(output_file, format="wav")


def process_ogg_files(model, input_audio, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    logging.info(f"`{input_audio}` processing file with Whisper")
    segments, _ = model.transcribe(input_audio, language="es", beam_size=5)

    for idx, segment in enumerate(segments):
        output_path_basename = f"{output_directory}/{idx}"
        txt_file = f"{output_path_basename}.txt"
        logging.info(f"`{txt_file}` writing file")
        with open(txt_file, "w") as output_file:
            output_file.write(segment.text)

        cut_audio(input_audio, f"{output_path_basename}.wav", segment.start * 1000, (segment.end * 1000) + 200)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process OGG files and generate text using Whisper.")

    parser.add_argument("--input-audio", default="data/input.wav", help="Path to input WAV audio.")
    parser.add_argument(
        "--output-directory", default="data/split_audio", help="Path to the directory to store text output."
    )
    parser.add_argument("--model-size", default="large-v3", help="Size of the Whisper model.")
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

    process_ogg_files(model, args.input_audio, args.output_directory)
