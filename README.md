# Valetudo voice package generator

This repository contains a collection of scripts designed to simplify the creation of custom voice
packages for Valetudo, a vacuum cleaner robot middleware. Leveraging the Whisper and Piper TTS
libraries, these scripts enable users to generate personalized voice packages by converting text to
speech and integrating them seamlessly into Valetudo. You can also personalize the voice by
finetuning a new Piper model from any audio source, allowing you to create unique voice prompts
tailored to your preferences or based on any speaker.

## 1. Get files from robot (optional)

```bash
mkdir -p data/original
scp -O -r root@{{ valetudo_ip }}:{{ robot_audio_files }} data/original/
```

**Note**: In my case, robot audio files are under `/audio/EN`

## 2. Download and extract audios from any source

You can use any audio source (e.g., YouTube, personal recordings) to create a custom voice model.

```bash
yt-dlp 'https://www.youtube.com/watch?v=XXXXXXXX'
ffmpeg -i input.webm -vn -acodec pcm_s16le -ar 22050 -ac 2 output.wav
```

## 3. Transcribe audio to text

Install requirements and run the script to generate text from your audio files using Whisper.

```bash
pip install -r requirements.txt
./get_sounds_list.py
```

## 4. Split audio into sentences

Run the script to split your audio into different sentences for Piper training.

```bash
./split_audio.py
```

## 5. Prepare files for Piper training

Run the script to generate the zip files needed for Piper model training or finetuning.

```bash
./split_files.sh
```

This will produce files ready to be loaded into the
[Piper multilingual training notebook](https://github.com/rhasspy/piper/blob/2fa4c2c13933c1f6b8d87e34d12788ca8e6d073b/notebooks/piper_multilingual_training_notebook.ipynb).

## 6. Personalize the voice model (finetune Piper)

To create a custom voice, use the prepared data to finetune a Piper model. Follow the instructions
in the
[Piper multilingual training notebook](https://github.com/rhasspy/piper/blob/2fa4c2c13933c1f6b8d87e34d12788ca8e6d073b/notebooks/piper_multilingual_training_notebook.ipynb)
to train or finetune a model using your own audio and transcriptions. This allows you to generate a
Piper model that matches any speaker from your audio source.

Once training is complete, download the resulting `.onnx` and `.onnx.json` model files.

## 7. Create new audios using Piper

Download a pre-trained or your personalized Piper model and use it to generate new audios.

```bash
# Example for downloading a pre-trained model
curl -LO 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx?download=true'
curl -LO 'https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx.json?download=true'

pip install piper-tts
./voice-generator.sh -m <your_model>.onnx
```

## 8. Package and upload to Valetudo

```bash
tar -czf voice_pack.tar.gz -C data/output/EN/ .
md5sum voice_pack.tar.gz > md5sum.txt
```

After uploading from Valetudo's interface, files are located at `/data/personalized_voice/XX` in
your robot.
