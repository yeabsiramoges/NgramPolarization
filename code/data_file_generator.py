import csv
import json
import spacy
import nltk

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from const import *

nltk.download('wordnet')
nltk.download('omw-1.4')

# CSV Tools

nlp = spacy.load("en_core_web_sm")
porter_stemmer = PorterStemmer()
word_net_lemmatizer = WordNetLemmatizer()

def generate_csv(adfontes_links, adfontes_text):
    with open(ADFONTES_CSV_FILE, "w", encoding="UTF-8") as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n', delimiter='>')
        
        for link, text in zip(adfontes_links, adfontes_text):
            if link not in open(ADFONTES_CSV_FILE, 'r', encoding='UTF-8').read():
                text = text.replace("\n"," ")
                processed_text = data_processing(text)
                writer.writerow((link, text, processed_text))

def extract_csv_data(adfontes_csv_file=ADFONTES_CSV_FILE):
    csv_dict = {
        'links':[],
        'text':[],
        'processed_text':[]
    }
    with open(adfontes_csv_file, "r", encoding="UTF-8") as csv_file:
        for line in csv_file:
            line_list = line.split(">")
            link, text, processed_text = line.split(">")

            csv_dict['links'].append(link)
            csv_dict['text'].append(text)
            csv_dict['processed_text'].append(processed_text)
    return csv_dict

def data_processing(text):
    processed_data = ""
    punctuations="?:!.,;"

    segmented_sentence = nlp(text).text
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(segmented_sentence)

    filtered_sentence = []

    for word in word_tokens:
        if word not in stop_words and word not in punctuations:
            filtered_sentence.append(word)
    
    for index in range(len(filtered_sentence)):
        word = filtered_sentence[index]
        word = porter_stemmer.stem(word)
        word = word_net_lemmatizer.lemmatize(word, pos="v")

        filtered_sentence[index] = word

    return ' '.join(filtered_sentence)

# Json Tools

def generate_json(adfontes_dict):
    with open(ADFONTES_JSON_FILE, "w", encoding='UTF-8') as json_file:
        json.dump(adfontes_dict, json_file)
    
def extract_dict(adfontes_json_file=ADFONTES_JSON_FILE):
    with open(adfontes_json_file, 'r', encoding='UTF-8') as json_file:
        return json.load(json_file)