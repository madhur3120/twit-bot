import discord
import random
from discord.ext import commands
from tweepy_setup import *
import pymongo
import asyncio
from datetime import datetime
import certifi
import random
import asyncio

client = pymongo.MongoClient(
    "mongodb+srv://Abhay:Abhay123@cluster0.bba05gv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.users

db.register_instances.create_index("inserted", expireAfterSeconds=120)
db.follow_instances.create_index("inserted", expireAfterSeconds=120)

bot = commands.Bot(command_prefix="!",
                   intents=discord.Intents.all(), help_command=None)


@bot.event
async def on_ready():
    print("Bot Is Online")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("No such command")
    else:
        await ctx.send(error)

page1 = discord.Embed(title=f"Help Commands 🤖",
                      description="List of all commands 🛠️", color=discord.Color(0xfa43ee))
page1.add_field(
    name="!help", value="🧰 Shows list of all commands ", inline=False)
page1.add_field(name="!profile",
                value="⚙️ Shows profile of a registered user ", inline=False)
page1.add_field(name="!profile 'mention discord handle",
                value="⚙️ Shows profile of a the user mentioned", inline=False)
page1.add_field(name="!register 'twitter username'",
                value="🔧 Request for registeration of your twitter handle ", inline=False)
page1.add_field(name="!verify 'last tweet content'",
                value="🗜️ Verify twitter account for successful registration ", inline=False)
page1.add_field(name="!leaderboard ",
                value="💻 Displays the top user", inline=False)
page2.add_field(name="!slots 'amount'",
                value="🔧 Play a Slot game for double money. If all the emojis are same, you win else you lose ", inline=False)
page2 = discord.Embed(title=f"Help Commands 🤖",
                      description="List of all commands 🛠️", color=discord.Color(0xfa43ee))
page2.add_field(name="!leaderboard 'number'",
                value="💻 Displays Top 'number' users", inline=False)
page2.add_field(name="!follow 'mention discord handle'",
                value="💰 Request mentioned user to follow you", inline=False)
page2.add_field(name="!rob 'mention discord handle'",
                value="💸  Steal some money from mentioned user's wallet", inline=False)
page2.add_field(name="!followed 'mention discord handle'",
                value="🤑 Verify that you have followed the mentioned user", inline=False)
page2.add_field(name="!8ball 'question'",
                value="🙋 Asking Yes/No Questions to the bot", inline=False)
page3 = discord.Embed(title="!beg",
                      description="👛 Beg some coins from the bot", colour=discord.Colour.orange())
page3 = discord.Embed(title="!balance",
                      description="💸 Check Your Wallet and Bank Balance", colour=discord.Colour.orange())
page3 = discord.Embed(title="!deposit 'amount'",
                      description="🤑 Deposit money from the wallet to the bank", colour=discord.Colour.orange())
page3 = discord.Embed(title="!withdraw 'amount'",
                      description="💰 Withdraw money from the bank to wallet", colour=discord.Colour.orange())
page3 = discord.Embed(title="!send 'mention discord handle' 'amount'",
                      description="💸 Send money from your wallet to the mentioned user's wallet", colour=discord.Colour.orange())
page3.add_field(name="!shop",
                value="💻 Displays the list of items present in store", inline=False)
page3.add_field(name="!buy 'item's name' 'quantitiy'",
                value="💰 Buy an item from the shop and add it your collection.", inline=False)
bot.help_pages = [page1, page2, page3]


@bot.command()
async def help(ctx):
    # skip to start, left, right, skip to end
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
    current = 0
    msg = await ctx.send(embed=bot.help_pages[current])

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return print("test")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0

            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(bot.help_pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(bot.help_pages)-1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(embed=bot.help_pages[current])


@bot.command()
async def register(ctx, arg1):
    res, err = get_user_id(arg1)
    discordId = ctx.message.author.id
    if err != "":
        await ctx.reply(f"Given username is invalid! 😕")
    else:
        try:
            register_instance = db.users.find_one({"discordId": discordId})
            lastTweetContent = last_tweet(res)
            if register_instance == None:
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
            print("Exception ", e)


@bot.command()
async def verify(ctx, arg1):
    discordId = ctx.message.author.id
    try:
        register_instance = db.register_instances.find_one(
            {"discordId": discordId})
        print("register ", register_instance)
        print("register_instance['twitterId'] ",
              register_instance['twitterId'])
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
                    "bank": 5000,
                    "wallet": 0,
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
    if arg1 == 1:
        em = discord.Embed(title=f"Top Liked User 📈",
                           description="This is based on the number of likes on twitter", color=discord.Color(0xfa43ee))
    else:
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
    requestedDiscordId = member.id
    requestingDiscordId = ctx.message.author.id
    try:
        userRequesting = db.users.find_one({"discordId": requestingDiscordId})
        if userRequesting == None:
            raise Exception("user not found")
        try:
            userRequested = db.users.find_one(
                {"discordId": requestedDiscordId})
            followers, err = get_followers(userRequesting["twitterId"])
            check = any(
                follower for follower in followers if follower["username"] == userRequested["username"])
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
    requestingDiscordId = member.id
    requestedDiscordId = ctx.message.author.id
    try:
        request_instance = db.follow_instances.find_one({"$and": [
            {"requestingUserDiscordId": requestingDiscordId},
            {"requestedUserDiscordId": requestedDiscordId}
        ]})
        if request_instance == None:
            raise Exception("Request instance not found")
        try:
            followers, err = get_followers(
                request_instance["requestingUserTwitterId"])
            check = any(
                follower for follower in followers if follower["id"] == request_instance["requestedUserTwitterId"])
            if check:
                data = db.users.update_one({"discordId": requestedDiscordId}, {"$inc": {
                    "coins": 50
                }})
                data = db.users.update_one({"discordId": requestingDiscordId}, {"$inc": {
                    "coins": -50
                }})
                data = db.users.update_one({"discordId": requestingDiscordId}, {"$push": {
                    "followers": request_instance["requestedUserTwitterId"]
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
async def report(ctx, member: discord.Member = None):
    if member == None:
        await ctx.reply(f"Mention the user whom you want to report.")
    userId = ctx.message.author.id
    reportUserId = member.id
    try:
        user_instance = db.users.find_one({"discordId": userId})
        if user_instance == None:
            await ctx.reply(f"You are not registered.")
        report_user_instance = db.users.find_one({"discordId": reportUserId})
        if report_user_instance == None:
            await ctx.reply(f"User you are reporting is not registered.")
        followers, err = get_followers(user_instance["twitterId"])
        print(followers)
        check = any(
            follower for follower in followers if follower["id"] == report_user_instance["twitterId"])
        print(check)
        if check:
            await ctx.reply("False report. The user is still following you.")
        else:
            db.users.update_one({"discordId": userId}, {"$inc": {
                "coins": 100
            }})
            db.users.update_one({"discordId": reportUserId}, {"$inc": {
                "coins": -100
            }})
            print("update")
            db.users.update_one({"discordId": userId}, {"$pull": {
                "followers": report_user_instance["twitterId"]
            }})
            print("update2")
            await ctx.reply("Report found true. 100 coins deducted from {member.mention} and added to your account.")
    except Exception as e:
        print(e)
        await ctx.reply("Some error occured")


@bot.command()
async def profile(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    user_data = db.users.find_one({"$and": [
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
    embed = discord.Embed(
        title="Username", description=user_data["username"], colour=discord.Colour.random())
    embed.set_author(name=f"{name}")
    embed.set_thumbnail(url=f"{pfp}")
    embed.add_field(name="Likes 👍 ", value=likes)
    embed.add_field(name="Followers 👥 ", value=len(followers), inline=True)
    embed.add_field(name="Following ", value=following, inline=False)
    embed.add_field(name="Wallet 🪙 ", value=user_data["wallet"], inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def beg(ctx):
    discordId = ctx.message.author.id
    earnings = random.randrange(101)
    try:
        db.users.update_one({"discordId": discordId}, {"$inc": {
            "wallet": earnings
        }})
        await ctx.send(f"Someone gave you {earnings} coins.")
    except Exception as e:
        await ctx.send(f"Some error occured!")


@bot.command()
async def balance(ctx):
    discordId = ctx.message.author.id
    try:
        user_data = db.users.find_one({"discordId": discordId})
        wallet_amount = user_data["wallet"]
        bank_amount = user_data["bank"]
        embed = discord.Embed(
            title=f"{ctx.author.name}'s balance 🪙", color=discord.Colour.green())

        embed.add_field(name="Wallet balance", value=wallet_amount)
        embed.add_field(name="Bank balance", value=bank_amount)
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"Some error occured!")


async def update_bank_withdraw(user_discordId, change=0):
    err = None
    try:
        user_data = db.users.find_one({"discordId": user_discordId})
        if user_data["bank"] < change:
            err = "You don't have that much money in bank!"
            return err
        if change < 0:
            err = "Amount should be positive!"
            return err
        data = db.users.update_one({"discordId": user_discordId}, {"$inc": {
            "bank": -1*change,
            "wallet": change
        }})

    except Exception as e:
        err = "Some error occured!"
    return err


async def update_bank_deposit(user_discordId, change=0):
    err = None
    try:
        user_data = db.users.find_one({"discordId": user_discordId})
        if user_data["wallet"] < change:
            err = "You don't have enough money in your wallet!"
            return err
        if change < 0:
            err = "Amount should be positive!"
            return err
        data = db.users.update_one({"discordId": user_discordId}, {"$inc": {
            "bank": change,
            "wallet": -1*change
        }})

    except Exception as e:
        err = "Some error occured!"
    return err


@bot.command()
async def withdraw(ctx, amount=None):
    if amount == None:
        await ctx.send("Please enter the amount!")
        return
    if amount.isnumeric():
        err = await update_bank_withdraw(ctx.author.id, int(amount))
        if err == None:
            await ctx.send(f"You withdrew {amount} coins")
        else:
            await ctx.send(err)
    else:
        await ctx.send("Enter a Numeric Value")


@bot.command()
async def deposit(ctx, amount=None):
    if amount == None:
        await ctx.send("Please enter the amount!")
        return
    if amount.isnumeric():
        amount1 = int(amount)
        err = await update_bank_deposit(ctx.author.id, amount1)
        if err == None:
            await ctx.send(f"You deposited {amount1} coins")
        else:
            await ctx.send(err)
    else:
        await ctx.send("Enter a Numeric Value")


@bot.command()
async def send(ctx, member: discord.Member, amount=None):
    if amount == None:
        await ctx.send("Please enter the amount!")
        return
    if amount.isnumeric():
        amount1 = int(amount)
    if amount1 < 0:
        await ctx.send("Amount should be positive!")
        return

    user_data = db.users.find_one({"discordId": ctx.author.id})
    if user_data["wallet"] < amount1:
        await ctx.send("Insufficient balance!")
        return

    db.users.update_one({"discordId": ctx.author.id}, {"$inc": {
        "wallet": -1*amount1,
    }})
    db.users.update_one({"discordId": member.id}, {"$inc": {
        "wallet": amount1,
    }})

    await ctx.send(f"You sent {amount1} coins to {member.mention}")


@bot.command()
async def slots(ctx, amount=None):
    if amount == None:
        await ctx.send("Please enter the amount!")
        return
    if amount.isnumeric():
        amount1 = int(amount)
    if amount1 < 0:
        await ctx.send("Amount should be positive!")
        return

    user_data = db.users.find_one({"discordId": ctx.author.id})
    if user_data["wallet"] < amount1:
        await ctx.send("Insufficient balance!")
        return

    final = []
    for i in range(3):
        a = random.choice(["🙂", "😁", "😉"])
        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[2] == final[2] or final[1] == final[2]:
        await ctx.send("You Won Double the Money!!!")
        db.users.update_one({"discordId": ctx.author.id}, {"$inc": {
            "wallet": 2*amount1,
        }})
    else:
        await ctx.send("Alas! You Lost Your Money")
        db.users.update_one({"discordId": ctx.author.id}, {"$inc": {
            "wallet": -1*amount1,
        }})


@bot.command()
async def rob(ctx, member: discord.Member):
    user_data = db.users.find_one({"discordId": member.id})
    if user_data["wallet"] < 50:
        await ctx.send("It's not worth it!")
        return
    earnings = random.randrange(0, user_data["wallet"])
    await db.users.update_one({"discordId": ctx.author.id}, {"$inc": {
        "wallet": earnings,
    }})
    await db.users.update_one({"discordId": member.id}, {"$inc": {
        "wallet": -1*earnings,
    }})

store = [{"name": "MacBook", "price": 9400, "description": "Macbook 2022"},
         {"name": "Iphone", "price": 12000, "description": "Iphone 18"},
         {"name": "Apple Watch", "price": 4000,
          "description": "Apple Watch Series 4"},
         {"name": "Sanmsung S21", "price": 7000,
             "description": "Samsung S21 with 64 MP Camera"},
         ]


@bot.command()
async def shop(ctx):
    em = discord.Embed(title="Shop")
    for item in store:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name, value=f"${price} | {desc}", inline=False)
    await ctx.send(embed=em)


@bot.command()
async def buy(ctx, itemName, amount=1):
    item_name = itemName.lower()
    name_ = None
    for item in store:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break
    if name_ == None:
        await ctx.send("Item is not present in store.")
        return

    cost = int(amount) * price
    user_data = db.users.find_one({"discordId": ctx.message.author.id})

    if user_data["wallet"] < cost:
        await ctx.send("Insufficient balance")
        return
    db.users.update_one({"discordId": ctx.message.author.id}, {"$inc": {
        "wallet": -1*cost,
    }})
    db.users.update_one({"discordId": ctx.message.author.id}, {"$push": {
        "items": {
            "name": itemName,
            "amount": amount
        }}})

    await ctx.send(f"You just bought {amount} {itemName}")


@bot.command()
async def bag(ctx):
    user_instance = db.users.find_one({
        "discordId": ctx.message.author.id
    })
    if user_instance == None:
        ctx.reply("You are not registered.")
    items = user_instance.items
    print(items)
    total_item = []
    for item in items:
        print(items)
        total_item[item.name] += int(amount)
    print(item)


@bot.command(aliases=['8ball', 'test'])
async def eightball(ctx, *, question):
    responses = ["As I see it, yes.", "Ask again later", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "Is is certain",
                 "It is decidedly no.", "Most likely", "My reply is NO.", "My sources say NO.", "Outlook not so good", "Outlook good!", "Signs point to yes!", "Without a doubt!!"]
    await ctx.send(f"**Question:** {question}\n**Answers:** {random.choice(responses)}")


# help pages
# page1 = discord.Embed(title=f"Help Commands 🤖",
#                        description="List of all commands 🛠️", color=discord.Color(0xfa43ee))
# page2 = discord.Embed(title="Bot Help 2",
#                       description="Page 2", colour=discord.Colour.orange())
# page3 = discord.Embed(title="Bot Help 3",
#                       description="Page 3", colour=discord.Colour.orange())

# bot.help_pages = [page1, page2, page3]


# @bot.command()
# async def paginate(ctx):
#     # skip to start, left, right, skip to end
#     buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
#     current = 0
#     msg = await ctx.send(embed=bot.help_pages[current])

#     for button in buttons:
#         await msg.add_reaction(button)

#     while True:
#         try:
#             reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

#         except asyncio.TimeoutError:
#             return print("test")

#         else:
#             previous_page = current
#             if reaction.emoji == u"\u23EA":
#                 current = 0

#             elif reaction.emoji == u"\u2B05":
#                 if current > 0:
#                     current -= 1

#             elif reaction.emoji == u"\u27A1":
#                 if current < len(bot.help_pages)-1:
#                     current += 1

#             elif reaction.emoji == u"\u23E9":
#                 current = len(bot.help_pages)-1

#             for button in buttons:
#                 await msg.remove_reaction(button, ctx.author)

#             if current != previous_page:
#                 await msg.edit(embed=bot.help_pages[current])

bot.run("MTA0MjUyOTM5MTMyODEwNDQ4OA.GLtS6q.DWTFb_GoezczLuERxTgxRs5E62SnJX7EJeyKAs")
