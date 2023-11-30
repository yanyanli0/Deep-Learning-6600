import numpy as np
import json
import nltk
from nltk.tokenize import sent_tokenize
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load pre-trained spelling correction model and tokenizer
spelling_correction = 'oliverguhr/spelling-correction-english-base'
spelling_model = AutoModelForSeq2SeqLM.from_pretrained(spelling_correction)
spelling_tokenizer = AutoTokenizer.from_pretrained(spelling_correction)

# Load pre-trained grammar correction model and tokenizer
grammar_correction = 'vennify/t5-base-grammar-correction'
grammar_model = AutoModelForSeq2SeqLM.from_pretrained(grammar_correction)
grammar_tokenizer = AutoTokenizer.from_pretrained(grammar_correction)

# Function to correct spelling
def correct_spelling(input_text):
    sentences = sent_tokenize(input_text)
    corrected_sentences = []
    for sentence in sentences:
        tokens = spelling_tokenizer(sentence, return_tensors="pt", truncation=True, max_length=spelling_tokenizer.model_max_length)
        outputs = spelling_model.generate(**tokens, max_length=spelling_tokenizer.model_max_length)
        corrected_sentence = spelling_tokenizer.decode(outputs[0], skip_special_tokens=True)
        corrected_sentences.append(corrected_sentence)
    return ' '.join(corrected_sentences)

# Function to correct grammar
def correct_grammar(input_text):
    tokens = grammar_tokenizer(input_text, return_tensors="pt", truncation=True, max_length=grammar_tokenizer.model_max_length)
    outputs = grammar_model.generate(**tokens, max_length=grammar_tokenizer.model_max_length)
    return grammar_tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function to correct both spelling and grammar
def correct_spelling_and_grammar(input_text):
    spelling_corrected = correct_spelling(input_text)
    return correct_grammar(spelling_corrected)

# Read input text from file
with open('myvoice_transcription.txt', 'r', encoding='utf-8') as file:
    input_text = file.read().strip()

combined_corrected_text = correct_spelling_and_grammar(input_text)

# Specify the filename
output_filename = "../Data/myvoice_transcription_corrected.txt"

# Save the combined corrected text to a file
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(combined_corrected_text)
