import discord
import time
import configparser
import random
client = discord.Client()
avgtimelst = []

#loading config files
botconf = configparser.ConfigParser()
botconf.read("bot.conf")
triggerbotconf = configparser.ConfigParser()
triggerbotconf.read("triggerbot.conf")
quotebotconf = configparser.ConfigParser()
quotebotconf.read("quotebot.config")



#bot info
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))   


#main event
@client.event
async def on_message(message):
    #defining variables
    msg = str(message.content)
    channel = str(message.channel.id)
    author = str(message.author)

    #reply to bots
    if message.author.bot and botconf["config"]["replytobot"] == "false": 
        return

    #start event timer
    print("\n start client.event")
    start = time.time()

    #triggerbot
    b = 0
    found = "false"
    triggersstr = (triggerbotconf["config"]["triggers"])
    triggers = triggersstr.split(",")
    print(triggers)
    print(type(triggers))
    while b < len(triggers) and found == "false": 
        if triggers[b] not in msg:
            b = b+1
        elif triggers[b] in msg:
            print("balls")
            found = "true"
            await message.channel.send("hello")
        else:
            print("something happened")
        
    #daily quote
    if channel == "1010042640508669982":
        print("weeee")

    #end function timer
    end = time.time()
    eventime = (end - start)
    reventime = str(round(eventime,3))
    avgtimelst.append(float(reventime))
    avgtime = str(sum(avgtimelst) / len(avgtimelst))
    print("\n end client.event \n time: " + str(reventime) + "\n average time: " + avgtime)



client.run('OTg2NDA4MjM3Njg5NjMwNzYx.GZZchW.Aymv6QYXFPcvrT6YqBmJIhB_HKWZK1UOEKeIVo')
