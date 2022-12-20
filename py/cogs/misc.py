        # bot commands
        await bot.process_commands(message)
    @tasks.loop(time=quotetime, reconnect=True)
    async def dailyquote():
        if config("quotebotenabled") == "true":
            file = open("data/quotes.var", "r+")
            list = file.read().split(":")
            rand = random.randint(0, (len(list)-1))
            print(rand)
            channel = bot.get_channel(int(quotebotconf["config"]["dailyquote"]))
            await channel.send(list.pop(rand))
            file.write(":".join(list))
            file.close()

