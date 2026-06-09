#import scripts.utility as utility\
from scripts import utility

util = utility.utility()


class bttv:

    def emoteList(name, id):
        chunks = []
        data = util.callAPI(f"https://api.betterttv.net/3/cached/users/twitch/{id}")
        set_id = data["id"]
        list = f"**{name}'s BTTV Emotes (Visual List: https://betterttv.com/users/{set_id}):** "

        for i in data["channelEmotes"]:
            if len(list) + len(i["code"]) > 1900:
                chunks.append(list)
                list = f"**{name}'s BTTV Emotes (Visual List: https://betterttv.com/users/{set_id}):** "
            list += "\n-" + i["code"]
        if list:
            chunks.append(list)

        for i in data["sharedEmotes"]:
            if len(list) + len(i["code"]) > 1900:
                chunks.append(list)
                list = f"**{name}'s BTTV Emotes (Visual List: https://betterttv.com/users/{set_id}):** "
            list += "\n-" + i["code"]
        if list:
            chunks.append(list)

        return chunks
    
    def globalEmoteList():
        chunks = []
        list = "**Global Emotes:**"
        count = 0
        data = util.callAPI("https://api.betterttv.net/3/cached/emotes/global")
        for i in data:
            count += 1
            list += "\n-" + i["code"]
            if count == 60:
                count = 0
                chunks.append(list)
                list = f"**Global Emotes:** "
        if list:
            chunks.append(list)
        return chunks
            

    def findEmote(userID, name):
        data = util.callAPI(f"https://api.betterttv.net/3/cached/users/twitch/{userID}")
        found = False
        animated = False
        index = 0
        id = ""
        for i in range(len(data["channelEmotes"])):
            if data["channelEmotes"][i]["code"] == name:
                found = True
                animated = data["channelEmotes"][i]["animated"]
                index = i
                id = data["channelEmotes"][i]["id"]
                #return f"https://cdn.betterttv.net/emote/{}/3x"
        for i in range(len(data["sharedEmotes"])):
            if data["sharedEmotes"][i]["code"] == name:
                found = True
                index = i
                animated = data["sharedEmotes"][i]["animated"]
                id = data["sharedEmotes"][i]["id"]
                #return f"https://cdn.betterttv.net/emote/{data[i]["id"]}/3x"
        return found, animated, id
    
    def findGlobalEmote(name):
        data = util.callAPI("https://api.betterttv.net/3/cached/emotes/global")
        found = False
        animated = False
        index = 0
        id = ""
        for i in range(len(data)):
            if data[i]["code"] == name:
                found = True
                animated = data[i]["animated"]
                index = i
                id = data[i]["id"]
        return found, animated, id
    