# twit-bot


To Invite TwitBot - Copy this URL and paste it in browser tab
https://discord.com/api/oauth2/authorize?client_id=1042529391328104488&permissions=8&scope=bot%20applications.commands

Supported Commands-

1. Help
   !help -> Shows the list of help commands
2. Profile
   !profile -> Shows profile of user who typed this command
   !profile @xyz -> Shows profile of xyz user
3. Register
   !register xyz_twitter_username -> Request for verification of xyz_twitter_username
4. Verify
   !verify content_of_last_tweet -> Verify the twitter handle requested for verification
5. Leaderboard (Leaderboard is generated on the basis of likes on last 10 tweets, retweets and replies)
   !leaderboard -> Shows the user with most likes.
   !leaderboard x -> Shows the top x users with most likes.
6. Follow
   !follow @xyz -> Request user x to follow your twitter handle.
7. Followed
   !followed @xyz -> Request for verification that you have followed the user requested you to follow him
8. 8ball
   !8ball "question" -> Ask randow question to get Yes/No answer.
9. Like
   !like 'mention discord handle' 'tweet content' -> Request mentioned user to like your tweet which matches the content mentioned
10. Liked
    !liked 'mention discord handle' 'tweet content' -> Verify that you have liked the tweet which matches the content of the mentioned user

How To Run The Bot

Way 1 -
Run the following commands in the terminal
pip install discord.py==2.1.0
pip install tweepy==4.9.0
pip install pymongo==4.3.3
pip install dnspython==2.2.1
pip install certifi==2021.5.30

-------------------OR--------------------------

Way 2 -
pip install -r requirements.txt
(This command will read the dependencies from the requirement.txt file)

---

Run the "main.py" file and the bot will be online.

Run the help command "!help" to check the bot commands
