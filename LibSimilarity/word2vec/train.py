# Code to train a word2vec model with gensim
# For use with ml5.js word2vec examples
from gensim.models import Word2Vec
import re
import json
import sys
import argparse
import glob
import os

#Parsing for the user arguments
parser = argparse.ArgumentParser(description="Text File to Word2Vec Vectors")

#Required input file
parser.add_argument("input", help="Path to the input text file")

#Optional arguments (room for further extending the script's capabilities)
parser.add_argument("-o", "--output", default="vector.json", help="Path to the output text file (default: vector.json)")

args = parser.parse_args()

#Using the arguments from the arg dictionary
output_text_file = args.output

listOfFiles = []
if os.path.isdir(args.input):
    # Make a list with all txt in the folder
    listOfFiles = glob.glob(args.input + '/*.txt')
else:
    # use a single file
    listOfFiles.append(args.input)

final_sentences = []
for file in listOfFiles:
    with open(file, 'r', encoding='UTF-8') as f:
        texts = f.read().lower().splitlines()
        for text in texts:
            sentence_list = text.split()
            #  print(sentence_list)
            final_sentences.append(sentence_list)

    """
    text = open(file, encoding='UTF-8').read().lower()# Remove lineabreaks
    #print("text",text)
    # Split into sentences (this could be improved! Using nltk?)
    sentences = re.split("[.?!]", text)
    print("sentences",sentences)
    # Split each sentence into words! (this could also be improved!)
    for sentence in sentences:
        words = re.split(r'\W+', sentence)
        final_sentences.append(words)
    """

#print("final_sentences",final_sentences)
# Create the Word2Vec model
model = Word2Vec(final_sentences, size=300, window=5, min_count=5, workers=4)
# Save the vectors to a text file
model.wv.save_word2vec_format(output_text_file, binary=False)

# Open up that text file and convert to JSON
f = open(output_text_file,encoding='UTF-8')
v = {"vectors": {}}
for line in f:
    w, n = line.split(" ", 1)
    v["vectors"][w] = list(map(float, n.split()))

# Save to a JSON file
# Could make this an optional argument to specify output file
with open(output_text_file[:-4] + "json", "w") as out:
    json.dump(v, out)
