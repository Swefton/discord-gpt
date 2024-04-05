import openai
from tokens import OPENAI_API_KEY
client = openai.OpenAI(api_key = OPENAI_API_KEY)



completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Write a simple hello world script in arm asm and write a summary on how it works."}
  ]
)

print(completion.choices[0].message.content)
