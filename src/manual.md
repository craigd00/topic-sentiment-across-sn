# User manual 

## API code to collect posts
The Twitter collection code is contained in `twitter_search.py` in `src/`, as well as the Reddit collection code of `reddit_pushshift_search.py`.
* Reddit code 
    + To collect data for a term, reddit_db, reddit_collection and CONNECTION_STRING variables can all be changed to map to where you want to store the data.
    + The query parameter can be modified to show the search term you are wanting to search for.
    + The date_from variable has to be changed to the date you want to begin searching from. For this project, as data was collected for a week, this variable was changed to the time of searching minus a week. The date is input in the format year, month, day, hour and mins.
    + Running `python reddit_pushshift_search.py` after the parameters are changed to suit your collection data on the anaconda powershell prompt will then begin running the API and saving the posts to your MongoDB collection.

* Twitter code 
    + To collect data for a term, twitter_db, twitter_collection and CONNECTION_STRING variables can all be changed to map to where you want to store the data.
    + The code imports the consumer_key, consumer_secret, access_token, and access_token_secret from code in the src called `twitter_credentials.py`. This file can be changed to hold your own credentials.
    + The query term can also be changed to reflect the topic you are wanting to search for.
    + You can then run `python twitter_search.py` on your anaconda powershell prompt begins the collection of tweets containing your query, and saves this to the MongoDB database specified.

## Sentiment Analysis
The sentiment analysis is determined in `src/` by using functions in `shared_modules.py` to classify the posts into positive, negative, or neutral.
* This is conducted for Reddit in the notebooks `reddit_afinn_all.ipynb`, `reddit_bert_all.ipynb`, `reddit_textblob_all.ipynb`, and `reddit_vader_all.ipynb`. The same is executed for Twitter, in `twitter_afinn_all.ipynb`, `twitter_bert_all.ipynb`, `twitter_textblob_all.ipynb`, and `twitter_vader_all.ipynb`. 
* Code only relevant to Twitter data is held in `twitter_modules.py`, and the same for Reddit in `reddit_modules.py`. Functions that both Twitter and Reddit data and analysis use is in `shared_modules.py`. All sentiment analysis can be viewed on how the graphs were made, in `sentiment_analysis.ipynb`.
* Graphs are saved to the folders described containing graphs in the readme.md file in `src/`.