import discord
import openai
import time
from tokens import TOKEN, OPENAI_API_KEY

bot = discord.Bot(intents=discord.Intents.all())
client = openai.OpenAI(api_key = OPENAI_API_KEY)


def ask_question(message):
    completion = client.chat.completions.create(
    model="gpt-4",
    messages= message
    )

    return completion.choices[0].message.content


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="prompt", description="ask gpt-4 for a response (future)")
async def response(ctx, prompt: str):
    user = await bot.fetch_user(ctx.author.id)
    await ctx.respond(f"Creating thread for {user.mention}!")
    thread = await ctx.send(f"{prompt}")
    new_thread = await thread.create_thread(name=user.global_name, auto_archive_duration=60)    
    initial_response = ask_question([{"role": "user", "content": prompt}])
    await new_thread.send(initial_response)

    @bot.event
    async def on_message(message):
        if isinstance(message.channel, discord.Thread) and message.channel.id == new_thread.id:
            if message.author != bot.user:
                messages = await message.channel.history(limit=200).flatten()
                messages.reverse()
                gpt_message = list()
                
                OG_promp = await ctx.fetch_message(message.channel.id)
                gpt_message.append({"role": "user", "content": OG_promp.content})
                
                for channel_message in messages[1:]:
                    if channel_message.author == bot.user:
                        gpt_message.append({"role": "assistant", "content": channel_message.content})
                    else:
                        gpt_message.append({"role": "user", "content": channel_message.content})
                response = ask_question(gpt_message)
                await new_thread.send(response)



bot.run(TOKEN)
