import utility

util = utility.utility()


class ffz:

    def emoteList(name, id):
        chunks = []
        list = f"**{name}'s FFZ Emotes (Visual List: https://www.frankerfacez.com/channel/{name}):** "
        data = util.callAPI(f"https://api.betterttv.net/3/cached/frankerfacez/users/twitch/{id}")

        for i in data:
            if len(list) + len(i["code"]) > 1900:
                chunks.append(list)
                list = f"**{name}'s FFZ Emotes (Visual List: https://www.frankerfacez.com/channel/{name}):** "
            list += "\n-" + i["code"]
        if list:
            chunks.append(list)

        return chunks


    def findEmote(userID, name, size):
        data = util.callAPI(f"https://api.betterttv.net/3/cached/frankerfacez/users/twitch/{userID}")

        for i in data:
            if i["code"] == name:
                return i["images"][size]
            
        return f'Emote "{name}" not found. For help run "/emote_help" '