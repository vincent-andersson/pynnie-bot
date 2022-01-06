import os
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
from twitter_monitor import *
from discord_webhook import DiscordWebhook, DiscordEmbed

client = commands.Bot(command_prefix='/')

userList = []
past_tweets = {}

@client.event
async def on_ready():
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/927918925130391573/6Iwyo63_7lFJ2s8y1Rjsy9Tu29OduJnfu_YQIWHaNQMNZiFcqcL7DEPoioLgoSGI56uf')
    embed = DiscordEmbed(title="Twitter Monitor", description="Pynnie Bot is now online!", color=0xe4ede0)
    webhook.add_embed(embed)
    webhook.execute()
    print('{0.user} is now online!'.format(client))

@client.command()
async def start(ctx):
    start_monitor()

@client.command()
async def stop(ctx, arg):
    stop_monitoring(arg)

@client.command()
async def add(ctx, arg):
    userList.append(arg)
    started_monitoring(arg)

def started_monitoring(user):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/927918925130391573/6Iwyo63_7lFJ2s8y1Rjsy9Tu29OduJnfu_YQIWHaNQMNZiFcqcL7DEPoioLgoSGI56uf')
    startEmbed = DiscordEmbed(title="Twitter Monitor", description="Started monitoring {}".format(user), color=0x58d763)
    webhook.add_embed(startEmbed)
    webhook.execute()
    print('Started monitoring {}'.format(user))

def send_tweet(tweet):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/927918925130391573/6Iwyo63_7lFJ2s8y1Rjsy9Tu29OduJnfu_YQIWHaNQMNZiFcqcL7DEPoioLgoSGI56uf')
    url = 'https://twitter.com/twitter/statuses/' + tweet.id_str
    tweetEmbed = DiscordEmbed(title="New Tweet by {}".format(tweet.user.screen_name), description=tweet.text, url=url, color=0x00ACEE)
    webhook.add_embed(tweetEmbed)
    webhook.execute()

def stop_monitoring(user):
    userList.remove(user)
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/927918925130391573/6Iwyo63_7lFJ2s8y1Rjsy9Tu29OduJnfu_YQIWHaNQMNZiFcqcL7DEPoioLgoSGI56uf')
    stopEmbed = DiscordEmbed(title="Twitter Monitor", description="Stopped monitoring {}".format(user), color=0xFF0000)
    webhook.add_embed(stopEmbed)
    webhook.execute()
    print('Stopped monitoring {}'.format(user))

@tasks.loop(seconds=1.0)
async def check_users(api):
    for user in userList:
        tweets = api.user_timeline(screen_name=user, count=1)

        if len(tweets) > 0:
            if tweets[0].id not in past_tweets.keys():
                print(tweets[0].text)
                send_tweet(tweets[0])
                past_tweets[tweets[0].id] = tweets[0].text

def start_monitor():
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    check_users.start(api)

if __name__ == "__main__":
    load_dotenv()
    client.run(os.getenv('TOKEN'))