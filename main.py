import discord
import random
from discord.ext import commands
from tweepy_setup import *
import pymongo
from datetime import datetime
import certifi
import random

client = pymongo.MongoClient(
    "mongodb+srv://Abhay:Abhay123@cluster0.bba05gv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.users

db.register_instances.create_index("inserted", expireAfterSeconds=120)
db.follow_instances.create_index("inserted", expireAfterSeconds=120)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)


@bot.event
async def on_ready():
    print("Bot Is Online")

@bot.command()
async def help(ctx):
    em = discord.Embed(title=f"Help Commands 🤖",
                       description="List of all commands 🛠️", color=discord.Color(0xfa43ee))
    em.add_field(name="!help", value = "🧰 Shows list of all commands ", inline=False)
    em.add_field(name="!profile", value = "⚙️ Shows profile of a registered user ", inline=False)
    em.add_field(name="!profile 'mention discord handle", value = "⚙️ Shows profile of a the user mentioned", inline=False)
    em.add_field(name="!register 'twitter username'", value = "🔧 Request for registeration of your twitter handle ", inline=False)
    em.add_field(name="!verify 'last tweet content'", value="🗜️ Verify twitter account for successful registration ", inline=False)
    em.add_field(name="!leaderboard ", value="💻 Displays the top user", inline=False)
    em.add_field(name="!leaderboard 'number'", value="💻 Displays Top 'number' users", inline=False)
    em.add_field(name="!follow 'mention discord handle'", value="💰 Request mentioned user to follow you", inline=False)
    em.add_field(name="!followed 'mention discord handle'", value="💰 Verify that you have followed the mentioned user", inline=False)
    em.add_field(name="!8ball 'question'", value="🙋 Asking Yes/No Questions to the bot", inline=False)
    await ctx.send(embed=em)

@bot.command()
async def register(ctx, arg1):
    res, err = get_user_id(arg1)
    discordId=ctx.message.author.id
    if err != "":
        await ctx.reply(f"Given username is invalid! 😕")
    else:
        try:
            register_instance = db.users.find_one({"discordId" : discordId})
            lastTweetContent = last_tweet(res)
            if register_instance==None:
                db.register_instances.insert_one({
                    "username": arg1,
                    "discordId": discordId,
                    "twitterId": res,
                    "serverId": ctx.guild.id,
                    "lastTweet": lastTweetContent,
                    "inserted": datetime.utcnow()})
                await ctx.reply(f"Tweet Something in 120 seconds! Then use !verify with the content of tweet for verification of your twitter handle.")
            else:
                await ctx.reply(f"You have already registered! 🙂")
        except Exception as e:
            print("Exception ",e)


@bot.command()
async def verify(ctx, arg1):
    discordId=ctx.message.author.id
    try:
        register_instance = db.register_instances.find_one({"discordId": discordId})
        print("register ", register_instance)
        print("register_instance['twitterId'] ", register_instance['twitterId'])
        lastTweetContent = last_tweet(register_instance["twitterId"])
        print(lastTweetContent)
        if register_instance["lastTweet"] == lastTweetContent:
            await ctx.reply("Tweet something new 🤨")
            return
        if lastTweetContent != arg1:
            await ctx.reply(f"Your input didn't match with your last tweet! 🤨")
        else:
            try:
                db.users.insert_one({
                    "username": register_instance["username"],
                    "discordId": discordId,
                    "twitterId": register_instance["twitterId"],
                    "serverId": ctx.guild.id,
                    "coins": 5000,
                    "inserted": datetime.utcnow()
                })
                await ctx.reply(f"User registered!")
                return
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        await ctx.reply(f"User instance not found in database!")


@bot.command()
async def leaderboard(ctx, arg1=1):
    def cmp(ele):
        return ele['likes']
    users = db.users.find()
    scores = []
    for user in users:
        scores.append(
            {"username": user["username"], "likes": likes_count(user["twitterId"])})
    scores.sort(key=cmp, reverse=True)
    if len(scores) < int(arg1):
        await ctx.reply("Entered number is more than the users present in database. 😳")
        arg1 = len(scores)

    em = discord.Embed(title=f"Top {arg1} Most Liked People 📈",
                       description="This is based on the number of likes on twitter", color=discord.Color(0xfa43ee))
    index = 1
    for score in scores:
        em.add_field(name=f"{score['username']}",
                     value=f"Likes 👍 : {score['likes']}", inline=False)
        if index == int(arg1):
            break
        else:
            index += 1
    await ctx.send(embed=em)


@bot.command()
async def follow(ctx, member: discord.Member):
    requestedDiscordId=member.id
    requestingDiscordId=ctx.message.author.id
    try:
        userRequesting = db.users.find_one({"discordId": requestingDiscordId})
        if userRequesting==None:
            raise Exception("user not found")
        try:
            userRequested = db.users.find_one({"discordId": requestedDiscordId})
            followers, err = get_followers(userRequesting["twitterId"])
            check = any(follower for follower in followers if follower["username"] == userRequested["username"])
            if check:
                await ctx.reply("User is already following you")
                return
            else:
                channel = ctx.guild.system_channel
                db.follow_instances.insert_one({
                    "requestingUserDiscordId": requestingDiscordId,
                    "requestedUserDiscordId": requestedDiscordId,
                    "requestingUserTwitterId": userRequesting["twitterId"],
                    "requestedUserTwitterId": userRequested["twitterId"],
                })
            await channel.send(f"{member.mention} Follow {userRequesting['username']} to earn 50 coins in 2 minutes.")
            return
        except Exception as e:
            print(e)
            await ctx.reply("User you are requesting is not registered")
    except:
        await ctx.reply("You are not registered!")

@bot.command()
async def followed(ctx, member: discord.Member):
    requestingDiscordId=member.id
    requestedDiscordId=ctx.message.author.id
    try:
        request_instance = db.follow_instances.find_one({"$and":[
            {"requestingUserDiscordId": requestingDiscordId},
            {"requestedUserDiscordId": requestedDiscordId}
        ]})
        if request_instance==None:
            raise Exception("Request instance not found")
        try:
            followers, err = get_followers(request_instance["requestingUserTwitterId"])
            check = any(follower for follower in followers if follower["id"] == request_instance["requestedUserTwitterId"])
            if check:
                data = db.users.update_one({"discordId": requestedDiscordId}, {"$inc" : {
                    "coins": 50
                }})
                data = db.users.update_one({"discordId": requestingDiscordId}, {"$inc" : {
                    "coins": -50
                }})
                await ctx.reply("Successfully verified! You have gained 50 coins.")
                return
            else:
                await ctx.reply("You have not followed the user!")
                return
        except Exception as e:
            print(e)
            await ctx.reply("User you are following is not registered")
    except Exception as e:
        print("e ", e)
        await ctx.reply(f"No request was made by {member.mention}")

@bot.command()
async def profile(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    user_data = db.users.find_one({"$and":[
        {"discordId": member.id},
        {"serverId": ctx.guild.id}
    ]})
    if user_data == None:
        await ctx.reply("User not registered!")
        return
    name = member.display_name
    pfp = member.display_avatar
    likes = likes_count(user_data["twitterId"])
    followers, err = get_followers(user_data["twitterId"])
    following, err = get_following_count(user_data["twitterId"])
    embed = discord.Embed(title="Username", description=user_data["username"], colour=discord.Colour.random())
    embed.set_author(name=f"{name}")
    embed.set_thumbnail(url=f"{pfp}")
    embed.add_field(name="Likes 👍 ", value = likes)
    embed.add_field(name="Followers 👥 ", value = len(followers), inline=True)
    embed.add_field(name="Following ", value = following, inline=False)
    embed.add_field(name="Coins 🪙 ", value = user_data["coins"], inline = True)
    await ctx.send(embed=embed)

@bot.command(aliases=['8ball','test'])
async def eightball(ctx, *, question):
    responses = ["As I see it, yes.", "Ask again later","Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "Is is certain", "It is decidedly no.","Most likely","My reply is NO.","My sources say NO.","Outlook not so good","Outlook good!","Signs point to yes!","Without a doubt!!"]
    await ctx.send(f"**Question:** {question}\n**Answers:** {random.choice(responses)}")

bot.run("MTA0MjUyOTM5MTMyODEwNDQ4OA.GLtS6q.DWTFb_GoezczLuERxTgxRs5E62SnJX7EJeyKAs")
