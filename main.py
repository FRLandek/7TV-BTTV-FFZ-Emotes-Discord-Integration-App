import discord
from discord import app_commands
import utility
import bttv, ffz, seventv
from typing import Optional

util = utility.utility()
bttv = bttv.bttv
ffz = ffz.ffz
seventv = seventv.seventv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)



@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


# HELP COMMAND ###################################################################################################
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@tree.command(name="emote_help", description="Instructions on how to use the app")
async def emoteHelp(interaction: discord.Interaction):
    await interaction.response.send_message("""                                            
On Twitch, there are 3 third party chat emote services that people use:
-7TV - Most popular today - https://7tv.app/
-BetterTTV - Used to be popular, still has many users - https://betterttv.com/
-FrankerFaceZ - Still has some old emotes but not many people use it - https://www.frankerfacez.com/
                                            
Popular Twitch channels usually have their own emote set under one of these services
                                            
**To see a list of a channel's emotes**:                                    
/emote_list {channel} {source} - Lists all the emotes in a channel's emote set under the specified emote service

**Channels with good emote sets for each service**:
-7TV - xqc
-BetterTTV - forsen
-FrankerFaceZ - nickmercs, imaqtpie, trick2g                                                                                 
""", ephemeral=True)
#---------------------------------------------------------------------------------------------------------------#


# LIST EMOTES ###################################################################################################
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.choices(emote_source=[
    app_commands.Choice(name="7TV", value="7tv"),
    app_commands.Choice(name="BTTV", value="bttv"),
    app_commands.Choice(name="FFZ", value="ffz"),
])
@tree.command(name="emote_list", description="Lists all BTTV emotes from the specified Twitch channel")
async def emoteList(
    interaction: discord.Interaction, 
    channel: str,
    emote_source: app_commands.Choice[str]
    ):

    await interaction.response.defer()
    id = util.twitchID(channel)

    if emote_source is None:  source = "7tv"
    else:                     source = emote_source.value

    if source == "7tv":
        chunks = seventv.emoteList(channel, id)
        for i in chunks[:5]:
            await interaction.followup.send(i, ephemeral=True)
        if len(chunks) > 5:
            await interaction.followup.send("Unfortunately, this list exceeds the max amount of Discord followup messages.", ephemeral=True)
    elif source == "bttv":
        chunks = bttv.emoteList(channel, id)
        for i in chunks[:5]:
            await interaction.followup.send(i, ephemeral=True)
        if len(chunks) > 5:
            await interaction.followup.send("Unfortunately, this list exceeds the max amount of Discord followup messages.", ephemeral=True)
    elif source == "ffz":
        chunks = ffz.emoteList(channel, id)
        for i in chunks[:5]:
            await interaction.followup.send(i, ephemeral=True)
        if len(chunks) > 5:
            await interaction.followup.send("Unfortunately, this list exceeds the max amount of Discord followup messages.", ephemeral=True)
#---------------------------------------------------------------------------------------------------------------#

# GET EMOTE ###################################################################################################
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.choices(emote_source=[
    app_commands.Choice(name="7TV", value="7tv"),
    app_commands.Choice(name="BTTV", value="bttv"),
    app_commands.Choice(name="FFZ", value="ffz"),
])
@app_commands.choices(size=[
    app_commands.Choice(name="Large", value="large"),
    app_commands.Choice(name="Medium", value="medium"),
    app_commands.Choice(name="Small", value="small"),
    app_commands.Choice(name="Tiny", value="tiny"),
])
@tree.command(name="emote", description="Posts an emote from the specified Twitch channel and source (Default: 7tv, size large, no effects)")
async def emote(
    interaction: discord.Interaction, 
    channel: str, 
    emote_name: str, 
    emote_source: Optional[app_commands.Choice[str]], 
    size: Optional[app_commands.Choice[str]]
    ):
    await interaction.response.defer()

    userID = util.twitchID(channel)

    if emote_source is None:  source = "7tv"
    else:                     source = emote_source.value

    if source == "7tv":
        if size is None or size.value == "large":               s = "4x"
        elif size.value == "medium":                            s = "3x"
        elif size.value == "small":                             s = "2x"
        elif size.value == "tiny":                              s = "1x"

        await interaction.followup.send(seventv.findEmote(userID, emote_name, s), ephemeral=True)
    elif source == "bttv":
        if size is None or size.value == "large":               s = 3
        elif size.value == "medium":                            s = 2
        elif size.value == "small" or size.value == "tiny":     s = 1

        found, animated, id = bttv.findEmote(userID, emote_name)
        if not found:
            await interaction.followup.send(f'Emote "{emote_name}" not found. For help run "/emote_help" ', ephemeral=True)
        else:
            if animated:
                url = f"https://cdn.betterttv.net/emote/{id}/{s}x.gif"
                await interaction.followup.send(url)
            else:
                url = f"https://cdn.betterttv.net/emote/{id}/{s}x"
                await interaction.followup.send(url)
    elif source == "ffz":
        if size is None or size.value == "large":               s = "4x"
        elif size.value == "medium":                            s = "2x"
        elif size.value == "small" or size.value == "tiny":     s = "1x"

        await interaction.followup.send(ffz.findEmote(userID, emote_name, s), ephemeral=True)
#---------------------------------------------------------------------------------------------------------------#

# #LIST BTTV GLOBAL EMOTES
# @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
# @app_commands.allowed_installs(guilds=True, users=True)
# @tree.command(name="bttv_g_ls", description="Lists all BTTV global emotes")
# async def emoteListGlobal(interaction: discord.Interaction):
#     await interaction.response.defer()

#     chunks = bttv.globalEmoteList()
    
#     for i in chunks:
#         await interaction.followup.send(i, ephemeral=True)

# #GET BTTV GLOBAL EMOTE
# @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
# @app_commands.allowed_installs(guilds=True, users=True)
# @tree.command(name="bttv_g", description="Posts a BetterTTV global emote")
# async def globalEmote(interaction: discord.Interaction, emote_name: str):
#     found, animated, id = bttv.findGlobalEmote(emote_name)
#     if not found:
#         await interaction.response.send_message(f'Emote "{emote_name}" not found. For help run "/emote_help" ')
#     else:
#         if animated:
#             await interaction.response.send_message(f"https://cdn.betterttv.net/emote/{id}/3x.gif")
#         else:
#             await interaction.response.send_message(f"https://cdn.betterttv.net/emote/{id}/3x")



token = input("Enter token: ")
client.run(token)