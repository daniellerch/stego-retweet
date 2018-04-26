# stego-retweet

Stego-retweet is a tool for hiding messages in Twitter using retweets and likes. With this tool you can hide two chars per retweet.


- [Install](#install)
- [Configuration](#configuration)
- [Hide a message](#hide-a-message)
- [Unhide a message](#unhide-a-message)


### Install

First you need to clone the GIT repository:

```bash
$ git clone https://github.com/daniellerch/stego-retweet.git
```

Inside the stego-retweet directory you will find a requirements file for installing Python dependencies with pip:

```bash
$ sudo pip install -r requirements.txt 
```

After that, you can execute stego-retweet with:

```bash
$ python stegoretweet.py
Usage:
    stegoretweet.py <send> <text>
    stegoretweet.py <send> <text> <hashtag1,hahstag2,hashtagN>
    stegoretweet.py <recv> <user>
```


### Configuration

To use stego-retweet you need a twitter account with an associated application.
Please, go to https://apps.twitter.com/.

When you create an application you obtain some access tokens you have to
configure in the srt/config.py "file".

```bash
WITTER_CONSUMER_KEY = "XXX"
TWITTER_CONSUMER_SECRET = "XXX"
TWITTER_KEY = "XXX"
TWITTER_SECRET = "XXX"
```


### Hide a message

To hide a message you have to execute "stegoretweet.py" with the "send" option and the message you want to hide.

Example:
```bash
$ python stegoretweet.py send "hello world!"
Retweet: 989844229433233409 , search: wish
Retweet & Like: 989844194750590978 , search: rose
Retweet: 989844176161443841 , search: dick
Retweet: 989844197430751232 , search: neil
Retweet & Like: 989844221032108033 , search: anne
Retweet: 989844244889329664 , search: note
```


### Unhide a message
To read a message you have to use the option "recv" and the name of the twitter account of the sender.

Example:
```bash
$ python stegoretweet.py recv UserAccount
r7@8b(hd(,dhello world!
```

You can see some garbage in the results. This is due to retweets that does not contains any hidden information.







