import os, asyncio, aiohttp, discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
MODE = os.getenv("MODE", "BTC")

intents = discord.Intents.default()
intents.guilds=True
intents.members=True
intents.presences=True

client = discord.Client(intents=intents)

def format_price(num):
    return f"{num:,.0f}"


async def fetch_json(session, url):
    async with session.get(url, timeout = 10) as r:
        r.raise_for_status()
        data = await r.json()
        return data


async def updater_loop():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print("bot not in server? check id?")
        await client.close()
        return

    async with aiohttp.ClientSession() as session:
        while not client.is_closed():
            try:
                if MODE == "BTC" or MODE == "ETH":

                    if MODE == "BTC":
                        symbol = "BTCUSDT"
                    else:
                        symbol="ETHUSDT"

                    j = await fetch_json(session, f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}")

                    price = float(j["lastPrice"])
                    percent = float(j["priceChangePercent"])


                    nick_name = format_price(price)

                    await guild.me.edit(nick = nick_name)

                    change = f"{'+' if percent >= 0 else ''}{percent:.2f}%" # makes +4.20%
                    await client.change_presence(
                        activity = discord.CustomActivity(name = change),
                        status=discord.Status.online
                    )

                    wait = 120
                else:
                    j = await fetch_json(session,"https://api.coingecko.com/api/v3/global")

                    if MODE == "BTC.D":
                        key = "btc"
                    else:
                        key = "eth"

                    dom = float(j["data"]["market_cap_percentage"][key])

                    await guild.me.edit(nick=f"{dom:.1f}%")

                    await client.change_presence(
                        activity = discord.CustomActivity(name=MODE),
                        status = discord.Status.online
                    )

                    wait = 3600

            except Exception as e:
                print("oop error:", e)
                wait = 60 # retry in 1 min

            await asyncio.sleep(wait)


@client.event
async def on_ready():
    print("logged in as", client.user, " MODE:", MODE)
    asyncio.create_task(updater_loop()) # start looping


client.run(TOKEN)
