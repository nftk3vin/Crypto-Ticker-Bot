# Discord Crypto Ticker Bot (Price or Dominance)

Simple discord bot that sets its nickname to the price of BTC or ETH,
or crypto dominance (BTC.D / ETH.D)  
You can switch mode in `.env`.

Examples:
- BTC   → Shows BTC price + 24h percent change in status
- ETH   → Same thing but for eth
- BTC.D → Shows btc dominance
- ETH.D → Shows eth dominance

## .env file example

BOT_TOKEN=yourbot_token_here
GUILD_ID=1171682017214214184
MODE=BTC

## Install

1. make a folder
2. paste the bot code into `discord_ticker.py`
3. make a `.env` file with the values above

## Run

```bash
pip install discord.py python-dotenv aiohttp
python discord_ticker.py
