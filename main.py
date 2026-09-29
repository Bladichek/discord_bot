import asyncio
import json
from LLM import ask_LLM
import os
import discord
from discord.ext import commands
config = {
    'token': os.getenv('DISCORD_TOKEN'),
    'prefix': 'prefix',
}


names={
    "james__mcgill": "Влад",
    "griiim19": "Серёжа",
    "lonesweetdragon": "Сергун",
    "joeqqqqqqq": "Юрка",
    "k0ves": "Саня",
    "totsamii228": "Гоша",
    "mamaisiayu": "Костя"
}




def generate_prompt(text):
    prompt = f'Ты - профессиональный промпт инженер. Твоя задача - написать промпт для LLM, чтобы она вела себя как яркий персонаж с предоставленным кратким описанием и использовала меньше токенов. Персонаж должен быть очень абсурден и общаться только текстом (без описания действий и своих мыслей). Персонаж должен обращаться к пользователям по имени (если оно указывается. )Вот описание персонажа: {text}'
    print(prompt)
    res = ask_LLM(prompt)
    return res

messages = []

def send_request(text, name):
    global messages, names
    username = names.get(name, 'user')
    messages.append({'role': username, 'context': f'{text}'})
    if len(messages)>10:
        messages.pop(0)
    with open('data.json', 'r', encoding='utf-8') as f:
        prompt=str({'role': 'system', 'context': json.loads(str(f.read()))['base_prompt']})+str(messages)
    res = ask_LLM(prompt)
    messages.append({'role': 'AI', 'context': f'{res}'})
    return res

def parse_commands(text):
    parts = text.split(maxsplit=1)
    command = parts[0]
    args = parts[1] if len(parts) > 1 else ''
    return (command, args)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

@bot.event
async def on_message(message):
    global messages
    if message.author.bot:
        return

    mention = "<@1553481041845555220>"
    if message.content.startswith(mention):
        text = message.content[len(mention):].strip()
        if text:
            if text.startswith('/role') and message.author.id==782628478263492649:

                data = {'base_prompt': generate_prompt(text[len('/role'):].strip())}
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                messages = []
                await message.delete()
                return None


            # Выносим блокирующий вызов в поток
            response = await asyncio.to_thread(send_request, text, message.author.name)
            await message.reply(response)

    await bot.process_commands(message)

bot.run(config['token'])