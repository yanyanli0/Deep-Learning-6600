import os
import sys
import time
import json
import pyaudio
import wave
import soundfile as sf
import torch
import numpy as np
import transformers
transformers.logging.set_verbosity_error()
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16_000

def record_audio(fname, duration_seconds):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording ...")
    frames = []
    for i in range(0, int(RATE / CHUNK * duration_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(fname, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_audio(fname, duration_seconds):
    wf = wave.open(fname, 'rb')
    p = pyaudio.PyAudio()
    t = time.time()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data != '' and (time.time() - t) < (duration_seconds + 2):
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.close()
    p.terminate()

def transcribe(fname, model_name):
    # load model and tokenizer
    processor = Wav2Vec2Processor.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name)
    # tokenize
    speech, _ = sf.read(fname)
    input_values = processor([speech,],
                             return_tensors="pt",
                             padding="longest").input_values
    # retrieve logits
    logits = model(input_values).logits
    # take argmax and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    with open(fname.split('.')[0] + "_transcription.txt", "w") as fd:
        fd.write(transcription.lower())

def calculate_wer(reference, hypothesis):
    r = reference.split()
    h = hypothesis.split()
    # Building the matrix
    d = np.zeros((len(r)+1)*(len(h)+1), dtype=np.uint8)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0: 
                d[0][j] = j
            elif j == 0: 
                d[i][0] = i
    # Calculation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitute = d[i-1][j-1] + 1
                insert = d[i][j-1] + 1
                delete = d[i-1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d[len(r)][len(h)] / float(len(r))

def calculate_cer(reference, hypothesis):
    r = reference
    h = hypothesis
    # Building the matrix
    d = np.zeros((len(r)+1)*(len(h)+1), dtype=np.uint8)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i
    # Calculation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitute = d[i-1][j-1] + 1
                insert = d[i][j-1] + 1
                delete = d[i-1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d[len(r)][len(h)] / float(len(r))

if __name__ == '__main__':
    action = sys.argv[1].lower()
    fname = sys.argv[2]
    if action == "record":
        duration_seconds = float(sys.argv[3])
        record_audio(fname, duration_seconds)
    elif action == "play":
        duration_seconds = float(sys.argv[3])
        play_audio(fname, duration_seconds)
    elif action == "transcribe":
        model_name = "facebook/wav2vec2-base-960h"
        if len(sys.argv) > 3:
            model_name = sys.argv[3]
        transcribe(fname, model_name)
    elif action == "evaluate":
        reference_text = sys.argv[3]
        with open(reference_text, "r", encoding='utf-8') as fd:
            reference_text = fd.read().replace("\n", "").strip()
        with open(fname, 'r') as fd:
            transcription = fd.read().strip()
        wer = calculate_wer(reference_text, transcription)
        cer = calculate_cer(reference_text, transcription)
        # wer = fastwer.score([transcription],
        #                     [reference_text])
        # cer = fastwer.score([transcription],
        #                     [reference_text],
        #                     char_level=True)
        with open("results.json", "w") as fd:
            json.dump({"word_error_rate": wer,
                       "character_error_rate": cer},
                      fd, indent=3)