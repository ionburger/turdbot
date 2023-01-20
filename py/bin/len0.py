# length func which works better for indexing lists
def len0(args):
    a = len(args)
    if a > 0:
        return a-1
    else:
        return False

