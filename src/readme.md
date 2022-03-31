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
* `sentiment_analysis.ipynb` Analysis of the comparisons of Twitter and Reddit, times of the libraries, and how sentiment changed over time.
* `shared_modules.py` Functions that are used in both Twitter and Reddit analysis
* `twitter_afinn_all.ipynb`, `twitter_bert_all.ipynb`, `twitter_textblob_all.ipynb`, and `twitter_vader_all.ipynb` conduct the sentiment analysis on the Twitter database terms by applying functions in `shared_modules.py` to get the sentiment of tweets.
* `twitter_search.py` Runs the data collection of tweets based on a query parameter, saves the posts collected to MongoDB
* `twittercredentials.py` The keys and tokens used to have access to the Twitter API
* `wordcloud_terms.ipynb` Produces wordclouds of the most positive and negative terms associated with positive posts and negative posts for each term

## Build instructions

**You must** include the instructions necessary to build and deploy this project successfully. If appropriate, also include 
instructions to run automated tests. 

### Requirements

List the all of the pre-requisites software required to set up your project (e.g. compilers, packages, libraries, OS, hardware)

For example:

* Python 3.7
* Packages: listed in `requirements.txt` 
* Tested on Windows 10

or another example:

* Requires Raspberry Pi 3 
* a Linux host machine with the `arm-none-eabi` toolchain (at least version `x.xx`) installed
* a working LuaJIT installation > 2.1.0

### Build steps

List the steps required to build software. 

Hopefully something simple like `pip install -e .` or `make` or `cd build; cmake ..`. In
some cases you may have much more involved setup required.

### Test steps

List steps needed to show your software works. This might be running a test suite, or just starting the program; but something that could be used to verify your code is working correctly.

Examples:

* Run automated tests by running `pytest`
* Start the software by running `bin/editor.exe` and opening the file `examples/example_01.bin`

