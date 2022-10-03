import csv
from operator import indexOf
from tkinter.tix import TEXT
import pandas as pd
from nltk import ngrams, Text
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import string
import collections
import re
import matplotlib.pyplot as plt
import requests
from Bigram import Bigram
import json

from Bigram import BigramEncoder

nltk.download('vader_lexicon')

INFORMATIVE_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\informative.txt"
MISINFORMATION_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\misinformation.txt"
SNOPES_ARTICLE_LIST = r"C:\Users\user\Documents\NGramPolarization\data\Snopes\snopes.tsv"
BIGRAMS_LIST = r"C:\Users\user\Documents\NGramPolarization\code\bigrams.csv"

TEXT_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\text.txt"
UNIQUE_SPLITTER = "@@@"

DEPTH = 30

def article_analizer(file_path, wrangle, plot):
    #open corpus text file
    with open(file_path,"r",encoding='utf-8', errors='replace') as file:
        for line in file:
            data = line.split(UNIQUE_SPLITTER)
            
            domain, classification, corpus_text = data

            #text cleanup
            regex = "[" + re.sub("\.", "",string.punctuation) + "]"

            corpus_text = re.sub('<.*>','', corpus_text)
            corpus_text = re.sub(regex, "", corpus_text)

            #getting words
            tokenized = corpus_text.split()

            bigrams = ngrams(tokenized, 2)
            trigrams = ngrams(tokenized, 3)

            #counting bigrams
            bi_grams_freq = collections.Counter(bigrams)
            tri_grams_freq = collections.Counter(trigrams)

            #try to create file
            try:
                bigrams_file = open("bigrams.txt", "x",encoding='utf-8', errors='replace')
                trigrams_file = open("trigrams.txt", "x",encoding='utf-8', errors='replace')
            except FileExistsError:
                print("Files already exist")

            #add to any existing data in file
            bigrams_file = open("bigrams.txt", "a",encoding='utf-8', errors='replace')
            trigrams_file = open("trigrams.txt", "a",encoding='utf-8', errors='replace')

            bigrams_list = bi_grams_freq.most_common(DEPTH)
            trigrams_list = tri_grams_freq.most_common(DEPTH)

            bigrams_file.write(str(bigrams_list)+", "+classification+"\n")
            trigrams_file.write(str(trigrams_list)+", "+classification+"\n")

            if plot:
                #ngram plots
                bigrams_series = pd.DataFrame(bigrams_list[0:20], columns=["Bigram", "Frequency"])
                bigrams_series.plot(kind="bar",
                                    x="Bigram",
                                    y="Frequency",
                                    color="green")
                plt.title("Corpus Bigram Frequency Plot")
                #plt.show()

            #extracting concordance and sentiment analysis
            corpus_text = Text(tokenized)
            ngram_index = 0

            try:
                bigram_concordance_file = open("concordance.txt", "x",encoding='utf-8', errors='replace')
            except:
                bigram_concordance_file = open("concordance.txt", "w",encoding='utf-8', errors='replace')

            concordance_data = []

            #sentiment analyzer
            sia = SentimentIntensityAnalyzer()

            for ngram in bigrams_list:
                bigram = ngram[0][0] + " " + ngram[0][1]
                bigram_concordance = corpus_text.concordance_list([ngram[0][0], ngram[0][1]])
                sentiment = sia.polarity_scores(bigram)
                concordance_data.append([ngram_index, bigram, bigram_concordance, sentiment])
                ngram_index += 1

            bigram_concordance_file.write(str(concordance_data))

            #Storywrangler API
            depth = 10
            lang = "es"
            metric = "rank"
            rt = "false"
            src = "api"

            dfs = {}

            if wrangle:
                for ngram in bigrams_list[0:depth]:
                    phrase = ngram[0][0] + " " + ngram[0][1]
                    storywrangler_api = requests.get("https://storywrangling.org/api/ngrams/%s?metric=%s&language=%s&rt=%s&src=%s" % (phrase,metric,lang,rt,src)).json()

                    dfs[phrase] = pd.DataFrame(
                        storywrangler_api['data'], 
                        columns=[phrase])
                    
                for ngram in dfs:
                    dfs[ngram].to_csv(f"{ngram}.csv")

def snopes_analizer():
    with open(SNOPES_ARTICLE_LIST, "r", encoding="utf-8", errors="replace") as articles:
        for article in articles:
            data = article.split("	")
            
            quality = "INFORMATIVE" if data[0] == "true" else "MISINFORMATION"
            text = data[3]

            
            #text cleanup
            regex = "[" + re.sub("\.", "",string.punctuation) + "]"

            text = re.sub('<.*>','', text)
            text = re.sub(regex, "", text)

            #getting words
            tokenized = text.split()

            bigrams = ngrams(tokenized, 2)
            trigrams = ngrams(tokenized, 3)

            #counting bigrams
            bi_grams_freq = collections.Counter(bigrams)
            tri_grams_freq = collections.Counter(trigrams)
            
            #try to create file
            try:
                bigrams_file = open("bigrams.txt", "x",encoding='utf-8', errors='replace')
                trigrams_file = open("trigrams.txt", "x",encoding='utf-8', errors='replace')
            except FileExistsError:
                print("Files already exist")

            #add to any existing data in file
            bigrams_file = open("bigrams.txt", "a",encoding='utf-8', errors='replace')
            trigrams_file = open("trigrams.txt", "a",encoding='utf-8', errors='replace')
            
            bigrams_list = bi_grams_freq.most_common(DEPTH)
            trigrams_list = tri_grams_freq.most_common(DEPTH)

            for bigram in bigrams_list:
                bigrams_file.write(str(bigram)+", "+quality+"\n")
            for trigram in trigrams_list:
                trigrams_file.write(str(bigram)+", "+quality+"\n")

#snopes_analizer()

def count_instances():
    with open(BIGRAMS_LIST, "r", encoding="utf-8", errors="replace") as bigrams:
        ngram_list = []

        try:
            mle_file = open("mle.csv", "x",encoding='utf-8', errors='replace')
        except FileExistsError:
            print("File already exist")
        
        for bigram in bigrams:
            data = bigram.split(",")
            bigram_string, frequency, classification = data
            
            ngram = Bigram(bigram_string)

            if (ngram in ngram_list):
                print("editing")
                index = ngram_list.indexOf(ngram)
                if ("MISINFORMATION" in classification):
                    ngram_list[index].increment_misinformation_count(int(frequency))
                else:
                    print("here")
                    ngram_list[index].increment_informative_count(int(frequency))
            else:
                if ("MISINFORMATION" in classification):
                    ngram.increment_misinformation_count(int(frequency))
                else:
                    ngram.increment_informative_count(int(frequency))

                ngram_list.append(ngram)
            print(ngram.maximum_likelihood_estimator(), ngram.get_informative_count(), ngram.get_misinformation_count())
            mle_file = open("mle.csv", "a",encoding='utf-8', errors='replace')
            mle_file.write(ngram.get_csv_formatting())
        
        mle_file.close()

def mle_calculator(bigram_file):
    mle_list = {}
    encoded = {}
    with open(bigram_file,"r",encoding='utf-8', errors='replace') as file:
        for line in file:
            bigram_string, freq, value = line.split(",")
            new_bigram = Bigram(bigram_string)
            if bigram_string not in mle_list.keys():
                mle_list[bigram_string] = new_bigram
            else:
                if value == "MISINFORMATION":
                    mle_list[bigram_string].increment_misinformation_count(int(freq))
                else:
                    mle_list[bigram_string].increment_informative_count(int(freq))
    for mle in mle_list.keys():
        print(mle_list[mle].get_csv_formatting())
        encoded[mle] = mle_list[mle].get_csv_formatting()
    return encoded



#count_instances()
#mle = mle_calculator(BIGRAMS_LIST)
#with open('convert.txt', 'w') as convert_file:
#     convert_file.write(json.dumps(mle))

def spread_out(file):
    with open(file,"r",encoding='utf-8', errors='replace') as file:
        count_mis = 0
        count_inf = 0
        for line in file:
            bigram_string, freq, value = line.split(",")
            for i in range(int(freq)):
                print(bigram_string, "MISINFORMATION" in value)
                if "MISINFORMATION" in value:
                    if count_mis <= 100000:
                        file_name = "main_directory/misinformation/" + str(count_mis) + ".txt"
                    else:
                        file_name = "test_directory/misinformation/" + str(count_mis) + ".txt"
                    try:
                        misinformation = open(file_name, "x",encoding='utf-8', errors='replace')
                    except:
                        print("File already exists")
                    misinformation = open(file_name, "a",encoding='utf-8', errors='replace')
                    misinformation.write(bigram_string)
                    count_mis+=1
                    misinformation.close()
                else:
                    if count_inf <= 100000:
                        file_name = "main_directory/informative/" + str(count_mis) + ".txt"
                    else:
                        file_name = "test_directory/informative/" + str(count_mis) + ".txt"
                    try:
                        informative = open(file_name, "x",encoding='utf-8', errors='replace')
                    except:
                        print("File already exists")
                    informative = open(file_name, "a",encoding='utf-8', errors='replace')
                    informative.write(bigram_string)
                    count_inf+=1
                    informative.close()

spread_out(BIGRAMS_LIST)
