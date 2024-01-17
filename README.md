# Valetudo voice package generator

This repository contains a collection of scripts designed to simplify the creation of custom voice
packages for Valetudo, a vacuum cleaner robot middleware. Leveraging the Whisper and Piper TTS
libraries, these scripts enable users to generate personalized voice packages by converting text to
speech and integrating them seamlessly into the Valetudo system. Enhance your vacuuming experience
with unique voice prompts tailored to your preferences.

## Get files from robot

```bash
mkdir -p data/original
scp -O -r root@{{ valetudo_ip }}:/audio/EN data/original/
```

## Speak to text

```bash
pip install -r requirements.txt
python get_sounds_list.py
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
