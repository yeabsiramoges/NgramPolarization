import json
from json import JSONEncoder

class Bigram():
    '''
    Bigram class used to create and track the existence of bigrams in both the 
    political leaning classification as well as the informative classification.
    Currenly supplies MLE calculation on a running basis.
    '''
    def __init__(self, bigram_string):
        self.bigram_string = bigram_string
        self.misinformation_count = 0
        self.informative_count = 0
    
    def get_bigram_string(self):
        return self.bigram_string

    def get_misinformation_count(self):
        return self.misinformation_count

    def get_informative_count(self):
        return self.informative_count

    def get_total_count(self):
        return self.get_informative_count() + self.get_misinformation_count()
    
    def increment_misinformation_count(self, count):
        self.misinformation_count+=count
    
    def increment_informative_count(self, count):
        self.informative_count+=count

    def compare_to(self, other):
        return self.get_bigram_string() == other.get_bigram_string()

    def maximum_likelihood_estimator(self):
        return self.get_misinformation_count() / (self.get_total_count())
    
    def get_csv_formatting(self):
        return self.get_bigram_string()  + "," + str(self.get_total_count()) + "," + str(self.maximum_likelihood_estimator()) +"\n"

class BigramEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__