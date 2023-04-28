from discord.ext import commands
import discord
import traceback

from marketplaces import eBay, StockX, Goat, Depop, Grailed

TOKEN = '<YOUR TOKEN>'
CHANNEL_ID = 0

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command('prices')
async def market_places(ctx, *args):
    if ctx.channel.id != CHANNEL_ID:
        return
    args = ' '.join(args)

    embed = discord.Embed(
        title='Prices across Marketplaces',
        description=f'Prices for query: "{args}"'
    )
    try:
        stockx_prices = StockX(args).get_prices()
        embed.add_field(name='[StockX] Average DS Price', value=f"[Link](https://stockx.com/{stockx_prices['urlKey']}) ${stockx_prices['market']['averageDeadstockPrice']}")
        embed.set_image(
        url=stockx_prices['media']['imageUrl']
    )
    except:
        print(traceback.format_exc())
        embed.add_field(name='[StockX] Average DS Price', value='Something went wrong')

    try:
        ebay_sold_prices = eBay(args).get_sold_prices()
        embed.add_field(name=f'[eBay] Average Sold Price', value=f"[Link](https://www.ebay.co.uk/sch/i.html?_nkw={args.replace(' ', '+')}&_ipg=200&rt=nc&LH_Sold=1) ${int(ebay_sold_prices)}")
    except:
        print(traceback.format_exc())
        embed.add_field(name='[eBay] Average Sold Price', value='Something went wrong')

    try:
        ebay_current_prices = eBay(args).get_current_prices()
        embed.add_field(name=f'[eBay] Average Listed Price', value=f"[Link](https://www.ebay.co.uk/sch/i.html?_nkw={args.replace(' ', '+')}&_ipg=200) ${int(ebay_current_prices)}")
    except:
        print(traceback.format_exc())
        embed.add_field(name='[eBay] Average Listed Price', value='Something went wrong')

    try:
        goat_prices = Goat(args).get_prices()
        embed.add_field(name=f'[GOAT] Lowest Listed Price', value=f"[Link](https://www.goat.com/sneakers/{goat_prices['slug']}) ${int(goat_prices['lowest_price_cents']/100)}")
    except:
        print(traceback.format_exc())
        embed.add_field(name='[GOAT] Lowest Listed Price', value='Something went wrong')

    try:
        depop_prices = Depop(args).get_prices()
        embed.add_field(name=f'[Depop] Average Listed Price', value=f"[Link](https://www.depop.com/search/?q={args.replace(' ', '%20')}) ${int(depop_prices)}")
    except:
        print(traceback.format_exc())
        embed.add_field(name='[Depop] Average Listed Price', value='Something went wrong')

    try:
        grailed_prices = Grailed(args).get_prices()
        grailed_url = Grailed(args).get_url()
        embed.add_field(name=f'[Grailed] Average Listed Price', value=f"[Link]({grailed_url}) ${grailed_prices['facets_stats']['price_i']['avg']}")
    except:
        print(traceback.format_exc())
        embed.add_field(name='[Grailed] Average Listed Price', value='Something went wrong')
    await ctx.send(embed=embed)



if __name__ == '__main__':
    bot.run(TOKEN)