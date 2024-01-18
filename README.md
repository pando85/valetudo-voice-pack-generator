# Valetudo voice package generator

This repository contains a collection of scripts designed to simplify the creation of custom voice
packages for Valetudo, a vacuum cleaner robot middleware. Leveraging the Whisper and Piper TTS
libraries, these scripts enable users to generate personalized voice packages by converting text to
speech and integrating them seamlessly into the Valetudo system. Enhance your vacuuming experience
with unique voice prompts tailored to your preferences.

## Get files from robot

```bash
mkdir -p data/original
scp -O -r root@{{ valetudo_ip }}:{{ robot_audio_files }} data/original/
```

**Note**: In my case, robot audio files are under `/audio/EN`

## Speak to text

```bash
pip install -r requirements.txt
./get_sounds_list.py
```

## Create new audios using piper

Download voices from https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0

```bash
curl -LO 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx?download=true'
curl -LO 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx.json?download=true'

pip install piper-tts
./voice-generator.sh -m en_US-ryan-high.onnx

tar -czf voice_pack.tar.gz -C data/output/EN/ .
md5sum voice_pack.tar.gz > md5sum.txt
```

After uploading from Valetudo's interface, files are located at `/data/personalized_voice/XX` in my
robot.


## Download and extract audios

```bash
yt-dlp 'https://www.youtube.com/watch?v=XXXXXXXX'
ffmpeg -i input.webm -vn -acodec pcm_s16le -ar 22050 -ac 2 output.wav
```

## Split audio

Run `./split_audio.py` to split audio into different sentences to train the piper model.

## Split files

Run `./split_files.sh` to get the zip files to load into `https://github.com/rhasspy/piper/blob/2fa4c2c13933c1f6b8d87e34d12788ca8e6d073b/notebooks/piper_multilingual_training_notebook.ipynb`.
