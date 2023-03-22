import discord, logging
from dotenv import load_dotenv
import os, sys, json

# 別ファイルを取り込む
import open_ai
import sql_interface

# ログの設定
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('../logs/discord.log'),
    ])

# インテンツ？
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

load_dotenv()

# sqlの管理
sm = sql_interface.SessionManager()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # AI専用のチャンネル
    if message.channel.name == "chatgpt-threads":
        if message.channel.type == discord.ChannelType.text:
            thread = await message.create_thread(
                name=message.content,
            )
    
    # スレッドに対する
    if message.channel.type == discord.ChannelType.public_thread:
        input_prompt = message.content.strip()
        system_prompt = message.channel.name
        msg_history = []
        for prompt, completion in sm.get_pair_list(message.channel.id):
            msg_history.append({"role":"user", "content": prompt})
            msg_history.append({"role":"assistant", "content": completion})
        async with message.channel.typing():
            completion = await open_ai.gptTurbo(system_prompt, msg_history, input_prompt)
        sm.add_record(input_prompt, completion, message.channel.id)
        await message.channel.send(completion)

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client.run(TOKEN)
