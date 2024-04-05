import discord
import openai
from tokens import TOKEN, OPENAI_API_KEY

bot = discord.Bot(intents=discord.Intents.all())
openai.api_key = OPENAI_API_KEY

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="prompt", description="ask gpt-4 for a response (future)")
async def response(ctx, prompt: str):
    user = await bot.fetch_user(ctx.author.id)
    thread = await ctx.send(f"{prompt}")
    new_thread = await thread.create_thread(name="Echo Thread", auto_archive_duration=60)
    
    
    
    await new_thread.send("RESPONSE")
    await ctx.respond(f"Thread created for {user.mention}!")

    @bot.event
    async def on_message(message):
        if isinstance(message.channel, discord.Thread) and message.channel.id == new_thread.id:
            if message.author != bot.user:
                messages = await message.channel.history(limit=200).flatten()
                messages.reverse()
                gpt_message = list()
                
                OG_promp = await ctx.fetch_message(message.channel.id)
                print(OG_promp.content)
                gpt_message.append({"role": "user", "content": OG_promp.content})
                
                for channel_message in messages[1:]:
                    if channel_message.author == bot.user:
                        gpt_message.append({"role": "bot", "content": channel_message.content})
                    else:
                        gpt_message.append({"role": "user", "content": channel_message.content})

                await new_thread.send("RESPONSE")



bot.run(TOKEN)
