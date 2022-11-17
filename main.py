import discord
from discord.ext import commands
from tweepy_setup import *
import tweepy
import pymongo
from datetime import datetime, timedelta

client = pymongo.MongoClient("mongodb+srv://Abhay:Abhay123@cluster0.bba05gv.mongodb.net/?retryWrites=true&w=majority")
db = client.users

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot Is Online")

@bot.command()
async def register(ctx, arg1):
    res, err = get_user_id(arg1)
    if err!="" :
        await ctx.reply(f"Username is invalid! {round(bot.latency * 1000)}ms")
    else:
        db.user_instance.insert_one({
            "username" : arg1,
            "serverId": ctx.guild.id,
            "end_time": datetime.today() + timedelta(seconds=15),
        })
        # db.users.insert_one({
        #     "username" : arg1,
        #     "twitterId": res,
        #     "serverId": ctx.guild.id
        # })
        # # await ctx.reply(f"Pong! {round(bot.latency * 1000)}ms")
        # await ctx.reply(f"User Registered {round(bot.latency * 1000)}ms")

@bot.command()
async def leaderboard(ctx):
    def cmp(ele):
        return ele['likes']
    users = db.users.find()
    scores = []
    for user in users:
        print(user["username"])
        scores.append({"username": user["username"], "likes": likes_count(user["twitterId"])})
    scores.sort(key=cmp, reverse=True)
    print(scores)
    await ctx.reply(f"Leaderboard")
# @bot.command()
# async def twit(ctx):
#     r = requests.get("https://api.twitter.com/2/users/:id/tweets")
#     res = r.json()
#     em = discord.Embed()
#     em.set_image(url=res['message'])
#     await ctx.send(embed=em)





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