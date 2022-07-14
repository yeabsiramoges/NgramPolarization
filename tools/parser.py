from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

LINK_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\links.txt"

url="https://stackoverflow.com/questions/25863101/python-urllib-urlopen-not-working"

with open(LINK_FILE_PATH, "r", encoding="utf-8", errors="replace") as file:
    for url in file:
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        
        page_text = re.sub('\\s+', ' ', soup.get_text())
        