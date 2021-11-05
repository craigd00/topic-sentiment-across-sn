from TikTokApi import TikTokApi
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging

verifyFp = "verify_kusi28ku_cEZyRnwz_BBKt_4Kt5_ACCl_b6T8OKici8vB" #expires 2hrs after?

api = TikTokApi.get_instance(logging_level=logging.INFO, use_test_endpoints=True) #dont check for data as frequent

tiktoks = api.by_hashtag('donaldtrump', count=30, custom_verifyFp=verifyFp)

tiktok_titles = []
for tiktok in tiktoks:
    tiktok_titles.append(tiktok['desc'])
    print(tiktok['desc'])

#works sometimes, the data might be inaccurate and sometimes fails for unknown reasons

analyzer = SentimentIntensityAnalyzer()
# Example code:

f = open("tiktok_scores.txt", "x", encoding="utf-8")

for tiktok_post in tiktok_titles:
  vs = analyzer.polarity_scores(tiktok_post)
  compound = vs['compound']
  sentiment_score = compound * 100
  print("The post '" + tiktok_post + "' has a sentiment score of: " + (str(sentiment_score)) + "%")
  
  if (compound >= 0.05):
    print("The post was POSITIVE")
    f.write("\n" + tiktok_post + ": RESULT = POSITIVE")
  elif (compound <= -0.05):
    print("The post was NEGATIVE")
    f.write("\n" + tiktok_post + ": RESULT = NEGATIVE")
  else:
    print("The post was NEUTRAL")
    f.write("\n" + tiktok_post + ": RESULT = NEUTRAL")
  print("{:-<65} {}".format(tiktok_post, str(vs)))

f.close()