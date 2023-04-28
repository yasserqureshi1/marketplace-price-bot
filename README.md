# Marketplace Compare Tool 

## About this Project

This repo contains a Discord bot that allows you to quickly and easily compare prices across popular marketplaces such as StockX, GOAT, Grailed, eBay, and Depop. 

With just a simple query, you can access real-time pricing information from multiple platforms, which can help you make informed decisions about where to list your items. It can also help you identify potential arbitrage opportunities, allowing you to capitalize on price differences between platforms and make some extra cash.

## Set-Up

1. Download or Clone this repo

2. Install the dependencies:
```
pip install -r requirements.txt
```
3. Create a Discord bot via the Discord Developer Portal and add it to your Discord server

4. Paste your bot token into `bot.py` (line 7):
```
TOKEN = '<YOUR TOKEN>'
```

5. Copy the channel ID of the channel you want your bot to work in and paste it into `bot.py` (line 8)
```
CHANNEL_ID = XXXXXXXXX
```

6. Run `bot.py` using the command:
```
python bot.py
```
Or for MacOS and Linux:
```
python3 bot.py
```

