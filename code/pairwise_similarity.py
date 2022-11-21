from sklearn.feature_extraction.text import TfidfVectorizer
from parser import *
import numpy as np
from media_analysis import *
from data_file_generator import *

documents = ["I'd like an apple", 
            "An apple a day keeps the doctor away", 
            "Never compare an apple to an orange", 
            "I prefer scikit-learn to Orange", 
            "The scikit-learn docs are Orange and Blue"]


input_doc = "The scikit-learn docs are Orange and Blue"


bias_dict = {
    "foxnews": ("HYPER_PARTISAN_RIGHT","SELECTIVE_INFORMATION"),
    "cnn": ("SKEWS_LEFT","FACT_REPORTING"),
    "cnbc": ("MIDDLE","FACT_REPORTING")
}


def pairwise_sim(documents, input_doc, links=False):
    if links:
        documents = [open(f).read() for f in documents]
    
    tfidf = TfidfVectorizer().fit_transform(documents)
    pairwise_similarity = tfidf * tfidf.T

    arr = pairwise_similarity.toarray()     
    np.fill_diagonal(arr, np.nan)                                                                                                                                                                                                                            
                                                                                                                                                                                                  
    input_idx = documents.index(input_doc)                                                                                                                                                                                                                      

    result_idx = np.nanargmax(arr[input_idx])                                                                                                                                                                                                                
    return documents[result_idx]


#pairwise_sim(documents, input_doc)

total_links = []
total_links.extend(retreive_links("https://www.cnn.com/us"))
total_links.extend(retreive_links("https://www.foxnews.com/"))
total_links.extend(retreive_links("https://www.cnbc.com/"))

input_doc = 'coronavirus'
total_links.append(input_doc)

print("___________________________")
domain = extract_domain(pairwise_sim(total_links, input_doc))
sub_domain, name, top_level = domain.split(".")
print("Pairwise Result:", domain)
print("Name:",name)
print("Classification:",bias_dict[name])

adfontes_base_link = "https://adfontesmedia.com/rankings-by-individual-news-source/"

adfontes_links = retreive_adfontes_links(adfontes_base_link)

read_range = adfontes_links[0:5]
adfontes_text = parse_text(read_range)
print(read_range)
print(len(adfontes_text))
print(adfontes_text)
bias_dict = generate_bias_dict(read_range, adfontes_text)
print(bias_dict)

generate_csv(read_range, adfontes_text)
generate_json(bias_dict)