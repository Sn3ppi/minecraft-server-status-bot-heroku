<b>Description:</b>

This bot was created for getting status of Dreammita server. See https://t.me/dreammita.
This version of bot is intended for deploying to Heroku.
Before deploying it to Heroku create your app there and create environment vars (Settings -> Reveal Config Vars): 

BOT_TOKEN - your Telegram bot token got by https://t.me/BotFather

HEROKU_APP_NAME - name of your Heroku app

IPADDR - your Minecraft server (ip:port)

<b>Bot commands:</b>

/help, /start - opens help menu

/status - shows current status (online/offline), IP, MOTD (description), current online, max online and version of Minecraft server and shows last update of this information

