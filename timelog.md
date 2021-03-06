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

### 11 Nov 2021
* *2 hours* Made new code to search reddit using pushshift api
* *1 hour* Fails sometimes when getting the results back
* *1 hour* Think this happens if a post has since been deleted, added try except statements around the results
* *2 hours* Created functions to be able to get comments back using a post id, already able to get all comments and post titles containing the search query
* *1 hour* Gave it a test run, failed again so added another try except for the new functions added, will test run tomorrow

### 12 Nov 2021
* *2 hours* Left the code running, it pulled back 3k post titles containing query, 7k comments containing query, and 22k comments from titles containing query. Code did not break and successfully worked

## Week 9

* Meeting asychronous on teams this week as I had asked all my questions the previous week, and only had one question so was easier to message

### 17 Nov 2021
* *1 hour* Ran code on Nicola Sturgeon as a query, did not get much data but testing how much it brings back on different topics
* *1 hour* Ran the code on Joe Biden, left running over night as twitter had lots of tweets about him

### 18 Nov 2021
* *1 hour* Ran code on Keir Starmer
* *1 hour* Ran code on Spiderman

### 19 Nov 2021
* *1 hour* Ran code again on Boris Johnson as I couldn't change my MongoDB database names on him that I currently had, data from reddit was also over a month
* *2 hours* Made a python notebook to analyse emotion difference solely using VADER, going to try a NLP approach next week to see if this improves the work, maybe manually classify a small dataset

## Week 10

* Meeting on Tuesday 2pm

### 23 Nov 2021
* *0.5 hour* Meeting with supervisor, scope of project changed to investigate covid topics and if sentiment analysis can identify some misinformation spreading subreddits

### 25 Nov 2021
* *2 hours* Changed code to save the subreddits from posts, and also to pull back the post id comments after it has collected terms of query

### 26 Nov 2021
* *0.5 hour*  Changed query to run for vaccines

### 27 Nov 2021
* *0.5 hour*  Changed query to run for lockdown

### 28 Nov 2021
* *0.5 hour*  Changed query to run for PCR
* *0.5 hour*  Changed query to run for facemasks

## Week 11

* Meeting asynchronous this week - Progress stunted a bit this week due to amount of coursework

### 29 Nov 2021
* *2 hours* Ran code on queries Pfizer and quarantine

### 30 Nov 2021
* *0.5 hour* Ran code on restrictions

## Week 12

* Supervisor had MSc project readings and I had exams and deadlines, so was not able to meet

## Week 13

* Meeting on Tuesday 14th has been pushed to following week

### 13 Dec 2021
* *2 hours* Created functions to return the top subreddits from one of the search queries
* *2 hours* Code to investigate the sentiment of each of the posts and save the subreddit with it
* *1 hour* Plotting the sentiment amongst subreddits by their search query
* *0.5 hour* Plotting the topics against eachother in reddit
* *0.5 hour* Finding the overlap amongst subreddits between the queries

### 15 Dec 2021
* *2 hours* Code for the analysis on the twitter data, plotted graphs on the terms

## Christmas Break

* Any work complete over the holidays up till Semester 2 resumes, meeting with superviosr on the 21st

### 20 Dec 2021
* *1 hour* Changed the reddit code to view percentages as a comparison

### 21 Dec 2021
* *0.5 hour* Supervisor meeting, going to look at running the search terms again to gather perception over different time periods

### 3 Jan 2022
* *0.5 hour* MongoDB cluster ran out of space when trying to run again

### 6 Jan 2022
* *0.5 hour* Fixed MongoDB problem by creating new project cluster to store data to, if could do over again would have each topic as a cluster rather than each time frame
* *0.5 hour* Ran the code for "vaccine" again

### 9 Jan 2022
* *0.5 hour* Ran on vaccine - last time forgot to change date in reddit code so cluster got too full 

## Semester 2 


## Week 1

* No meeting yet as supervisor will get in contact with me when he knows day he is free

### 10 Jan 2022
* *0.5 hour* Ran on lockdown 

### 11 Jan 2022
* *0.5 hour* Ran on PCR 

### 12 Jan 2022
* *0.5 hour* Ran on facemasks 

### 13 Jan 2022
* *0.5 hour* Ran on Pfizer
* *0.5 hour* Ran on quarantine

### 14 Jan 2022 
* *0.5 hour* Computer update had changed IP for MongoDB so had to add current
* *0.5 hour* Ran on restrictions
* *0.5 hour* Ran on booster

## Week 2

* Supervisor contacted to arrange meeting for following week

### 17 Jan 2022
* *1 hour* Created new cluster for the third runs, ran the code on vaccine

### 19 Jan 2022
* *0.5 hour* Ran on lockdown

### 20 Jan 2022
* *0.5 hour* Ran on PCR
* *0.5 hour* Ran on facemasks

### 21 Jan 2022
* *0.5 hour* Ran on Pfizer

### 23 Jan 2022
* *0.5 hour* Ran on quarantine

## Week 3

* Supervisor meeting on the 25th 

### 24 Jan 2022
* *0.5 hour* Ran on restrictions
* *0.5 hour* Ran on booster

### 25 Jan 2022
* *0.5 hour* Meeting with supervisor on progress, potential of trying to use a classifier to evaluate or VADER v Other sentiment analysis libraries

### 26 Jan 2022
* *1 hour* Wrote up meeting minutes from previous meetings that I had not wrote up yet

## Week 4

* Supervisor meeting on the 1st 

### 31 Jan 2022
* *2 hours* Read and collected literature of VADER, NLP and sentiment analysis
* *1 hour* Modularised code used in the jupyter notebooks for analysis
* *2 hours* Produced graphics of Reddit and Twitter terms using TextBlob instead of VADER for comparison
* *1 hour* Made graphs of all runs of Reddit and Twitter

### 1 Feb 2022
* *0.5 hour* Meeting with supervisor

### 3 Feb 2022
* *1 hour* Adding issues to GitHub, updating project boards, committing changes

## Week 5

* Asynchronous meeting on Teams due to supervisor's commitments

### 7 Feb 2022
* *1 hour* Researched Flair as a sentiment analysis tool
* *2 hours* Implemented and tested Flair, created code to run it on databases
* *1 hour* Tried to run on database, kept crashing at the lockdown database so will not be suitable for project
* *1 hour* Researched Afinn, another sentiment analysis library
* *1 hour* Implemented code to run it on the databases, and produced graphics again for each run

### 8 Feb 2022
* *0.5 hour* Asynchronous teams meeting, left all details of my progress

### 13 Feb 2022
* *1 hour* Researched BERT for text classification, looked at previous work
* *1 hour* Looked into the hugging face transformers library for BERT models, provides high scale models for text classification
* *1 hour* During research, some models won't be applicable as lots do not include neutral sentiment

## Week 6

* Meeting on the 15th

### 14 Feb 2022
* *1 hour* Tested out a couple of different models, settled on twitter-roberta-base-sentiment, seems to have very good accuracy for social media posts, 7 million downloads last month
* *2 hours* Ran it on the code structure I have been using for other sentiments, breaks connection as it runs for too long, need to find a way to speed up

### 15 Feb 2022
* *1 hour* Restructured code, got the data from MongoDB first before passing it into BERT rather than at the same time, still taking a while to run but looks like it might work
* *0.5 hour* Meeting with supervisor
* *1 hour* Left notebook running overnight

### 16 Feb 2022
* *1 hour* Changed model to tensorflow to see if that improves time, it made it longer
* *1 hour* Notebook failed overnight on last database due to getting over 512 characters which is BERTs limit, made a function to remove usernames as this was the reason with loads of @'s, and did not provide usefulness to sentiment
* *1 hour* Changed the dictionaries into dataframes as easier to apply the functions to this
* *1 hour* Setup the code again and left running overnight

### 17 Feb 2022
* *1 hour* Failed overnight again, not sure why because I had filtered out the >512 characters, going to introduce padding side and max length into tokenizer

## Week 7

* Meeting on the 22nd

### 21 Feb 2022
* *4 hours* Debugging code to find out where the bert model was failing at, took a while to run and split into lists to finally figure out what was happening
* *1 hour* It was an emoji the system didn't recognise causing it to fail, introduced a try catch finally to stop this interfering, if there is an exception it will now use the emoji function to remove an emoji - hopefully this will be only thing that will cause errors
* *1 hour* Ran the code again and left running overnight

### 22 Feb 2022
* *0.5 hour* Meeting with supervisor
* *1 hour* Graphics were finally produced with bert, classifies a lot of negative posts compared to other models

### 23 Feb 2022
* *1 hour* Fixed BERT model to deal with text > 512, by setting max length in the tokenizer
* *2 hours* Filtered out terms in Reddit dataset that did not contain the search query for first database
* *1 hour* MongoDB error as kept timing out getting a CursorNotFound, changed db into dictionary then put through function to remove from db if term not included
* *0.5 hour* Wrote abstract for dissertation
* *1 hour* Wrote out limitations of project
* *1 hour* Planned out stuff still to finish with dissertation code

### 24 Feb 2022
* *1 hour* Filtered out the terms in databases 2 and 3 for reddit that did not contain the search term - some variable in pushshift can search self text only instead of title
* *0.5 hour* Committed work that had been changed to github

### 25 Feb 2022
* *0.5 hour* Code finished running on run 2 for twitter, inspected graph and ran for 3
* *1 hour* Changed about code in modules to streamline better and for fair experimentation, all in dataframes

### 26 Feb 2022
* *0.5 hour* Inspected graph for run 3
* *0.5 hour* Added in dill to save my variables to a file, save fig to the graphs, and a time variable to track how long it takes to run each database
* *1 hour* Rewrote a shared modules function and wrote a notebook for all bert runs to stop having so many notebooks, ran this but will take a while
* *1 hour* Reviewed dissertations from hall of fame and the lecture from January
* *2 hours* Wrote introduction for dissertation

### 27 Feb 2022
* *1 hour* Started planning background section, going to split categories into two of a bit of background about stuff being used in project, and then mini literature reviews on different parts of the problem
* *3 hours* Wrote first part of background, researched different ways of collecting data as well as short background of NLP and sentiment analysis
* *2 hours* Wrote about data collection of twitter and reddit on related work, this is relevant to project as it is the two social networks this involves

## Week 9

* Meeting on the 1st

### 28 Feb 2022
* *3 hours* Wrote about previous work to do with sentiment analysis with Python libraries
* *3 hours* Wrote about previous work to do with COVID-19 and sentiment analysis

### 2 Mar 2022
* *1 hour* Made functions for VADER, Afinn and TextBlob to use data frames as the previous were to do with taking in a list of dictionaries
* *2 hours* Made notebooks for twitter afinn, textblob and vader to produce for all three runs, ready to execute once bert finished running
* *0.5 hour* Left VADER etc running overnight

### 3 Mar 2022
* *1 hour* GitHub commit broke as the dill variables were too large to push

### 5 Mar 2022
* *1 hour* Reverted commits and deleted the dill variables from repo, pushed to develop branch
* *0.5 hour* Created new reddit analysis feature branch to run all sentiments for reddit, only analysing sentiment at this point but saving the variables for subreddit analysis, changed bert module to take in text

### 6 Mar 2022
* *1 hour* Made reddit bert notebook, ran this over weekend

### 8 Mar 2022
* *0.5 hour* Saved variables and graphs to folder from BERT
* *1 hour* Made notebooks for Afinn, VADER and TextBlob for reddit for all runs and ran this overnight

### 9 Mar 2022
* *0.5 hour* Saved variables and graphs to folder
* *0.5 hour* Merged develop branch with the twitter and reddit notebooks into main
* *0.5 hour* Tidied up code, moving graph images into folders and deleting unnecessary notebooks

## Week 10

* Meeting cancelled this week due to supervisors research

### 14 Mar 2022
* *3 hours* Made wordcloud image code to get back most common words for positive and negative posts for each term for each run

### 15 Mar 2022
* *1 hour* Started analysis on all sentiment, going to investigate time variable first
* *2 hours* Made a function to acquire all the variables from dill for each run and term, and place this in a dictionary for easy access to variables

### 16 Mar 2022
* *1 hour* Gathered the times for the reddit and twitter runs out the dictionaries, through a function made to extract each time and place into pandas dataframe to plot easily
* *1 hour* Function to graph two subplots, one for reddit and one for twitter time, for comparison in seconds on time taken to run
* *3 hours* Made code and functions to graph the sentiment of terms compared to the reddit terms per run
* *2 hours* Graphed the top negative and positive subreddits, one for each library, and for a threshold and just top

### 18 Mar 2022
* *2 hours* Planned out requirements section of dissertation

### 20 Mar 2022
* *3 hours* Set up the testing on Github
* *1 hour* Wrote out requirements section of dissertation

# Week 11

* Meeting cancelled due to supervisors research deadline

### 22 Mar 2022
* *1 hour* Made diagrams for design section of dissertation
* *1 hour* Planned out what I am going to write for design section
* *1 hour* Made graphs for most popular subreddits for each term for each run
* *1 hour* Removed reddit modules that were no longer used and had changed, updated tests
* *0.5 hour* Used coverage with pytest
* *0.5 hour* Removed twitter modules that were never used
* *1 hour* Finalised pytests
* *2 hours* Commented code

### 23 Mar 2022
* *2 hours* Wrote out first part of design, tested positive for covid so was not able to work as much as I thought

### 24 Mar 2022
* *1 hours* Finished writing out design

### 25 Mar 2022
* *4 hours* Wrote out first half of implementation section

### 26 Mar 2022
* *4 hours* Wrote out second half of implementation section

### 27 Mar 2022
* *1 hour* Planned out evaluation section
* *3 hours* Writing part of evaluation section, adding figures and graphs
* *0.5 hour* Had to edit codebase as wanted to change part of time graph layout

# Week 12

* Meeting with supervisor Tuesday

### 28 Mar 2022
* *1 hour* Wrote evaluation about most popular subreddits
* *1 hour* Wrote parts of evaluation
* *1 hour* Had to make a new graph function in code as the library ones were hard to compare in latex
* *3 hours* Wrote evaluation, just need to finish two wee subsections
* *1 hour* Wrote conclusion

### 29 Mar 2022
* *1 hour* Meeting with supervisor, feedback on diss
* *2 hours* Evaluated a test dataset for model accuracy to put in diss, made confusion matrices
* *0.5 hour* Made classification reports on models
* *1 hour* Had to make new graph to compare overall results
* *3 hours* Finished evaluation

### 30 Mar 2022
* *2 hours* Redrafted changes suggested in abstract, intro, background, requirements and design
* *3 hours* Redrafted changed in implementation

### 31 Mar 2022
* *3 hours* Edited read me and manual files to provide guidance
* *1 hour* Supervisor meeting on redraft
* *2 hours* Removed acknowledgements, added more citations to intro, added non-functional requirements
* *3 hours* Redrafted paper
* *2 hours* Code to add more graphs

### 1 Mar 2022
* *3 hours* Video presentations