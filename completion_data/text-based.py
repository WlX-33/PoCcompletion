import json
import csv
import numpy as np
from gensim.models import Word2Vec
import numpy as np
from gensim.models import KeyedVectors
from gensim.parsing.preprocessing import remove_stopwords
from scipy import spatial
model = Word2Vec.load('poc_content_word2vec_model.bin')

def preprocess_text(text):
    return text.lower().split()
def get_sentence_vector(text, model):
    words = preprocess_text(text)
    # word_vectors = [model[word] for word in words if word in model.key_to_index]
    word_vectors = [model.wv[word] for word in words if word in model.wv.key_to_index]
    if len(word_vectors) == 0:
        return np.zeros(model.vector_size)
    sentence_vector = np.mean(word_vectors, axis=0)
    return sentence_vector
def calculate_similarity(vector1, vector2):
    sim = 0
    norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    if norm_product > 0:
        sim = np.dot(vector1, vector2) / norm_product
    return sim
def read_json(name):
    js_path = name
    f = open(js_path, 'r', encoding='latin')
    f = json.load(f) 
    return f

# Example usage
with open('pocpath1', 'r', encoding='utf-8') as file:
    code1 = file.read()

with open('pocpath2', 'r', encoding='utf-8') as file:
    code2 = file.read()

cve1 = get_sentence_vector(code1, model)
cve2 = get_sentence_vector(code2, model)
score = calculate_similarity(cve1, cve2)
print(score)
