#   This is for Python 2.7, you can use "2to3" - https://docs.python.org/2/library/2to3.html for python 3 but it will require some tinkering

# This script asks twitch for the top 5 streamers in the "Oldschool Runescape" category (game_id=459931), then it asks for those 
# streamers' follower count, if the follower count is less than 100...but they're the top of the category
# I assume they're viewbotting, it then watches the follower count of the potential phishers and if anybody follows them
# the bot will whisper the potential victim a little warning, mentioning not to click suspicious links...hopefully saving their account.

#   This was my first python project ever, it is not great, I know
#   I did have a more sophisticated way of finding viewbotters, looking at active chatters etc etc but I can't find it, this is a very simple version that only checks if someone is in the top 5 viewers but has less than 100 viewers.

import requests # pip install requests
import json # pip install json
import schedule # pip install schedule
import time # pip install time
import socket   # pip install socket
DoNotDisturbAgain = []  # An array of names that you shouldn't bother again, it gets populated after warning somebody but you can add to it if someone whines.

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "BOT_USERNAME_HERE"
PASS = 'oauth:BOT_OAUTH_HERE'   # Like this 'oauth:OAUTH_HERE'
CHANNEL = "BOT_USERNAME_HERE"

def send_message(msg):
    s.send(bytes("PRIVMSG #" + CHANNEL + " :" + msg + "\r\n")) # Function that sends messages

print("Connecting to host.")
s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n"))
s.send(bytes("NICK " + NICK + "\r\n"))
s.send(bytes("JOIN #" + CHANNEL + " \r\n"))
print("Connected to host")

def PhishFind():
    headers = {
        'Client-ID': 'BOT_CLIENT_ID_HERE',  # Don't forget to add your bot client ID.
    }
    response = requests.get('https://api.twitch.tv/helix/streams?first=5&game_id=459931', headers=headers)  # Ask twitch to get the top 5 Oldschool Runescape streamers currently
    resp = response.json()  # Save their reply
    streams = resp['data']  # Format their reply
    for phishers in streams:    # For each of the top 5 streams from the osrs section
        followerresp = requests.get('https://api.twitch.tv/helix/users/follows?to_id=' + (phishers['user_id']), headers=headers)    # Ask twitch how many followers they have
        followers = followerresp.json() # Save the response
        streams2 = followers['data']    # Format that response
        phisher = (phishers['user_name'])   # Get the usernames of the followers and add them to an array.
        if (followers['total']) < 100:  # If they have less than 100 followers in total...
            print ("\n\nThese people are phishing:\n Username:" + (phishers['user_name']) + "\n Title: " + (phishers['title']) + "\n Viewers: " + str((phishers['viewer_count'])) + "\n Followers: " + str((followers['total'])))   # Write down their name, title and amount of viewers and amount of total followers in the console
            for following in streams2:  # For each of the people following the potential phisher
                follow = following['from_name'] # Add the people following to an array
                if follow not in DoNotDisturbAgain: # If the person following the phisher isn't in the "don't disturb list" then warn them
                    DoNotDisturbAgain.append(follow)    # Add the follower you're about to warn to the "don't disturb" list
                    send_message("/w " + following['from_name'] + " Hi, The stream you followed: " + (phishers['user_name']) + " is actually a fake stream made to steal your Runescape password!") # Whisper the person who followed the Phisher with a warning.
        elif (followers['total']) > 100:    # If the total followers is higher than 100 then, start everything again
            continue


schedule.every(1).minutes.do(PhishFind) # Start the whole process again every minute

while 1:
    schedule.run_pending()  # Keep things looping
    time.sleep(1)
