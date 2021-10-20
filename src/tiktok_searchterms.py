from TikTokApi import TikTokApi
import logging
verifyFp = "verify_kusi28ku_cEZyRnwz_BBKt_4Kt5_ACCl_b6T8OKici8vB" #expires 2hrs after?

api = TikTokApi.get_instance(logging_level=logging.INFO, use_test_endpoints=True) #dont check for data as frequent

tiktoks = api.by_hashtag('donaldtrump', count=30, custom_verifyFp=verifyFp)

for tiktok in tiktoks:
    print(tiktok['desc'])
#print(tiktoks)

#works sometimes, the data might be inaccurate and sometimes fails for unknown reasons