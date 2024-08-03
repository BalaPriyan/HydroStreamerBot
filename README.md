<h1 align="center">🚀 Hydro Streamer Bot 🌊</h1>

<p align="center">
  <a href="https://github.com/BalaPriyan/HydroStreamerBot">
    <img src="https://telegra.ph/file/a8bb3f6b334ad1200ddb4.png" height="100" width="100" alt="Telegram Logo">
  </a>
</p>

<p align="center">
  <b>Telegram Advanced File to Link Bot</b><br/>
  Convert files to links for easy streaming and downloading with advanced features using Hydrogram.
</p>

<p align="center">
  <a href="https://github.com/BalaPriyan/issues">🐞 Report a Bug</a>
  |
  <a href="https://github.com/BalaPriyan/issues">✨ Request a Feature</a>
</p>

<hr>

<details open="open">
  <summary>📋 Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-this-bot">About This Bot</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#original-repository">Original Repository</a></li>
      </ul>
    </li>
    <li>
      <a href="#how-to-make-your-own">How to Make Your Own</a>
      <ul>
        <li><a href="#deploy-on-heroku">Deploy on Heroku</a></li>
        <li><a href="#host-it-on-vps-or-locally">Run It in a VPS / Locally</a></li>
      </ul>
    </li>
    <li><a href="#setting-up-things">Setting Up Things</a></li>
    <ul>
      <li><a href="#mandatory-vars">Mandatory Vars</a></li>
      <li><a href="#optional-vars">Optional Vars</a></li>
    </ul>
    <li><a href="#how-to-use-the-bot">How to Use the Bot</a></li>
    <li><a href="#faq">FAQ</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact-me">Contact Me</a></li>
    <li><a href="#credits">Credits</a></li>
  </ol>
</details>

## 🤖 About This Bot

### ⚙️ Features

- **Streamlined Code**: Unnecessary features removed for efficiency. 
- **High Speed**: Utilizes Hydrogram for faster operation.
- **Easy Deployment**: Fully configured for Heroku.
- **Enhanced Functionality**: Improved user interface and additional features:

  - 👤 **User-Friendly Interface**
  - 🔗 **Stream Links**
  - 👥 **Group Functionality**
  - 📂 **Retrieve Files**
  - 🔄 **Update Channel**
  - 📋 **Log Channel**
  - ⚖️ **Terms & Conditions**
  - ❌ **Delete Links**
  - 📢 **Broadcasts (Admin)**
  - 🚫 **Ban User (Admin)**
  - ✅ **Unban User (Admin)**
  - 🔢 **Link Limits**

### 💻 Bot Commands

<details>
  <summary><strong>View All Commands</strong> <sup><kbd>(Click to expand)</kbd></sup></summary>

```
start - Start the bot
link - Generate a stream link
help - Bot usage details
myfiles - Retrieve all files
ban - (Admin) Ban users
unban - (Admin) Unban users
stats - (Admin) Bot usage stats
who - (Admin) Check sender of a file
```

</details>

## 🎥 Original Repository

[HydroStreamerBot](https://github.com/BalaPriyan/HydroStreamerBot) is a modified version of [FileStreamBot](https://github.com/SpringsFern/FileStreamBot).

## 🚀 How to Make Your Own

### Deploy on Heroku

Press the button below to deploy on Heroku:

[![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new-app?template=https://github.com/BalaPriyan/HydroStreamerBot)

Then go to the [variables tab](#mandatory-vars) for more info on setting up environmental variables.

### Host It on VPS or Locally

```sh
git clone https://github.com/BalaPriyan/HydroStreamerBot
cd HydroStreamerBot
python3 -m venv ./venv
. ./venv/bin/activate
pip3 install -r requirements.txt
python3 -m WebStreamer
```

To stop the bot:

```sh
Ctrl + C
```

If you want to run the bot 24/7 on VPS:

```sh
sudo apt install tmux -y
tmux
python3 -m WebStreamer
```

Now you can close the VPS, and the bot will keep running.

## ⚙️ Setting Up Things

If you're on Heroku, just add these to the Environmental Variables. If you're hosting locally, create a `.env` file in the root directory and add all the variables there. Example `.env` file:

```sh
API_ID=
API_HASH=
BOT_TOKEN=
BIN_CHANNEL=
DATABASE_URL=
FQDN=
HAS_SSL=
MULTI_TOKEN1=
MULTI_TOKEN2=
MULTI_TOKEN3=
OWNER_ID=
PORT=
```

### 🔐 Mandatory Vars

- **`API_ID`**: Get it from [my.telegram.org](https://my.telegram.org).
- **`API_HASH`**: Get it from [my.telegram.org](https://my.telegram.org).
- **`BOT_TOKEN`**: Get the bot token from [@BotFather](https://telegram.dog/BotFather).
- **`BIN_CHANNEL`**: Create a new channel (private/public), post something in your channel, forward that post to [@missrose_bot](https://telegram.dog/MissRose_bot), and reply with `/id`. Copy the forwarded channel ID here.
- **`OWNER_ID`**: Your Telegram User ID. Send `/id` to [@missrose_bot](https://telegram.dog/MissRose_bot) to get it.
- **`DATABASE_URL`**: MongoDB URI for saving user IDs for broadcasting.

### 🔧 Optional Vars

- **`SLEEP_THRESHOLD`**: Flood wait exception threshold. Defaults to 60 seconds.
- **`WORKERS`**: Maximum concurrent workers. Defaults to 6.
- **`PORT`**: Port for the web app. Defaults to 8080.
- **`WEB_SERVER_BIND_ADDRESS`**: Server bind address. Defaults to `0.0.0.0`.
- **`NO_PORT`**: If `True`, the port is not displayed. Defaults to `False`.
- **`FQDN`**: Fully Qualified Domain Name. Defaults to `WEB_SERVER_BIND_ADDRESS`.
- **`HAS_SSL`**: If `True`, generated links are in HTTPS format. Defaults to `False`.
- **`PING_INTERVAL`**: Time for server pings. Defaults to 1200 ms.
- **`UPDATES_CHANNEL`**: Telegram channel username without `@`.
- **`FORCE_UPDATES_CHANNEL`**: If `True`, users must join the update channel to use the bot.
- **`SESSION_NAME`**: Database name. Defaults to `HydroStreamerBot`.
- **`ALLOWED_USERS`**: User Telegram IDs allowed to use the bot.
- **`KEEP_ALIVE`**: If `True`, the server pings itself every few minutes.
- **`IMAGE_FILEID`**: Photo to send with `/myfiles`. Use file_id or an HTTP URL.
- **`TOS`**: URL to your Terms of Service.
- **`MODE`**: Set to `secondary` to use the server only for serving files.
- **`LINK_LIMIT`**: Limit the number of links a user can generate.

## 📟 How to Use the Bot

⚠️ **Before using the bot, don't forget to add all the bots (multi-client ones too) to the `BIN_CHANNEL` as admins.**

- **`/start`**: To check if the bot is alive.
- To get an instant stream link, just forward any media to the bot.

## ❓ FAQ

- **How long do the links remain valid?**

  Links remain valid as long as your bot is running and you haven't deleted the log channel.

## 🤝 Contributing

Feel free to contribute to this project if you have any ideas!

## 📬 Contact Me

[![Telegram Channel](https://img.shields.io/static/v1?label=Join&message=Telegram%20Channel&color=blueviolet&style=for-the-badge&logo=telegram&logoColor=violet)](https://t.me/BalapriyanBots)

## 🏅 Credits

- [Me](https://github.com/BalaPriyan) for migrating to HydroGram
- [Fyaz Mohammed](https://github.com/fyaz05) for commands, stream site, and optimizations
- [SpringsFern](https://github.com/SpringsFern) for [FileStreamBot](https://github.com/SpringsFern/FileStreamBot)
- [eyaadh](https://github.com/eyaadh) for some files