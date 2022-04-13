import discord
from dotenv import load_dotenv
import os

import img_picker


client = discord.Client()


@client.event
async def on_ready():
    music = discord.Activity(type=discord.ActivityType.listening, name="YURI IS GREAT!")
    await client.change_presence(status=discord.Status.idle, activity=music)
    print("登入成功。")


@client.event
async def on_message(message):
    msg_in = message.content
    if msg_in.startswith("y!"):
        if "百合" in str(message.channel):
            parameter = msg_in[2:]
            if parameter[:4] == "yuri":
                img = discord.File(img_picker.random_pick())
                await message.channel.send(file=img)
            elif parameter[:4] == "nsfw":
                if str(message.auther) == str(message.guild.owner):
                    if message.channel.is_nsfw():
                        embed = discord.Embed(title="nsfw", description="此頻道已啟用nsfw。", color=0xF1411C)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="nsfw", description="此頻道未啟用nsfw。如果想要啟用，請至【編輯頻道】→【概要】→【限制級頻道】啟用。",
                                              color=0xF1411C)
                        await message.channel.send(embed=embed)
        else:
            await message.channel.send("請在「百合」頻道使用此機器人。")


# 取得TOKEN
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(base_dir, "TOKEN.env"))
TOKEN = str(os.getenv("TOKEN"))
client.run(TOKEN)
