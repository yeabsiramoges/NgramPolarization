from urllib.error import HTTPError
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
import re

LINK_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\links.txt"
TEXT_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\text.txt"
UNIQUE_SPLITTER = "@@@"

with open(LINK_FILE_PATH, "r", encoding="utf-8", errors="replace") as links:
    for link in links:
        try:
            link = link.split(" ")

            classification = link[0]
            url = link[1]

            page = urlopen(url)
            domain = urlparse(url).netloc

            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            
            page_text = re.sub('\\s+', ' ', soup.get_text()).replace("\n", "\t")

            text = open(TEXT_FILE_PATH, "a", encoding="utf-8", errors="replace")
            text.write(domain + UNIQUE_SPLITTER + classification + UNIQUE_SPLITTER + page_text + "\n")
            text.close()
        except HTTPError:
            pass

links.close()

with open(TEXT_FILE_PATH, "r", encoding="utf-8", errors="replace") as links:
    for link in links:
        print(link.split(UNIQUE_SPLITTER)[0])