import discord
from discord import app_commands
import utility
import bttv

util = utility.utility()
bttv = bttv.bttv

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

#LIST BTTV EMOTES
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@tree.command(name="bttv_ls", description="Lists all BTTV emotes from the specified Twitch channel")
async def emoteList(interaction: discord.Interaction, channel: str):
    await interaction.response.defer()

    id = util.twitchID(channel)
    chunks = bttv.emoteList(channel, id)
    
    for i in chunks:
        await interaction.followup.send(i, ephemeral=True)

#GET BTTV EMOTE
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@tree.command(name="bttv", description="Posts a BetterTTV emote from the specified Twitch channel")
async def emote(interaction: discord.Interaction, channel: str, emote_name: str):
    userID = util.twitchID(channel)
    found, animated, id = bttv.findEmote(userID, emote_name)
    if not found:
        await interaction.response.send_message(f'Emote "{emote_name}" not found')
    else:
        if animated:
            await interaction.response.send_message(f"https://cdn.betterttv.net/emote/{id}/3x.gif")
        else:
            await interaction.response.send_message(f"https://cdn.betterttv.net/emote/{id}/3x")

#LIST BTTV GLOBAL EMOTES
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@tree.command(name="bttv_g_ls", description="Lists all BTTV global emotes")
async def emoteListGlobal(interaction: discord.Interaction):
    await interaction.response.defer()

    chunks = bttv.globalEmoteList()
    
    for i in chunks:
        await interaction.followup.send(i, ephemeral=True)

#GET BTTV GLOBAL EMOTE
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@tree.command(name="bttv_g", description="Posts a BetterTTV global emote")
async def globalEmote(interaction: discord.Interaction, emote_name: str):
    found, animated, id = bttv.findGlobalEmote(emote_name)
    if not found:
        await interaction.response.send_message(f'Emote "{emote_name}" not found')
    else:
        if animated:
            await interaction.response.send_message(f"https://cdn.betterttv.net/emote/{id}/3x.gif")
        else:
            await interaction.response.send_message(f"https://cdn.betterttv.net/emote/{id}/3x")



token = input("Enter token: ")
client.run(token)