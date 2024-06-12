import re
from collections import Counter
import math

def tokenize(code):
    tokens = re.findall(r'\b\w+\b', code)
    return tokens

def token_frequency(tokens):
    return Counter(tokens)

def cosine_similarity(counter1, counter2):
    intersection = set(counter1.keys()) & set(counter2.keys())
    numerator = sum([counter1[x] * counter2[x] for x in intersection])

    sum1 = sum([v**2 for v in counter1.values()])
    sum2 = sum([v**2 for v in counter2.values()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator

def compare_codes(code1, code2):
    tokens1 = tokenize(code1)
    tokens2 = tokenize(code2)
    freq1 = token_frequency(tokens1)
    freq2 = token_frequency(tokens2)
    similarity = cosine_similarity(freq1, freq2)
    return similarity

def getdata(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return file_content

path1 = "pocpath1"
path2 = "pocpath2"
poccontent1 = getdata(path1)
poccontent2 = getdata(path2)
similarity = compare_codes(poccontent1, poccontent2)
