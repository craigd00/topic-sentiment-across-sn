## 08/02/22

# Meeting conducted over message on MS teams

### What I had done since last meeting
* It was more difficult than we thought to actually find these python libraries for sentiment analysis, as the majority of online posts refer to either VADER or TextBlob which we are already using, have one or two more to try and investigate so not sure if they will be applicable yet
* Tried a sentiment analysis library called Flair, problem was it only predicted positive or negative and not neutral. It also took over an hour to run it on only one database for the first lockdown run back in november, so it wasn't going to be suitable as it could not even run this as it just crashed after just over an hour. Spent a while trying to get it to work with the dataset but think there was too much data for it to handle. However on the papers I read on it, it has high accuracy compared to VADER and TextBlob but it is more of a classifier than a library, and even if I could eventually get it working with the dataset, it does not give us the three values we need.
* Tried another sentiment analysis library called Afinn, this worked similar to VADER and TextBlob theoretically, and was a bit slower calculating sentiment, probably around fifteen mins for each individual run. It classifies a lot more posts as negative compared to the other two sentiment analysis features.
* Have only found really one more library to do with this called FastText, still need to test it to see if it is capable of doing what we need it to do.

### BERT
* Going to have a proper look at a bert model this week, was looking at hugging face transformers but there is not much readily available datasets to train it on similar to what we are trying to do. 
* The sentiment analysis datasets for training on kaggle did not seem great, so thinking it might be useful to manually label some of the data and test it against this to see performance
* Might be a bit time consuming so will try again to find a dataset before I try this. 

### Filtering Results
* I think some reddit posts were also picking up other languages which may affect results, so I need to filter out the results to make sure this is not the case


### For the next meeting
* Test out BERT to see if it is possible