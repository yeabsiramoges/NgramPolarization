import pandas as pd
from nltk import ngrams, Text
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import string
import collections
import re
import matplotlib.pyplot as plt
import requests

nltk.download('vader_lexicon')

TEXT_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\text.txt"
UNIQUE_SPLITTER = "@@@"

def analizer(file_path, classification, wrangle):
    #open corpus text file
    with open(file_path,"r",encoding='utf-8', errors='replace') as file:    
        corpus_text = file.read().split(UNIQUE_SPLITTER)[2]

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
        bigrams_file = open(classification+" "+"bigrams.txt", "x")
        trigrams_file = open(classification+" "+"trigrams.txt", "x")
    except FileExistsError:
        print("Files already exist")

    #overwrite any existing data in file
    bigrams_file = open(classification+" "+"bigrams.txt", "w")
    trigrams_file = open(classification+" "+"trigrams.txt", "w")

    bigrams_list = list(bi_grams_freq.most_common())
    trigrams_list = list(tri_grams_freq.most_common())

    bigrams_file.write(str(bigrams_list))
    trigrams_file.write(str(trigrams_list))

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
        bigram_concordance_file = open("concordance.txt", "x")
    except:
        bigram_concordance_file = open("concordance.txt", "w")

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

analizer(TEXT_FILE_PATH, "INFORMATIVE", False)