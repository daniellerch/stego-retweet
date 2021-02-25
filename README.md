# stego-retweet

Stego-retweet is a tool for hiding messages in Twitter using retweets. With this tool you can hide two chars per retweet.


- [stego-retweet](#stego-retweet)
  - [Install](#install)
  - [Configuration](#configuration)
  - [Hide a message](#hide-a-message)
  - [Unhide a message](#unhide-a-message)


## Install

First you need to clone the GIT repository:

```bash
~$ git clone https://github.com/daniellerch/stego-retweet.git
```

Inside the stego-retweet directory you will find a requirements file for installing Python dependencies with pip:

```bash
~$ pip3 install -r requirements.txt
```

After that, you can execute stego-retweet with:

```bash
~$ python3 stegoretweet.py
Usage:
    stegoretweet.py <send> <text>
    stegoretweet.py <send> <text> <hashtag1,hahstag2,hashtagN>
    stegoretweet.py <recv> <user>
```


## Configuration

To use stego-retweet you need a twitter account with an associated application.
Please, go to https://apps.twitter.com/.

When you create an application you obtain some access tokens you have to
configure in the srt/config.py "file".

```bash
TWITTER_CONSUMER_KEY = 'XXX'
TWITTER_CONSUMER_SECRET = 'XXX'
TWITTER_KEY = 'XXX'
TWITTER_SECRET = 'XXX'
```

You can also set some environment variables for the trace level or to select the directory where you want the log to be written.

- The trace level is set by default to `INFO`. You can select another level of detail by executing the following command:

    ```bash
    export TRACE_LEVEL="DEBUG"
    ```
- The directory where the logs were written has a default value of `log`. You can change it by running the following command:

    ```bash
    export LOG_PATH="/home/user/log"
    ```

## Hide a message

To hide a message you have to execute "stegoretweet.py" with the "send" option and the message you want to hide.

Example:
```bash
~$ python3 stegoretweet.py send "hello world!"
Password:
Retweet: 989930938296619008 , search: ignored
Retweet: 989931396696289280 , search: contamination
Retweet: 989930832365346816 , search: varied
Retweet: 989930844587479043 , search: replication
Retweet: 989931572815155200 , search: jobs
Retweet: 989931584651517953 , search: tokyo
```

Using the above command yout are going to retweet whatever tweet that serves to hide the message. To have a little control you can provide a list of hashtags. Stego-retweet will hide information in tweets that contain these hashtags if they are found. Otherwise, stego-retweet will use any other tweet.


Example:
```bash
~$ python3 stegoretweet.py send "hello world!" "crypto,bitcoin,infosec"
Password:
Retweet: 989922919383011328 , search: attended #crypto
Retweet: 988077479037427713 , search: conservation #bitcoin
Retweet: 989915705439961088 , search: particularly #crypto
Retweet: 989930267304517633 , search: headquarters
Retweet: 989119168611082241 , search: fears #crypto
Retweet: 989519586155487233 , search: complicated #bitcoin
```


## Unhide a message
To read a message you have to use the option "recv" and the name of the twitter account of the sender. You need to provide the same password used to send the message.

Example:
```bash
~$ python3 stegoretweet.py recv UserAccount
Password:
r7@8b(hd(,dhello world!
```

You can see some garbage in the results. This is due to retweets that does not contains any hidden information.
