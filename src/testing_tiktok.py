#!pip install TikTokApi
#!python -m playwright install

from TikTokApi import TikTokApi

verifyFp = "verify_kusi28ku_cEZyRnwz_BBKt_4Kt5_ACCl_b6T8OKici8vB" #expires 2hrs after?

api = TikTokApi.get_instance() #dont check for data as frequent

trending = api.by_trending(count=30, custom_verifyFp=verifyFp)

for tiktok in trending:
    # Prints the id of the tiktok
    print(tiktok['music'])
#print(trending)