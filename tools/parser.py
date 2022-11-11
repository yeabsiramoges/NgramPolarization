from urllib.error import HTTPError
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
import re
import csv
import nltk
from nltk.util import ngrams

from numpy import true_divide

LINK_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\links.txt"
TEXT_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\text.txt"
CONGRESS_TWITTER_ACCOUNTS_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\Congress.csv"

SNOPES_ARTICLE_LIST = r"C:\Users\user\Documents\NGramPolarization\data\Snopes\snopes.tsv"
ARTICLES_FILE = r"C:\Users\user\Documents\NGramPolarization\data\news_articles.csv"

INFORMATIVE_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\informative.txt"
MISINFORMATION_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\misinformation.txt"

UNIQUE_SPLITTER = "@@@"

def parse_text():
    with open(LINK_FILE_PATH, "r", encoding="utf-8", errors="replace") as links:
        for link in links:
            try:
                skip = False
                link = link.split(" ")

                classification = link[0]
                url = link[1]

                page = urlopen(url)
                domain = urlparse(url).netloc

                html = page.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                
                page_text = re.sub('\\s+', ' ', soup.get_text()).replace("\n", "\t")
                
                if classification == "INFORMATIVE":
                    FILE_PATH = INFORMATIVE_FILE_PATH
                elif classification == "MISINFORMATION":
                    FILE_PATH = MISINFORMATION_FILE_PATH
                else:
                    skip = True
                
                if not skip:
                    text = open(FILE_PATH, "a", encoding="utf-8", errors="replace")
                    text.write(domain + UNIQUE_SPLITTER + classification + UNIQUE_SPLITTER + page_text + "\n")
                    text.close()
            except HTTPError:
                pass

    links.close()

    with open(TEXT_FILE_PATH, "r", encoding="utf-8", errors="replace") as links:
        for link in links:
            print(link.split(UNIQUE_SPLITTER)[0])

def parse_twitter_accounts():
    with open(CONGRESS_TWITTER_ACCOUNTS_FILE_PATH, "r", encoding="utf-8", errors="replace") as officials:
        for official in officials:
            official_data = official.split(",")
            twitter_account = official_data[2].replace("https://twitter.com/", "")

            try:
                twitter_account_file = open("accounts.txt", "x",encoding='utf-8', errors='replace')
            except FileExistsError:
                print("Files already exist")

            twitter_account_file = open("accounts.txt", "a",encoding='utf-8', errors='replace')
            twitter_account_file.write(twitter_account + " ")
    officials.close()


#Separate from the rest

def parse_mega_article_set(file, label_id, text_id, deli=","):
    bigram_dict = {}
    trigram_dict = {}

    with open(file, "r", encoding="utf-8", errors="replace") as input_file:
        csv_reader = csv.reader(input_file, delimiter=deli)
        for line in csv_reader:
            label = "MISINFORMATION" if line[label_id] == "Fake" else "INFORMATIVE"
            text_without_stopwords = line[text_id]

            monogram = text_without_stopwords.split(" ")
            bigram = [' '.join(e) for e in ngrams(monogram, 2)]
            trigram = [' '.join(e) for e in ngrams(monogram, 3)]

            for b in bigram:
                if b in bigram_dict:
                    mis, inf = bigram_dict[b]
                    if label == "MISINFORMATION":
                        mis += 1
                    if label == "INFORMATIVE":
                        inf += 1
                    bigram_dict[b] = (mis, inf)
                else:
                    mis = 0
                    inf = 0
                    if label == "MISINFORMATION":
                        mis = 1
                    if label == "INFORMATIVE":
                        inf = 1
                    bigram_dict[b] = (mis, inf)
            
            for t in trigram:
                if t in trigram_dict:
                    mis, inf = trigram_dict[t]
                    if label == "MISINFORMATION":
                        mis += 1
                    if label == "INFORMATIVE":
                        inf += 1
                    trigram_dict[t] = (mis, inf)
                else:
                    mis = 0
                    inf = 0
                    if label == "MISINFORMATION":
                        mis = 1
                    if label == "INFORMATIVE":
                        inf = 1
                    trigram_dict[t] = (mis, inf)
    with open("bigrams2.csv", "a", encoding="utf-8", errors="replace") as output:
        for key in bigram_dict:
            if bigram_dict[key][0] != 0 and bigram_dict[key][1] != 0 and bigram_dict[key][0] == bigram_dict[key][1]:
                output.write(key + "," + str(bigram_dict[key][0]) + "," + "NEUTRAL")
                output.write("\n")
            else:
                if bigram_dict[key][0] != 0:
                    output.write(key + "," + str(bigram_dict[key][0]) + "," + "MISINFORMATION")
                    output.write("\n")
                if bigram_dict[key][1] != 0:
                    output.write(key + "," + str(bigram_dict[key][1]) + "," + "INFORMATIVE")
                    output.write("\n")
    with open("trigrams2.csv", "a", encoding="utf-8", errors="replace") as output:
        for key in trigram_dict:
            if trigram_dict[key][0] != 0 and trigram_dict[key][1] != 0 and trigram_dict[key][0] == trigram_dict[key][1]:
                output.write(key + "," + str(trigram_dict[key][0]) + "," + "NEUTRAL")
                output.write("\n")
            else:
                if trigram_dict[key][0] != 0:
                    output.write(key + "," + str(trigram_dict[key][0]) + "," + "MISINFORMATION")
                    output.write("\n")
                if trigram_dict[key][1] != 0:
                    output.write(key + "," + str(trigram_dict[key][1]) + "," + "INFORMATIVE")
                    output.write("\n")

parse_mega_article_set(ARTICLES_FILE, 8, 10)
parse_mega_article_set(SNOPES_ARTICLE_LIST, 0, 3)