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
      "What's up amigo!",
      "*whispers*",
      "Hey stupid!",
      "",
      "",
      "",
      "",
      "Hey dumbass!",
      "Listen here you imbecile!"
    ]
    #Random Body
    tweet_body = [
      "I am from the FBI, and I have been assigned to monitor twitter users who lack common sense. The fact that I'm replying to this tweet indicates something that you should get by now. Edson over and out.",
      "I'm from the future where everyone's turned into malnourished skinheads mainly because of the series of events that this idiotic tweet that you put out caused. I just came here to tell you that so you can maybe carefully think over the next tweets you're gonna put out.",
      "This tweet embodies every living person in the Lizard-ruled earth in the year 2046's way of thinking, daft and counter-productive. Maybe you should learn how organize your thoughts better before tweeting. (_)_)::::::::)~~~ <--- Rocket Ship",
      "Your desperate attempt to sound like an intellectual person by using words that no normal human being in the year 2020 uses reeks of idiocracy. How can you think that just by sounding like an overly-compensating asshole, people will actuall support you."
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

