An overview of the file structure:

* `timelog.md` The time log for the project.
* `plan.md` A week-by-week plan of the project, updated weekly. 
* `src/` Source code for the project. .gitignore file included.
    + `cardiffnlp` Holds the twitter-roberta-base-sentiment BERT model after installing libraries
    + `confusion_matrices` The confusion matrices for each sentiment library analysed against the test set in csv_test_files
    + `csv_test_files` The vaccine sentiment test set from Kaggle to analyse model performance
    + `reddit_graphs` Holds the graphs for Reddit runs for each sentiment library for all terms, as well as the graphs for the most popular subreddits for each run
    + `reddit_vars` Dill files for each sentiment run, used to save the sentiment analysis results after run for the library
    + `sentiment_graphs` Graphs for the time taken for each library
        + `afinn` Graphs for twitter and reddit runs on same graph for each term, subreddit sentiment graphed using Afinn results with threshold and top values
        + `bert` Graphs for twitter and reddit runs on same graph for each term, subreddit sentiment graphed using BERT results with threshold and top values
        + `textblob` Graphs for twitter and reddit runs on same graph for each term, subreddit sentiment graphed TextBlob Afinn results with threshold and top values
        + `vader` Graphs for twitter and reddit runs on same graph for each term, subreddit sentiment graphed using VADER results with threshold and top values
        + `lib_comparisons` Graphs the overall summed total sentiment for each library Twitter v Reddit, as well as more graphs for individual terms for each run of Twitter and Reddit
    + `twitter_graphs` Holds the graphs for Twitter runs for each sentiment library for all terms
    + `twitter_vars` Dill files for each sentiment run, used to save the sentiment analysis results after run for the library
    + `wordclouds` Wordcloud images for each library, for both Twitter and Reddit, for each term, displaying the most popular words for each run of the term for positive sentiment posts and negative sentiment posts
* `tests/` Contains the tests used with Pytest in order to check functions are working correctly.
* `environment.yml` Includes dependencies for the environment to run for the GitHub workflow, created through exporting my virtual environment from conda
* `requirements.txt` All the libraries and modules required to run the code in this project
* `status_report/` The status report submitted in December.
* `meetings/` Records of the meetings during the project.
* `dissertation/` Project dissertation
* `presentation/` Presentation of project


* Continuous Integration provided by GitHub workflows throughout the project to automate the build and test that the functions were working correctly. Builds the project and installs dependencies using conda on Linux

## Installation
* To allow the code to run, it is recommended to create a new virtual environment to run this on. This can be achieved by typing the following command on an Anaconda Powershell Prompt
        + conda create -n environment_name python=3.7.9
        + conda activate environment_name
* To install the packages required to run the project, with requirements.txt being the requirements file from here in your local directory
        + pip install -r requirements.txt

## API code to collect posts
* The Twitter collection code is contained in `twitter_search.py` in `src/`, as well as the Reddit collection code of `reddit_pushshift_search.py`.
* Reddit code 
        + To collect data for a term, reddit_db, reddit_collection and CONNECTION_STRING variables can all be changed to map to where you want to store the data.
        + The query parameter can be modified to show the search term you are wanting to search for.
        + The date_from variable has to be changed to the date you want to begin searching from. For this project, as data was collected for a week, this variable was changed to the time of searching minus a week. The date is input in the format year, month, day, hour and mins.
        + Running python reddit_pushshift_search.py after the parameters are changed to suit your collection data on the anaconda powershell prompt will then begin running the API and saving the posts to your MongoDB collection.

* Twitter code 
        + To collect data for a term, twitter_db, twitter_collection and CONNECTION_STRING variables can all be changed to map to where you want to store the data.
        + The code imports the consumer_key, consumer_secret, access_token, and access_token_secret from code in the src called `twitter_credentials.py`. This file can be changed to hold your own credentials.
        + The query term can also be changed to reflect the topic you are wanting to search for.
        + You can then run python twitter_search.py on your anaconda powershell prompt begins the collection of tweets containing your query, and saves this to the MongoDB database specified.

## Sentiment Analysis
* The sentiment analysis is determined in `src/` by using functions in `shared_modules.py` to classify the posts into positive, negative, or neutral. This is conducted for Reddit in the notebooks `reddit_afinn_all.ipynb`, `reddit_bert_all.ipynb`, `reddit_textblob_all.ipynb`, and `reddit_vader_all.ipynb`. The same is executed for Twitter, in `twitter_afinn_all.ipynb`, `twitter_bert_all.ipynb`, `twitter_textblob_all.ipynb`, and `twitter_vader_all.ipynb`. Code only relevant to Twitter data is held in `twitter_modules.py`, and the same for Reddit in `reddit_modules.py`. Functions that both Twitter and Reddit data and analysis use is in `shared_modules.py`. All sentiment analysis can be viewed on how the graphs were made, in `sentiment_analysis.ipynb`.

## Data
* To view the data, the graphs can all be viewed within the `src/` directory as described above, with graphs and image data being in `confusion_matrices`, `reddit_graphs`, `sentiment_graphs`, `twitter_graphs` and `wordclouds`. Some graphs are also displayed in the Jupyter notebooks within src, but all of the relevant ones are in the folders described. To view the classification reports of the sentiment analysis libraries against a vaccine sentiment test set, the results are in `evaluation_of_libraries.ipynb`.