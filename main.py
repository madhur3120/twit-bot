import discord
from discord.ext import commands
from tweepy_setup import *
import pymongo
from datetime import datetime
import certifi

client = pymongo.MongoClient(
    "mongodb+srv://Abhay:Abhay123@cluster0.bba05gv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.users

db.register_instances.create_index("inserted", expireAfterSeconds=120)
db.follow_instances.create_index("inserted", expireAfterSeconds=120)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot Is Online")


@bot.command()
async def register(ctx, arg1):
    res, err = get_user_id(arg1)
    print(ctx.message.author.id)
    discordId=ctx.message.author.id
    if err != "":
        await ctx.reply(f"Username is invalid!")
    else:
        try:
            register_instance = db.register_instances.find_one({"serverId" : ctx.guild.id})
            print("register_instance ",register_instance)
            if register_instance==None:
                db.register_instances.insert_one({
                    "username": arg1,
                    "discordId": discordId,
                    "twitterId": res,
                    "serverId": ctx.guild.id,
                    "inserted": datetime.utcnow()})
                await ctx.reply(f"tweet something!")
            else:
                await ctx.reply(f"You have already registered!")
        except Exception as e:
            print("Exception ",e)


@bot.command()
async def verify(ctx, arg1):
    serverId = ctx.guild.id
    discordId=ctx.message.author.id
    try:
        register_instance = db.register_instances.find_one({"serverId": serverId})
        lastTweetContent = last_tweet(register_instance["twitterId"])
        print(lastTweetContent)
        if lastTweetContent != arg1:
            await ctx.reply(f"Content didn't match with your last tweet!")
        else:
            try:
                db.users.insert_one({
                    "username": register_instance["username"],
                    "discordId": discordId,
                    "twitterId": register_instance["twitterId"],
                    "serverId": ctx.guild.id,
                    "coins": 5000
                })
                await ctx.reply(f"User registered!")
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        await ctx.reply(f"User instance not found in database!")


@bot.command()
async def leaderboard(ctx, arg1):
    def cmp(ele):
        return ele['likes']
    users = db.users.find()
    scores = []
    for user in users:
        print(user["username"])
        scores.append(
            {"username": user["username"], "likes": likes_count(user["twitterId"])})
    scores.sort(key=cmp, reverse=True)
    print(scores)
    if len(scores) < int(arg1):
        await ctx.reply("Entered number is more than the users present in database.")
        arg1 = len(scores)

    em = discord.Embed(title=f"Top {arg1} Richest People",
                       description="This is based on the number of likes on twitter", color=discord.Color(0xfa43ee))
    index = 1
    for score in scores:
        em.add_field(name=f"{score['username']}",
                     value=f"likes: {score['likes']}", inline=False)
        if index == int(arg1):
            break
        else:
            index += 1
    await ctx.send(embed=em)


@bot.command()
async def follow(ctx, arg):
    try:
        userRequesting = db.users.find_one({"serverId": ctx.guild.id})
        try:
            userRequested = db.users.find_one({"username": arg})
            channel = ctx.guild.system_channel
            db.follow_instances.insert_one({
                "requestingUserTwitterId": userRequesting["twitterId"],
                "requestedUserTwitterId": userRequested["twitterId"],
            })
            await channel.send(f"{arg.mention} Follow {userRequesting['username']} to earn 50 coins.")
        except:
            await ctx.reply("User you are requesting is not registered")
    except:
        await ctx.reply("You are not registered")

@bot.command()
async def followed(ctx, arg):
    try:
        userFollowing = db.users.find_one({"serverId": ctx.guild.id})
        try:
            userFollowed = db.users.find_one({"username": arg})
            request = db.request_instances.find_one({
                "$and" : [
                    {"requestingUserTwitterId": userFollowed["twitterId"]},
                    {"requestedUserTwitterId": userFollowed["twitterId"]}
                ]
            })
        except:
            await ctx.reply("User you are following is not registered")
    except:
        await ctx.reply("You are not registered")


@bot.command()
async def profile(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    user_data = db.users.find_one({"$and":[
        {"discordId": member.id},
        {"serverId": ctx.guild.id}
    ]})
    print(user_data)
    name = member.display_name
    pfp = member.display_avatar
    likes = likes_count(user_data["twitterId"])
    followers, err = get_followers_count(user_data["twitterId"])
    following, err = get_following_count(user_data["twitterId"])

    embed = discord.Embed(title="Twitter Username", description=user_data["username"], colour=discord.Colour.random())
    embed.set_author(name=f"{name}")
    embed.set_thumbnail(url=f"{pfp}")
    embed.add_field(name="Likes", value = likes)
    embed.add_field(name="Followers", value = followers, inline=True)
    embed.add_field(name="Following", value = following, inline=False)
    embed.add_field(name="Coins", value = user_data["coins"], inline = True)

    await ctx.send(embed=embed)

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
