 # triggerbot
        if config("triggerbotenabled") == "true":
            x = 0
            found = "false"
            triggers = config("triggerbottriggers", db="data")
            while x < len(triggers) and found == "false":
                if triggers[x] not in msg:
                    x = x+1
                elif triggers[x] in msg:
                    found = "true"
                    replys = config("triggerbotreplys", db="data")
                    rand = random.randint(0, len(replys))-1
                    await message.channel.send(replys[rand])
                else:
                    print("something happened")
