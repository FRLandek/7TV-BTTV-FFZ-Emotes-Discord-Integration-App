import utility

util = utility.utility()

class seventv:

    def emoteList(name, id):
        chunks = []
        data = util.callAPI(f"https://7tv.io/v3/users/twitch/{id}")
        set_id = data["emote_set_id"]
        list = f"**{name}'s 7TV Emotes (Visual List: https://7tv.app/users/{set_id}):** "
        emotes = data["emote_set"]["emotes"]


        for i in emotes:
            if len(list) + len(i["name"]) > 1900:
                chunks.append(list)
                list = f"**{name}'s 7TV Emotes (Visual List: https://7tv.app/users/{set_id}):** "
            list += "\n-" + i["name"]
        if list:
            chunks.append(list)

        return chunks


    def findEmote(userID, name, size):
        data = util.callAPI(f"https://7tv.io/v3/users/twitch/{userID}")
        emotes = data["emote_set"]["emotes"]

        for i in emotes:
            if i["name"] == name:
                return f"https://cdn.7tv.app/emote/{i["id"]}/{size}.webp"
            
        return f'Emote "{name}" not found. For help run "/emote_help" '