from src.shared_modules import bert_preprocess, process_emoji

def test_bert_preprocess():
    post = "@PiersMorgan https://twitter.com please delete your account"

    processed = bert_preprocess(post)
   
    assert processed == " http please delete your account"


def test_emoji_regex():
    post = "Today is a great day😀"

    remove_emoji = process_emoji(post)

    assert remove_emoji == "Today is a great day"