import discord
from discord import app_commands
from tokens import TOKEN, GUILD

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
@tree.command(
    name="commandname",
    description="My first application Command",
    guild=discord.Object(id=GUILD)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")
    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD))
    print("Ready!")
    
    
client.run(TOKEN)