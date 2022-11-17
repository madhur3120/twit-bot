import discord
from discord.ext import commands
from tweepy_setup import *
import tweepy


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot Is Online")

@bot.command()
async def ping(ctx, arg1):
    id = get_user_id(arg1)
    t = last_tweet(id)
    likes_count(id)
    # print(t)
    await ctx.reply(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def twit(ctx):
    r = requests.get("https://api.twitter.com/2/users/:id/tweets")
    res = r.json()
    em = discord.Embed()
    em.set_image(url=res['message'])
    await ctx.send(embed=em)





# @bot.event
# async def on_message(message):
#     if message.content == "Hello".lower():
#         await message.channel.send("Hey!")

# @bot.event
# async def on_member_join(member):
#     channel = member.guild.system_channel
#     await channel.send(f"{member.mention} Welcome to the Server")

# @bot.event
# async def on_member_remove(member):
#     channel = member.guild.system_channel
#     await channel.send(f"GoodBye {member.mention}")   





bot.run("MTA0MjUyOTM5MTMyODEwNDQ4OA.GLtS6q.DWTFb_GoezczLuERxTgxRs5E62SnJX7EJeyKAs")