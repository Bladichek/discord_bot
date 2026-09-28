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

def generate_prompt(text):
    prompt = f'Ты - профессиональный промпт инженер. Твоя задача - написать промпт для LLM, чтобы она вела себя как яркий персонаж с предоставленным кратким описанием и использовала меньше токенов. Персонаж должен быть очень абсурден и общаться только текстом (без описания действий и своих мыслей). Вот описание персонажа: {text}'
    res = ask_LLM(prompt)
    return res

messages = []

def send_request(text):
    global messages
    messages.append({'role': 'user', 'context': f'{text}'})
    if len(messages)>10:
        messages.pop(0)
    with open('data.json', 'r') as f:
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
    if message.author.bot:
        return

    mention = "@Зелёный дедушка"
    if message.content.startswith(mention):
        text = message.content[len(mention):].strip()
        if text:
            # Выносим блокирующий вызов в поток
            response = await asyncio.to_thread(send_request, text)
            await message.reply(response)

    await bot.process_commands(message)

bot.run(config['token'])