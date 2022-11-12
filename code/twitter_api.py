import twint

def generate_date_range(beginning_year, end_year):
    date_ranges = []
    month = ("01-01", "12-31")
    for year in range(beginning_year, end_year+1):
        new_beginning_year = str(year)+"-"+month[0]
        new_end_year = str(year)+"-"+month[1]
        date_ranges.append((new_beginning_year, new_end_year))
    return date_ranges

def generate_tweets():
    config = twint.Config()
    config.Search = "Obama"
    twint.run.Search(config)

tweets = generate_tweets()
print(tweets)