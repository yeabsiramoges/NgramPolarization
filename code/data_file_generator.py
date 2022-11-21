import csv
import json
from const import *

def generate_csv(adfontes_links, adfontes_text):
    with open(ADFONTES_CSV_FILE, "w", encoding="UTF-8") as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        
        for link, text in zip(adfontes_links, adfontes_text):
            if link not in open(ADFONTES_CSV_FILE, 'r', encoding='UTF-8').read():
                text = text.replace("\n"," ")
                writer.writerow((link, text))

def generate_json(adfontes_dict):
    with open(ADFONTES_JSON_FILE, "w", encoding='UTF-8') as json_file:
        json.dump(adfontes_dict, json_file)