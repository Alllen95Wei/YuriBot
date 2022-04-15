import discord
from dotenv import load_dotenv
import os

import img_picker
import log_writter

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    music = discord.Activity(type=discord.ActivityType.listening, name="YURI IS GREAT!")
    await client.change_presence(status=discord.Status.idle, activity=music)
    log_writter.write_log("-------------------------------------------------------------\n", True)
    log_writter.write_log("\n登入成功！\n目前登入身份：" +
                          str(client.user) + "\n以下為使用紀錄(只要開頭訊息有\"y!\"，則這則訊息和系統回應皆會被記錄)：\n\n")


@client.event
async def on_message(message):
    final_msg_list = []
    final_msg_type_list = []
    msg_in = message.content
    if msg_in.startswith("y!"):
        use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
        log_writter.write_log(use_log)
        if "百合" in str(message.channel):
            parameter = msg_in[2:]
            if parameter == "test":
                final_msg_list.append("test")
                final_msg_type_list.append("text")
            if parameter[:4] == "help":
                embed = discord.Embed(title="協助", description="一隻香香的百合機器人~", color=0xFEE4E4)
                embed.add_field(name="`help`", value="顯示此協助訊息。", inline=False)
                embed.add_field(name="`yuri`", value="顯示隨機一張香香的百合圖。", inline=False)
                embed.add_field(name="`nsfw`", value="檢查並編輯頻道的nsfw狀態。", inline=False)
                final_msg_list.append(embed)
                final_msg_type_list.append("embed")
            elif parameter[:4] == "yuri":
                if message.channel.is_nsfw():
                    img = discord.File(img_picker.random_pick(True))
                else:
                    img = discord.File(img_picker.random_pick())
                final_msg_list.append(img)
                final_msg_type_list.append("file")
            elif parameter[:4] == "nsfw":
                if str(message.author) == str(message.guild.owner):
                    if message.channel.is_nsfw():
                        await message.channel.edit(nsfw=False)
                        embed = discord.Embed(title="nsfw", description="已為此頻道停用nsfw。", color=0xF1411C)
                    else:
                        await message.channel.edit(nsfw=True)
                        embed = discord.Embed(title="nsfw", description="已為此頻道啟用nsfw。", color=0xF1411C)
                elif str(message.guild.owner) == "None":
                    embed = discord.Embed(title="nsfw", description="無法取得伺服器擁有者的資訊。", color=0xF1411C)
                else:
                    if message.channel.is_nsfw():
                        nsfw_status = "啟用"
                    else:
                        nsfw_status = "停用"
                    embed = discord.Embed(title="nsfw", description="目前此頻道{0}nsfw。\n你並非伺服器擁有者。請向**{1}**要求。"
                                          .format(nsfw_status, message.guild.owner), color=0xF1411C)
                final_msg_list.append(embed)
                final_msg_type_list.append("embed")
        else:
            final_msg_list.append("請在「百合」頻道使用此機器人。")
    for i in range(len(final_msg_list)):
        current_msg = final_msg_list[i]
        if isinstance(current_msg, discord.File):
            await message.channel.send(file=final_msg_list[i])
        elif isinstance(current_msg, discord.Embed):
            await message.channel.send(embed=final_msg_list[i])
        elif isinstance(current_msg, str):
            await message.channel.send(final_msg_list[i])
        new_log = str(message.channel) + "/" + str(client.user) + ":\n" + str(final_msg_list[i]) + "\n\n"
        log_writter.write_log(new_log)
        # TODO: 找出訊息重複傳送的問題
    final_msg_list.clear()


# 取得TOKEN
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(base_dir, "TOKEN.env"))
TOKEN = str(os.getenv("TOKEN"))
client.run(TOKEN)
