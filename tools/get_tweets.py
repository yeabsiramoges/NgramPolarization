import os

CONGRESS_TWITTER_ACCOUNTS_FILE_PATH = r"C:\Users\user\Documents\NGramPolarization\data\Congress.csv"
CLI_PY_PATH = r"C:\Users\user\Documents\NGramPolarization\imports\Optimized-Modified-GetOldTweets3-OMGOT\GetOldTweets3-0.0.10\cli.py"

with open(CONGRESS_TWITTER_ACCOUNTS_FILE_PATH, "r", encoding="utf-8", errors="replace") as officials:
    for official in officials:
        official_data = official.split(",")
        twitter_account = official_data[1].replace("https://twitter.com/", "")

        shell_command = "python " + CLI_PY_PATH + " --username " + twitter_account
        output_stream = os.popen(shell_command)

        try:
            congress_tweets_file = open("tweets.txt", "x",encoding='utf-8', errors='replace')
        except FileExistsError:
            print("Files already exist")

        congress_tweets_file = open("tweets.txt", "a",encoding='utf-8', errors='replace')
        output_stream.read()
officials.close()