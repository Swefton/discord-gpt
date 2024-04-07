import discord
import openai
from tokens import TOKEN, OPENAI_API_KEY

bot = discord.Bot(intents=discord.Intents.all())
client = openai.OpenAI(api_key=OPENAI_API_KEY)

processing_emoji = '⌛'
prompt_map = {}


def ask_question(message):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=message
    )
    return completion.choices[0].message.content


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="prompt", description="Ask GPT-4 for a response (future)")
async def response(ctx, prompt: str):
    user = await bot.fetch_user(ctx.author.id)
    await ctx.respond(f"Creating thread for {user.mention}!")
    thread = await ctx.send(f"{prompt}")
    new_thread = await thread.create_thread(name=user.global_name, auto_archive_duration=60)

    prompt_map[new_thread.id] = prompt

    await thread.add_reaction(processing_emoji)
    
    initial_response = ask_question([{"role": "user", "content": prompt}])
    
    if len(initial_response) > 2000:
        chunks = [initial_response[i:i+2000] for i in range(0, len(initial_response), 2000)]
        
        for chunk in chunks:
            await new_thread.send(chunk)
    else:
        await new_thread.send(initial_response)

    await thread.remove_reaction(processing_emoji, bot.user)


@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.Thread):
        if message.channel.id in prompt_map:
            prompt = prompt_map[message.channel.id]
            if message.author != bot.user:
                messages = await message.channel.history(limit=200).flatten()
                messages.reverse()
                gpt_message = list()
                gpt_message.append({"role": "user", "content": prompt})
                
                for channel_message in messages[1:]:
                    if channel_message.author == bot.user:
                        gpt_message.append({"role": "assistant", "content": channel_message.content})
                    else:
                        gpt_message.append({"role": "user", "content": channel_message.content})
               
                
                await messages[-1].add_reaction(processing_emoji)
                
                response = ask_question(gpt_message)
                
                if len(response) > 2000:
                    chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
                    
                    for chunk in chunks:
                        await message.channel.send(chunk)
                else:
                    await message.channel.send(response)
                
                await messages[-1].remove_reaction(processing_emoji, bot.user)



@bot.event
async def on_thread_delete(thread):
    if thread.id in prompt_map:
        del prompt_map[thread.id]
        print(f"Deleted thread {thread.id} from prompt_map")


bot.run(TOKEN)
