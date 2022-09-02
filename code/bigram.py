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

    def compare_to(self, other):
        return self.get_bigram_string() == other.get_bigram_string()