#---------- WORD CLOUDS ----------#
def twitter_wordcloud_terms(df, sentiment):
    wordcloud_terms = " ".join(tweet for tweet in df[df["sentiment"]==sentiment].tweet.astype(str))     # joins the tweets into a string
    return wordcloud_terms