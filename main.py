import asyncio
import os
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Мы успешно вошли в сеть как {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)

async def main():
    async with bot:
        await bot.load_extension('commands')
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
