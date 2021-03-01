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
Tweet with id "1366464152739450883" containing the target "famous" successfully retweeted!
Tweet with id "1366464284268449793" containing the target "singapore" successfully retweeted!
Tweet with id "1366464261376122883" containing the target "lion" successfully retweeted!
Tweet with id "1366464276869902336" containing the target "experiences" successfully retweeted!
Tweet with id "1366449721003413521" containing the target "televisions" successfully retweeted!
Tweet with id "1366464269684862979" containing the target "bouquet" successfully retweeted!
```

Using the above command yout are going to retweet whatever tweet that serves to hide the message. To have a little control you can provide a list of hashtags. Stego-retweet will hide information in tweets that contain these hashtags if they are found. Otherwise, stego-retweet will use any other tweet.


Example:
```bash
~$ python3 stegoretweet.py send "hello world!" "crypto,bitcoin,infosec"
Password:
Tweet with id "989922919383011328" containing the target "attended #crypto" successfully retweeted!
Tweet with id "988077479037427713" containing the target "conservation #bitcoin" successfully retweeted!
Tweet with id "989915705439961088" containing the target "particularly #crypto" successfully retweeted!
Tweet with id "989930267304517633" containing the target "headquarters" successfully retweeted!
Tweet with id "989119168611082241" containing the target "fears #crypto" successfully retweeted!
Tweet with id "989519586155487233" containing the target "complicated #bitcoin" successfully retweeted!
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
