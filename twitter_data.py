#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "776833072541020160-mwkdLBwD1Vne5z8wdEZlqf6nv6wE9N3"
access_token_secret = "zApvpdGtH49YmAf4UuVW9Msd8AH03k3wpzWn3H7h5b64f"
consumer_key = "9CvvP18XP8Bh2qKZfuW95arA0"
consumer_secret = "vigk5N5Kr4Zd6O4nq7BAxdDPYJBy0892reVZLDUnbcyxISm6WZ"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['demonetisation','noteban'])