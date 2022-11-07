# Copyright (c) 2022, Ian Burgess
# All rights reserved.
#
# This source code is licensed under the GPLv3 license. A copy of this license can be found in the LICENSE file in the root directory of this source tree.

import shelve
server = "default"
def config(value,db="config",serverid=server,mode="r"):
    default = {
        "replytobot":"false",
        "triggerbotenabled":"true",
        "quotebotenabled":"true",
        "triggerbottriggers":["hello","hi","howdy"],
        "quotequeue":"1010042640508669982",
        
        
    }
    data = shelve.open("bot.shlf",writeback=True)
    if mode == "r":
        try:
            return data[db][serverid][value]
        except:
            return default[value]
    elif mode == "w":
        data[db][serverid] = value
        return("success")
    else:
        print("error")
    data.close()

