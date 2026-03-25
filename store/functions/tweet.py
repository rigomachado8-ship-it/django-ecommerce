import os
from requests_oauthlib import OAuth1Session

class Tweet:
    def __init__(self):
        self.oauth = None
        self.authenticate()

    def authenticate(self):
        consumer_key = os.getenv("X_CONSUMER_KEY")
        consumer_secret = os.getenv("X_CONSUMER_SECRET")
        access_token = os.getenv("X_ACCESS_TOKEN")
        access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

        if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
            print("Twitter/X keys not set. Tweeting disabled.")
            return

        self.oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

    def make_tweet(self, text):
        if not self.oauth:
            print("Skipping tweet (no API keys)")
            return

        response = self.oauth.post(
            "https://api.twitter.com/1.1/statuses/update.json",
            data={"status": text}
        )

        print("Tweet response:", response.status_code)