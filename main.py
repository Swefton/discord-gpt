import discord
from discord import app_commands
from openai import OpenAI
from tokens import TOKEN, GUILD, OPENAI_API_KEY

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content) 

@tree.command(
    name="commandname",
    description="My first application Command",
    guild=discord.Object(id=GUILD)
)
async def first_command(interaction, optional_param1 : str = "test", optional_param2 : str = ""):
    await interaction.response.send_message(f"Hello! {optional_param1} {optional_param2}")
    print(interaction.data)
    print(type(interaction.channel), interaction.channel)
    for i in interaction.channel.members:
        print(i)
    await interaction.channel.create_thread(name="test", message=interaction.message, reason="gpt", )   
 
     
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD))
    print("Ready!")
    

    
    
client.run(TOKEN)
   
   
    
'''
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)
'''