

<b>Description:</b>

This bot was created for getting status of Minecraft Server.

<b>Deploy to Heroku:</b>

This version of bot is intended for deploying to Heroku.
Before deploying it to Heroku create your app there and create environment vars (Settings -> Reveal Config Vars): 
<ul>
  <li>BOT_TOKEN - your Telegram bot token got by <a href="https://t.me/BotFather">BotFather</a></li>
  <li>BOT_USERNAME - your Telegram bot @username</li>
  <li>HEROKU_APP_NAME - name of your Heroku app</li>
  <li>IPADDR - your Minecraft server (ip:port)</li>
</ul>

Connect your web-app to <a href="https://uptimerobot.com/">UptimeRobot</a>

<b>Bot commands:</b>

<code>/help</code>, <code>/start</code> - opens help menu

<code>/status</code> - shows current status (online/offline), IP, MOTD (description), current online, max online and version of Minecraft server and shows last update of this information
