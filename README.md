# Python-Twitter

**Using the Twitter API with Python (via Twython).**

## Description

This started as me playing with using Twitter from the cli of a Raspberry Pi, and expanded from here into whether I could use Python and the API to do some semi-automated management of lists. The plan was to do more, and I may well do one day, but for now I haven't had the time.

I've now decided to tidy up my code and make it public, since others may find it useful.

## Prerequisites

A great Python to Twitter API module has been created in the form of [Twython](https://github.com/ryanmcgrath/twython), so rather than spend ages trying to make my own interface I have simply used that.

You can install Twython using `pip install twython`.

There may be other Python modules I'm using which aren't part of the standard install, I'll track them down and add them here as I go.

## API Details File

I use a seperate file for my API details which, for obvious reasons, I exclued from my public repository. It therefore needs to be created and populated with your own API credentials.

The file is called TwitterAPIDetails.py and contains the following:

```Python
# Twitter API and Access keys
apiKey = ''
apiSecret = ''
accessToken = ''
accessTokenSecret = ''
```

## Disclaimer

All code provided as is without warranty of any kind, use at your own risk.
