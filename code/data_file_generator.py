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

def extact_csv_data(adfontes_csv_file=ADFONTES_CSV_FILE):
    csv_dict = {
        'links':[],
        'text':[]
    }
    with open(adfontes_csv_file, "r", encoding="UTF-8") as csv_file:
        for line in csv_file:
            line_list = line.split(",")
            link = line_list[0]
            text = "".join(line_list[1:])

            csv_dict['links'].append(link)
            csv_dict['text'].append(text)
    return csv_dict


def generate_json(adfontes_dict):
    with open(ADFONTES_JSON_FILE, "w", encoding='UTF-8') as json_file:
        json.dump(adfontes_dict, json_file)
    
def extract_dict(adfontes_json_file=ADFONTES_JSON_FILE):
    with open(adfontes_json_file, 'r', encoding='UTF-8') as json_file:
        return json.load(json_file)