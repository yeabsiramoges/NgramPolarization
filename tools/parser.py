from urllib.error import HTTPError
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
import re

from numpy import true_divide

LINK_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\links.txt"
TEXT_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\text.txt"

INFORMATIVE_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\informative.txt"
MISINFORMATION_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\misinformation.txt"

UNIQUE_SPLITTER = "@@@"

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