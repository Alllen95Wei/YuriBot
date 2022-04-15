import discord
from dotenv import load_dotenv
import os

import img_picker
import log_writter


client = discord.Client()
final_msg_list = []


@client.event
async def on_ready():
    music = discord.Activity(type=discord.ActivityType.listening, name="YURI IS GREAT!")
    await client.change_presence(status=discord.Status.idle, activity=music)
    log_writter.write_log("-------------------------------------------------------------\n", True)
    log_writter.write_log("\n登入成功！\n目前登入身份：" +
                          str(client.user) + "\n以下為使用紀錄(只要開頭訊息有\"y!\"，則這則訊息和系統回應皆會被記錄)：\n\n")


@client.event
async def on_message(message):
    global final_msg_list
    msg_in = message.content
    if msg_in.startswith("y!"):
        use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
        log_writter.write_log(use_log)
        if "百合" in str(message.channel):
            parameter = msg_in[2:]
            if parameter == "test":
                await message.channel.send("test")
            if parameter[:4] == "help":
                embed = discord.Embed(title="協助", description="一隻香香的百合機器人~", color=0xFEE4E4)
                embed.add_field(name="`help`", value="顯示此協助訊息。", inline=False)
                embed.add_field(name="`yuri`", value="顯示隨機一張香香的百合圖。", inline=False)
                embed.add_field(name="`nsfw`", value="檢查頻道的nsfw。", inline=False)
                final_msg_list.append(embed)
            elif parameter[:4] == "yuri":
                if message.channel.is_nsfw():
                    img = discord.File(img_picker.random_pick(True))
                else:
                    img = discord.File(img_picker.random_pick())
                final_msg_list.append(img)
            elif parameter[:4] == "nsfw":
                if message.channel.is_nsfw():
                    embed = discord.Embed(title="nsfw", description="此頻道已啟用nsfw。", color=0xF1411C)
                else:
                    embed = discord.Embed(title="nsfw", description="此頻道未啟用nsfw。如果想要啟用，請至【編輯頻道】→【概要】→【限制級頻道】啟用。",
                                          color=0xF1411C)
                final_msg_list.append(embed)
        else:
            await message.channel.send("請在「百合」頻道使用此機器人。")
    for i in range(len(final_msg_list)):
        new_log = str(message.channel) + "/" + str(client.user) + ":\n" + str(final_msg_list[i-1]) + "\n\n"
        log_writter.write_log(new_log)
        if isinstance(final_msg_list[i], discord.File):
            await message.channel.send(file=final_msg_list[i])
        elif isinstance(final_msg_list[i], discord.Embed):
            await message.channel.send(embed=final_msg_list[i])
        elif isinstance(final_msg_list[i], str):
            await message.channel.send(final_msg_list[i])
        # TODO: 找出訊息重複傳送的問題
    final_msg_list.clear()


# 取得TOKEN
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(base_dir, "TOKEN.env"))
TOKEN = str(os.getenv("TOKEN"))
client.run(TOKEN)
