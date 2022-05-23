import tweepy
import private
import datetime, time
import random
import json

# Tweepy Imports
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler

class TwitterStreamer():
  """
  Class for Streaming and Proccessing Live Tweets
  """


  def stream_tweets(self, target_list):
    # This handles twitter auth and connection to twitter streaming api
    auth = OAuthHandler(private.TWITTER_APP_KEY, private.TWITTER_APP_SECRET)
    auth.set_access_token(private.ACCESS_TOKEN,private.ACCESS_TOKEN_SECRET)
    listener = StdOutListener()
    stream = Stream(auth,listener)

    stream.filter(follow=target_list)

  def get_user_id(self,usernames):
    # This fetches the user_id of the tweet author
    auth = OAuthHandler(private.TWITTER_APP_KEY, private.TWITTER_APP_SECRET)
    auth.set_access_token(private.ACCESS_TOKEN,private.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    user = []

    for username in usernames:
      temp = api.get_user(username)
      user.append(temp.id_str)
    return user

  def reply_to_tweet(self, tweet):
    auth = OAuthHandler(private.TWITTER_APP_KEY, private.TWITTER_APP_SECRET)
    auth.set_access_token(private.ACCESS_TOKEN,private.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    current_tweet = json.loads(tweet) # Converts the string object into a JSON format
    tweet_id  = current_tweet.get("id_str")
    user_display_name = current_tweet.get("user").get("screen_name")
    reply_to = current_tweet.get("in_reply_to_status_id_str")
    print(tweet_id)
    print(user_display_name)

    # Randomize Image Index
    random_image = random.randint(1,29)

    # Random Catch Phrase!
    catch_phrases = [
      "Bazinga!",
      "*whispers*",
      "Hey!",
      "What's up.",
      "",
      "",
      "",
      "VSauce! Michael here.",
      "Listen."
    ]
    #Random Body
    tweet_body = [
      "There are around 2 billion species on Earth—with 6.8 million likely to be species of insects. And up to 10 types of bacteria lives inside of each of these insects!",
      "The strings of string instruments were originally made from the guts of animals like sheep or lambs. Now, instrument makers have transitioned to metal wiring. But before metal, it was common for all string instruments to be made from the guts of the animals geographically available to the makers.",
      "In about 20 years, the future could look eerily similar to Wall-E. Artificial intelligence expert Kai-Fu Lee said that 40 percent of human jobs could be replaced by equally capable robots. And drivers might be affected the most.",
      "Water is our body's mechanical oil—without it, it can't function. You lose about 8 percent of your body water while on a flight. This is because the humidity in the climate-controlled environment can be as low as 10 to 15 percent.",
      "Before it became sushi, that tuna could sail through the sea at lightning speed. The fastest speed a tuna can swim has been recorded at over 45 km/h or about 28 mph.",
      "Seems like someone had a tre-moon-dous allergy problem! During the Apollo 17 mission, astronaut Harrison Schmitt found out that he had a severe reaction to moon dust."
    ]

    # Randomize
    random_catch_phrase = random.randint(0, len(catch_phrases)-1)
    random_tweet_body = random.randint(0, len(tweet_body)-1)

    #Generate the tweet
    tweet = "@"+str(user_display_name) + " " + catch_phrases[random_catch_phrase]+ " " + tweet_body[random_tweet_body]
    print(tweet)

    # Get the image to upload
    media = api.media_upload(f"assets/{random_image}.jpg")

    # Initiate the tweet
    if(reply_to is None):
      api.update_status(status=tweet,in_reply_to_status_id=tweet_id,media_ids=[media.media_id])





class StdOutListener(StreamListener):
  """
  Basic listener class that prints the received tweets
  """
  twitter_streamer = TwitterStreamer()

  # Overrides the on_data function. Runs when data is received
  def on_data(self, data):
    try:
      print(data)
      print(isinstance(data,str))
      twitter_streamer.reply_to_tweet(data)
      return True
    except BaseException as e:
      print(f"Error on data: {str(e)}")
    return True
  # Overrides the on_error function. Runs when an error is encountered
  def on_error(self,status):
    print(status)
    return False


# Main Function
if __name__ == "__main__":

  twitter_streamer = TwitterStreamer()

  # Gets the users from the "targets.txt" file
  with open("targets.txt","r") as f:
    content = f.readlines()
  # Appends the users into the target list array
  target_list = [x.strip() for x in content] 
  print(target_list)

  # Initiate the get_user_id function
  targets = twitter_streamer.get_user_id(target_list)
  print(targets)
  
  # Initiate tweet streaming
  twitter_streamer.stream_tweets(targets)

