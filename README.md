<h1 align="center">🚀 Hydro Streamer Bot 🌊</h1>

<p align="center">
  <a href="https://github.com/BalaPriyan/HydroStreamerBot">
    <img src="https://telegra.ph/file/a8bb3f6b334ad1200ddb4.png" height="100" width="100" alt="Telegram Logo">
  </a>
</p>

<p align="center">
  <b>Telegram Advanced File to Link Bot (Enterprise Edition)</b><br/>
  Convert files to links for easy streaming and downloading with advanced features using Hydrogram and a fully distributed Microservices Architecture.
</p>

<p align="center">
  <a href="https://github.com/BalaPriyan/HydroStreamerBot/issues">🐞 Report a Bug</a>
  |
  <a href="https://github.com/BalaPriyan/HydroStreamerBot/issues">✨ Request a Feature</a>
</p>

<hr>

<details open="open">
  <summary>📋 Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-this-bot">About This Bot</a>
    </li>
    <li>
      <a href="#architecture-overview">Architecture Overview</a>
    </li>
    <li>
      <a href="#how-to-make-your-own">How to Make Your Own</a>
      <ul>
        <li><a href="#deploy-with-docker-compose-recommended">Deploy with Docker Compose</a></li>
        <li><a href="#deploy-on-heroku">Deploy on Heroku</a></li>
      </ul>
    </li>
    <li><a href="#setting-up-things">Setting Up Things</a></li>
    <ul>
      <li><a href="#mandatory-vars">Mandatory Vars</a></li>
      <li><a href="#optional-vars">Optional Vars</a></li>
    </ul>
    <li><a href="#how-to-use-the-bot">How to Use the Bot</a></li>
    <li><a href="#faq">FAQ</a></li>
    <li><a href="#credits">Credits</a></li>
  </ol>
</details>

## 🤖 About This Bot

### ⚙️ Features
- **Enterprise Microservices**: Dedicated Telegram Bot workers decoupled from High-Performance HTTP streaming web workers via **Gunicorn**.
- **Horizontal Scaling**: Employs **Redis** caching mechanisms for automatic load balancing across `multi_clients`.
- **Live MongoDB Configurations**: Variable settings adapt instantly via MongoDB document syncing without requiring hard container resets.
- **Robust Security**: Employs `aiohttp-ratelimit` spam prevention, Anti-FloodWait sliding windows, explicit CORS policies, and Content-Disposition sanitization.

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

## 🏗️ Architecture Overview

Unlike typical monolothic Telegram streaming bots, HydroStreamer utilizes a robust decoupled ecosystem via Docker:
- `bot_worker`: A lightweight runner specifically handling interactive Telegram inputs using Hydrogram hooks.
- `web_worker`: Scalable Gunicorn-managed worker arrays focused perfectly on maintaining blazing HTTP chunk throughput.
- `redis`: Handles distributed payload sharding dictating precisely which client processes handle a stream globally.
- `nginx`: Custom Reverse Proxy managing bandwidth-intensive chunking, buffering constraints, and port aggregation.

## 🚀 How to Make Your Own

### Deploy with Docker Compose (Recommended)

Since the platform relies heavily on background tasking and distributed load management, **Docker Compose** is the preferred topology framework:

```sh
git clone https://github.com/BalaPriyan/HydroStreamerBot
cd HydroStreamerBot
# Edit your .env variables accordingly
nano .env 
docker-compose up -d --build
```
This single command mounts the `bot_worker`, `web_worker`, `nginx` proxy, and `redis` broker fully network-isolated!

### Deploy on Heroku (Legacy Mono-App)

Press the button below to deploy on Heroku natively using the single-process `web` Procfile fallback:

[![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new-app?template=https://github.com/BalaPriyan/HydroStreamerBot)

## ⚙️ Setting Up Things

Create a `.env` file in the root directory and specify all parameters. Check the examples below.

### 🔐 Mandatory Vars

- **`API_ID` & `API_HASH`**: Acquire from [my.telegram.org](https://my.telegram.org).
- **`BOT_TOKEN`**: Register your token from [@BotFather](https://telegram.dog/BotFather).
- **`BIN_CHANNEL`**: Create a Channel (Private/Public), and attach the ID here.
- **`OWNER_ID`**: Your Telegram User ID.
- **`DATABASE_URL`**: Initial MongoDB connection URI for persistent `FileId` handling and broadcasting configurations.
- **`REDIS_URL`**: Required string addressing the Redis Broker. Default: `redis://redis:6379`.

### 🔧 Optional Vars (Live DB Sync Compatible)
Many of these following vars can be instantiated directly into a MongoDB generic config document (`{"_id": "hydrostreamer_config"}`) to change behaviors globally **without** container restarts.

- **`RUN_MODE`**: `BOT`, `WEB`, or `ALL`. Automatically orchestrated by Docker Compose to segregate workflows.
- **`SLEEP_THRESHOLD`**: Flood wait exception threshold. Defaults to 60 seconds.
- **`WORKERS`**: Maximum concurrent Hydrogram core workers. Defaults to 6.
- **`PORT` & `WEB_SERVER_BIND_ADDRESS`**: Aiohttp binding metrics.
- **`HAS_SSL`**: If `True`, enforces HTTPS return URIs natively. defaults to `False`.
- **`LINK_LIMIT`**: Limit the number of stream links a Free user can actively generate globally.

## 📟 How to Use the Bot

⚠️ **Before using the bot, don't forget to add all the bots (multi-client workers too) to the `BIN_CHANNEL` as administrators.**

- **`/start`**: To check if the bot ecosystem is running smoothly.
- To get an instant stream link, just forward any target media immediately to the bot framework.

## ❓ FAQ

- **How long do the streaming link sessions remain mapped?**
  Links remain permanently active as long as the MongoDB object clusters map directly to the undeleted File source originally published in your Telegram log channel. Don't purge the channel!

## 🤝 Contributing
Feel free to open Pull Requests specifically geared towards the impending React.js frontend dashboard integrations. 

## 🏅 Credits
- [BalaPriyan](https://github.com/BalaPriyan) for the primary HydroGram architectures & microservices updates.
- [Fyaz Mohammed](https://github.com/fyaz05) for commands, stream site, and native layout optimizations.
- [SpringsFern](https://github.com/SpringsFern) for the initial legacy foundations on FileStreamBot.