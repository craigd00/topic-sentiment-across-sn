## 25/01/22

### What I had done since last meeting
* Ran code over past two weeks for all terms
* Now have 3 databases for different periods of time

### Problems since last time
* Cluster filled with space, so have created a new cluster each time I run the data for all 7 terms
* Reddit Pushshift API stopped retrieving all comments from a post with the query term in the title

### Pushshift problem
* Leave at the side for now, can remove terms not containing the query when analysing but keep in database

### Data
* How much data do we have? Three runs of each term at the moment
* Classifier allows us to measure different posts
* Want to visualise - whole point of analysis is difference between reddit and twitter
* With data can plot a time series of how sentiment changes

### Classifier
* K-means could be good to look at, would need a training set for classifiers
* Using VADER as NLP has limitations

### Mitigation and Limitations
* Potential roadmap to mediate concern - mitigation
* Important we understand the limitations of the project going into it and the writeup
* Could look at TextBlob v VADER if classifiers is too time constrained, could measure performance by comparing the sentiment tools

### Literature Review
* Background on NLP
* How NLP sentiment takes place
* Introduce problem and why NLP is a good choice

### For the next meeting
* See how sentiment changes as time goes on
* Have a look at literature background
* Potentially see classifiers - specifically K-means
* Remove unwanted posts