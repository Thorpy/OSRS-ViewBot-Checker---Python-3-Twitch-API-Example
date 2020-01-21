# OSRS-Phish-Viewbot-Finder---Python-2.7
This is a Python script that logs a bot into twitch that will look for potential viewbotters in the OSRS category and will warn anybody that follows their channel that the video is most likely a phishing scam and not to click any links.


My first project (from a while ago) to learn some python, it's not perfect but it works..kind of

![Image of bot from CMD](https://i.imgur.com/WBgcvIy.png)
![Image of bot whispering follower](https://i.imgur.com/wS12drE.png)

You will need to "pip install" the imports.
This bot only works with Python 2.7, you "can" use "2to3" to convert it but it isn't perfect and will probably require some editing:
https://docs.python.org/2/library/2to3.html

The bot's connection to twitch IRC will be broken sometimes (I think twitch kicks it out)
In order to fix this I used a simple shellscript that checked to see if the python process was alive or not, if not it'd restart the script.
This ran on a raspberry pi behind my monitors uninterrupted for a year.

This is purely for a personal backup and to be a (albeit badly written) example of how to interact with the twitch api using python.
