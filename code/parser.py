from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


links = ["http://news.bbc.co.uk/2/hi/health/2284783.stm"]

def retreive_links(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    urls = []
    for link in soup.find_all('a'):
        if "://" in str(link.get('href')) or "www" in str(link.get('href')):
            urls.append(link.get('href'))
    
    return urls

def parse_text(links):
    text_list = []
    for url in links:
        try:
            html = urlopen(url).read()
            soup = BeautifulSoup(html, features="html.parser")

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.body.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            text_list.append(text)
        except:
            continue
    return text_list

def extract_domain(url):
    domain = urlparse(url).netloc
    return domain

def retreive_adfontes_links(base_link):
    final_links = []
    for page in range(1,9):
        page_link = base_link
        if page != 1:
            page_link += str(page) + "/"
        retreived_links = retreive_links(page_link)
        for link in retreived_links:
            if "bias-and-reliability" in link:
                final_links.append(link)
    return final_links