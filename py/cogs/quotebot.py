 
        # daily quote
        if channel == config("quotequeue") and config("quotebotenabled") == "true":
            file = open("data/quotes.var", "a")
            file.write(msg)
            file.write(":")
            file.close()