class Bigram:
    def __init_(self, bigram_string, misinformation_count, informative_count):
        self.bigram_string = bigram_string
        self.misinformation_count = misinformation_count
        self.informative_count = informative_count
    
    def increment_misinformation_count(self):
        misinformation_count+=1
    
    def increment_informative_count(self):
        informative_count+=1
    
    def get_bigram_string(self):
        return self.bigram_string

    def get_misinformation_count(self):
        return self.misinformation_count

    def get_informative_count(self):
        return self.informative_count

    def compare_to(self, other):
        return self.get_bigram_string() == other.get_bigram_string()

    def maximum_likelihood_estimator(self):
        return self.get_misinformation_count() / (self.get_informative_count() + self.get_misinformation_count())