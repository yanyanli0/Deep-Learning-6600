# DSAN 6600 Deep Learning Final Project
## Voice-to-Text with Spelling and Grammar Correction

Final Project for DSAN 6600: Neural Networks and Deep Learning

Group members:
* Yanyan Li
* Hongxin Wu
* Xinran Zhang

Pretrain Models:
| Model | Link | About |
|-------|------|-------|
| facebook/wav2vec2-base-960h | https://huggingface.co/facebook/wav2vec2-base-960h| Wav2Vec2 |
| oliverguhr/spelling-correction-english-base | https://huggingface.co/oliverguhr/spelling-correction-english-base | Text2Text Generation |
| vennify/t5-base-grammar-correction | https://huggingface.co/vennify/t5-base-grammar-correction | Text2Text Generation |

App UI:
| Name | Link |
|------|------|
| Flask for Python | https://flask.palletsprojects.com/en/3.0.x/ |

## Abstract

In an increasingly interconnected world, the ability to understand and communicate in English is vital for non-native speakers. This project addresses this need by developing an innovative speech recognition tool that not only transcribes spoken language but also corrects spelling and grammar. With the use of advanced deep learning models—facebook/wav2vec2-base-960h for transcription, oliverguhr/spelling-correction-English-base for spelling, and vennify/t5-base-grammar-correction for grammar—our system has been trained on a diverse dataset of TED Talks and YouTube videos to handle a variety of accents and speech patterns.

The outstanding point in this project is an intuitive web application that contains the process of recording, playback, and transcription for users, making the technology accessible to students and educators globally. The backend of the application, built with Python and Flask, processes voice inputs and delivers corrected text output, providing better understanding and learning. Our evaluation, using metrics such as Word Error Rate (WER) and Character Error Rate (CER), indicates significant improvements in model performance post fine-tuning.

Looking ahead, we aim to expand its dataset and refine its models to capture even broader linguistic features. The ultimate goal is to enhance the educational experience and facilitate clearer communication for English learners worldwide.
