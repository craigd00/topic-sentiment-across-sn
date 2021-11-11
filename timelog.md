# Timelog

* Determining Topic Sentiment Across Social Network Platforms
* Craig Dick
* 2378675D
* Supervisor: Peter Inglis

## Guidance

* This file contains the time log for your project. It will be submitted along with your final dissertation.
* **YOU MUST KEEP THIS UP TO DATE AND UNDER VERSION CONTROL.**
* This timelog should be filled out honestly, regularly (daily) and accurately. It is for *your* benefit.
* Follow the structure provided, grouping time by weeks.  Quantise time to the half hour.

## Week 1

* Chose project

## Week 2

### 29 Sep 2021

* *1 hour* Read over what is expected from us for project, how much each part was worth
* *2 hours* Researched for the best task managers, reference manager, tools to use
* *0.5 hour* Zotero for reference managing, going to use built in issue tracker on Github
* *2 hours* Researched potential APIs for searching social media, Facebook, Twitter, Flickr, Instagram, LinkedIn
* *2 hours* Looked at lectures from previous year on sentiment analysis, classifiers, etc.

### 1 Oct 2021

* *0.5 hour* First meeting with supervisor, talked about project goals

## Week 3

* Was ill at start of week, so nothing was able to get done until Wednesday

### 6 Oct 2021

* *1 hour* Set up github and overleaf for project
* *0.5 hour* Created this timelog, cloned project on my PC
* *0.5 hour* Created a wiki for the Github, added previous weeks minutes
* *3 hours* Read literature about topic sentiment analysis

### 7 Oct 2021
* *0.5 hour* Rescheduled meeting with supervisor, spoke about the research papers
* *2 hours* Looked at potential Python libraries that could use for sentiment analysis
* *1 hour* Found VADER, played around with it for a bit to see how it worked

## Week 4

* Supervisor changed the meeting this week to the following week

### 15 Oct 2021
* *2.5 hours* Researching Facebook Graph API, watching Youtube tutorials
* *0.5 hour* Deciding Facebook will be practically impossible due to no public search
* *0.5 hour* Instagram and Facebook API's both offer limited features after Cambridge Analytica
* *0.5 hour* Created email to use for authenticating API's in this project
* *2 hours* Using a TikTok API wrapper to see how it works, built test code using it
* *0.5 hour* Applied for Twitter developer account as will need it eventually

## Week 5

* Meeting also pushed back further due to supervisor's research commitments

### 20 Oct 2021
* *1 hour* Watched YouTube and read articles on whether it is possible to scrape Facebook, seems like it will cause a ban for IP
* *0.5 hour* Downloaded moodle project template and put meetings from wiki into folder on project too

### 21 Oct 2021
* *1 hour* Reddit seems like it has a useable API, maybe too similar to Twitter but researched articles on it

### 22 Oct 2021
* *2 hours* Tried to set up test version of Reddit API
* *2 hours* Set up basic version of Reddit API from tutorial, enabled it to topic search, need to figure out how to get comments from posts

## Week 6

* Meeting ayschronous on teams this week

### 27 Oct 2021
* *3 hours* Figured out how to get comments from Reddit API, figured out how to get post id's 
* *2 hours* Tidied up Reddit code, created a smoother way in Jupyter notebook to investigate clearer

### 29 Oct 2021
* *2 hours* Added the sentiment analyser to the reddit code, obviously not trained fully yet to classify
* *3 hours* Set up Twitter API, similar style to reddit notebook too
* *0.5 hour* Merged feature branches for reddit and twitter into develop branch
* *1 hour* Tested and tried TikTok API again, not suitable, will not work

## Week 7

* Meeting on Tuesday

### 2 Nov 2021
* *0.5 hour* Discussed project progress with supervisor

### 3 Nov 2021
* *0.5 hour* Looked at Reddit API limits, if connecting through OAuth2 can make 60 requests/min
* *0.5 hour* Trying to figure out if you can search by time period on Reddit - value t on search?

### 5 Nov 2021
* *1 hour* Transferred twitter and reddit code from notebooks into runnable python, changed it so it only creates lists of texts instead of dictionaries
* *2 hours* Figuring out set up of MongoDB clusters, got one created for project to test dataset

### 6 Nov 2021
* *3 hours* Converted both twitter and reddit code to insert posts and tweets into a MongoDB collection, trialled it before 24 hour run tomorrow

### 7 Nov 2021
* *2 hours* Fiddled about with code, for some reason seems to stop after a while, is there not enough tweets available about Nicola Sturgeon?

## Week 8

* Meeting asychronous on teams this week

### 8 Nov 2021
* *2 hours* Tried to run again but this time changed to Boris Johnson, seems to collect more data as think there is more tweets about him, twitter only looks at past 7 days

### 9 Nov 2021
* *2 hours* Trying to change the code in Twitter and Reddit so that it can run continuously, twitter runs for decent time
* *1 hour* Made a reddit file to loop through subreddits instead of r/all, will this stop it breaking?

### 10 Nov 2021
* *2 hours* Test run on twitter worked, collected 60k docs. Reddit gets a json decode error after a while, trying to see if this is because it runs out of posts?
* *0.5 hour* Reddit code doesn't collect enough unique posts, only 2000ish out of 20k dataset are unique and not sure why
* *3 hours* Reddit API kept failing, found new API called Pushshift that stores reddit data, sometimes 24hr delay to saving data but for a dataset this should not be a problem, can set dates to filter from etc.