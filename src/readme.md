# Readme

This code is used to collect datasets of posts and tweets from Reddit and Twitter, and build a database of terms based on this. The posts and tweets are then taken back from the database to use in analysis of the sentiment. The sentiment is calculated in the notebooks, saved to Dill variables, and graphed to show the results.

* `cardiffnlp` Holds the twitter-roberta-base-sentiment BERT model after installing libraries
* `confusion_matrices` The confusion matrices for each sentiment library analysed against the test set in csv_test_files
* `csv_test_files` The vaccine sentiment test set from Kaggle to analyse model performance
* `reddit_graphs` Holds the graphs for Reddit runs for each sentiment library for all terms, as well as the graphs for the most popular subreddits for each run
* `reddit_vars` Dill files for each sentiment run, used to save the sentiment analysis results after run for the library
* `sentiment_graphs` Graphs for the time taken for each library
    + `afinn` Graphs for twitter and reddit runs on same graph for each term, subreddit sentiment graphed using Afinn results with threshold and top values
    + `bert` Graphs for twitter and reddit runs on same graph for each term, subreddit sentiment graphed using BERT results with threshold and top values
    + `textblob` Graphs for twitter and reddit runs on same graph for each term, subreddit sentiment graphed TextBlob Afinn results with threshold and top values
    + `vader` Graphs for twitter and reddit runs on same graph for each term, subreddit sentiment graphed using VADER results with threshold and top values
    + `lib_comparisons` Graphs the overall summed total sentiment for each library Twitter v Reddit, as well as more graphs for individual terms for each run of Twitter and Reddit
* `twitter_graphs` Holds the graphs for Twitter runs for each sentiment library for all terms
* `twitter_vars` Dill files for each sentiment run, used to save the sentiment analysis results after run for the library
* `wordclouds` Wordcloud images for each library, for both Twitter and Reddit, for each term, displaying the most popular words for each run of the term for positive sentiment posts and negative sentiment posts
* `__init__.py` Used so the tests can detect the code
* `.gitignore` Stops unnecessary files and large files being pushed to GitHub
* `evaluation_of_libraries.ipynb` Evaluates the sentiment analysis libraries performance against a vaccine sentiment test dataset.
* `manual.md` Contains information on how the code can be executed to collect the terms specific to task, and then analyse the sentiment.
* `mongodbcredentials.py` Holds the CONNECTION_STRING details for the databases on MongoDB
* `reddit_afinn_all.ipynb`, `reddit_bert_all.ipynb`, `reddit_textblob_all.ipynb`, and `reddit_vader_all.ipynb` Conducts the sentiment analysis on the Reddit database terms by applying functions in `shared_modules.py` to get the sentiment of posts.
* `reddit_modules.py` Has the specific functions for Reddit analysis and processing
* `reddit_pushshift_search.py` Runs the data collection for Reddit based on a query, using the Pushshift API
* `remove_reddit_terms.ipynb` Used to check that no false Reddit posts filtered into the database
* `requirements.txt` Used to install the packages that the project depends on 
* `sentiment_analysis.ipynb` Analysis of the comparisons of Twitter and Reddit, times of the libraries, and how sentiment changed over time.
* `shared_modules.py` Functions that are used in both Twitter and Reddit analysis
* `twitter_afinn_all.ipynb`, `twitter_bert_all.ipynb`, `twitter_textblob_all.ipynb`, and `twitter_vader_all.ipynb` conduct the sentiment analysis on the Twitter database terms by applying functions in `shared_modules.py` to get the sentiment of tweets.
* `twitter_search.py` Runs the data collection of tweets based on a query parameter, saves the posts collected to MongoDB
* `twittercredentials.py` The keys and tokens used to have access to the Twitter API
* `wordcloud_terms.ipynb` Produces wordclouds of the most positive and negative terms associated with positive posts and negative posts for each term

## Build instructions
To allow the code to run, it is recommended to create a new virtual environment to run this on. This can be achieved by typing the following command on an Anaconda Powershell Prompt
* `conda create -n environment_name python=3.7.9`
* `conda activate environment_name`
To install the packages required to run the project, with requirements.txt being the requirements file from here in your local directory
* `pip install -r requirements.txt`
The tests are held in the tests folder. To run these:
* `pytest --cov tests/ -W ignore::DeprecationWarning`
* These are held in a folder outwith the `src/` folder, so these may need to be viewed on [GitHub](https://github.com/craigd00/topic-sentiment-across-sn)

### Requirements
The prerequisites for setup of the project are

* Python 3.7.9
* Packages: listed in `requirements.txt` 
* Tested on Windows 10

### Build steps
* `conda create -n environment_name python=3.7.9`
* `conda activate environment_name`
* `pip install -r requirements.txt`

### Test steps
Pytest feature testing can be run using the tests in the `tests` directory

* Run automated tests by running `pytest --cov tests/ -W ignore::DeprecationWarning`


