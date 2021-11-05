## 07/10/21

### What I had done since last meeting
* Tried playing around with VADER for sentiment analysis
* Watched and researched Facebook's Graph API, no ability to publicly search posts, would ban IP by scraping
* Created outlook account for project
* Tested TikTok API, not going to work as cannot see comments and have to have TikTok open to search
* Reddit potential with API, got it working so it gets posts containing a term, retrieves comments from post
* Set up Twitter API code similar to reddit and analysed

### Reddit and Twitter API's
* Similarity between these social networks not important
* People will gravitate towards their preferred social platforms so both will have different users
* Minimum of two sources of information - should just work with these two
* If able to make case based on the information then project question is answered
* Sanitising incoming data is most difficult part
* Investigate reddit limits, Twitter has 180 requests then sleeps for 15 mins
* Run scripts for a day then save to MongoDB to store datasets to test, investigate how much it collects
* Ideally filter Reddit for a specific subreddit, any data here more relevant than reddit/all

### VADER for sentiment analysis
* As it is already made library, better than anything we could make from scratch 
* Could run some experiments on the datasets with it, with sanitised and unsanitised input
* Already gives compound values which is useful because we want scalar value metric to make comparisons and average of these values
* Look at accuracy of VADER

### Questions
* VADER uses entire text for sentiment analysis - i.e. wouldn't be able to tokenise as uses capitals for emphasis etc.
- Test this out checking how it classifies with lower case text and without
* Is Reddit and Twitter to similar social medias to investigate?
- Similarity of these not important 
* Tweets from Twitter API contain other info like location etc - should I be storing any of these?
- Focus on text right now, possible to change based on progress of project, could maybe get locations to see where opinions come from
* If pulling comments on a Reddit post, should the comments also contain the search term?
- Can be assumed, but maybe look at specific subreddits on topic to get more meaningful data, however this could be bias

### For the next meeting
* Keep going with sentiment analysis
* Have a look at trying to run dataset for a length of time, save to MongoDB