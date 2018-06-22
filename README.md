# Telegram-Bot

This is a Python script which uses the [official Telegram Bot API](https://core.telegram.org/bots/api)
to send messages from the command line.


## Install

First you need to get a bot token from the [Bot Father](https://telegram.me/BotFather).

Then you can run `$ sudo python setup.py [bot token]` which will create a configuration directory under `/etc/telegram-bot` 
and install a copy of the `telegram-bot.py` under `/usr/bin`.

## Adding Users

In order to send messages from the bot, a user has to contact the bot first.
Search your bot on Telegram and send the message "_Add me_".

Now run `$ sudo python add-new-user.py`.
This script will see the new users and will prompt you if you want to add them to the configuration file.

## Sending Messages

Send a simple message like this:

`$ telegram-bot -u @username -t "Hello, World!"`

Pipe text from `stdin`:

`$ echo "Hello, World!" | telegram-bot -u @username -p`

### Styling

The script supports styling with markdown or html. Just use the `--parsing` option:

`$ telegram-bot -u @username -t "*bold*" --parsing "markdown"`

### Other Options

You can send a message silently (users will receive a notification without sound):

`$ telegram-bot -u @username -t "sneaky" --disable-notification`

When sending URLs there is the option to disable the link preview and just send the URL:

`$ telegram-bot -u @username -t "https://telegram.org" --disable-preview`

---

## Informations

#### Can I send **images** or **files** with this program?

No, (at least not yet).

#### Can I **receive** messages with this program?

No. This is meant for sending messages (like status updates) only.

#### Can I enable webhooks on another program to receive messages?

You can. But be aware that `add-new-user.py` depends on the `getUpdates` method, which will be disabled when webhooks are enabled. Read more in the official API documentation: [Getting Updates](https://core.telegram.org/bots/api#getting-updates)

#### Can I use the same token for multiple devices?

Yes you can. Telegram users will only see your bot however.

#### Are group chats and channels supported?

Yes. You don't have to send the "Add me" command though, just add your bot to the group or channel and run `sudo python add-new-user.py` again.

#### How **secure** are those messages?

The content of the message is sent inside the a `POST`-request over https. So it is fairly secured.
Your bot token however is always sent inside the URL as per API requirements.

> _"All queries to the Telegram Bot API must be served over HTTPS and need to be presented in this form: `https://api.telegram.org/bot<token>/METHOD_NAME`
."_

---

## Examples

#### root-login notifier

Add the following line to your `/root/.bashrc`

```bash
echo "someone just loged in as root! \n" `who -u` | telegram-bot -u @username -s
```

#### reboot notifier

Add the following line to your cronjobs

```bash
@reboot telegram-bot -u @username -t "I just rebooted"
```

#### Other examples

[Digitec Daily Offer](https://t.me/digitecdaily)

