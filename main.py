import discord
from dotenv import load_dotenv
import os
from platform import system

import img_picker
import log_writter
import update

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    music = discord.Activity(type=discord.ActivityType.listening, name="YURI IS GREAT!")
    await client.change_presence(status=discord.Status.idle, activity=music)
    log_writter.write_log("-------------------------------------------------------------\n", True)
    log_writter.write_log("\n登入成功！\n目前登入身份：" +
                          str(client.user) + "\n以下為使用紀錄(只要開頭訊息有\"y!\"，則這則訊息和系統回應皆會被記錄)：\n\n")


test_mode = False
current_os = system()


@client.event
async def on_message(message):
    global test_mode
    final_msg_list = []
    msg_in = message.content
    if msg_in.startswith("y!"):
        if msg_in == "y!test":
            use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
            log_writter.write_log(use_log)
            if test_mode:
                test_mode = False
                embed = discord.Embed(title="測試模式", description="測試模式已**關閉**。", color=0xFEE4E4)
                final_msg_list.append(embed)
            else:
                test_mode = True
                embed = discord.Embed(title="測試模式", description="測試模式已**開啟**。", color=0xFEE4E4)
                final_msg_list.append(embed)
        elif test_mode:
            return
        else:
            use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
            log_writter.write_log(use_log)
            if "百合" in str(message.channel) or "yuri" in str(message.channel).lower() \
                    and "Direct Message" not in str(message.channel):
                parameter = msg_in[2:]
                if parameter == "":
                    embed = discord.Embed(title="百合機器人在此！", description="使用`y!help`來取得指令支援。", color=0xFEE4E4)
                    final_msg_list.append(embed)
                if parameter == "test":
                    final_msg_list.append("test")
                if parameter[:4] == "help":
                    embed = discord.Embed(title="協助", description="一隻香香的百合機器人~", color=0xFEE4E4)
                    embed.add_field(name="`help`", value="顯示此協助訊息。", inline=False)
                    embed.add_field(name="`yuri`", value="顯示隨機一張香香的百合圖。", inline=False)
                    embed.add_field(name="`nsfw`", value="檢查並編輯頻道的nsfw狀態。", inline=False)
                    embed.add_field(name="`setchannel`", value="更改目前的頻道名稱為「黃金百合聖教會-`<伺服器名稱>`分會」。", inline=False)
                    embed.add_field(name="`ping`", value="查看百合機器人的延遲毫秒數。", inline=False)
                    embed.add_field(name="`sendlog`", value="傳送紀錄文件(`log.txt`)。", inline=False)
                    embed.add_field(name="`test`", value="開啟或關閉測試模式。", inline=False)
                    embed.add_field(name="`poem`", value="讚嘆百合。", inline=False)
                    embed.add_field(name="`about`", value="取得Yuri Bot的詳細資訊。", inline=False)
                    final_msg_list.append(embed)
                elif parameter[:4] == "yuri":
                    if message.channel.is_nsfw():
                        img = discord.File(img_picker.random_pick(True, current_os))
                    else:
                        img = discord.File(img_picker.random_pick(current_os=current_os))
                    final_msg_list.append(img)
                elif parameter[:4] == "nsfw":
                    if str(message.author) == str(message.guild.owner):
                        if message.channel.is_nsfw():
                            await message.channel.edit(nsfw=False, reason="{0}使用了y!nsfw指令".format(message.author))
                            embed = discord.Embed(title="nsfw", description="已為此頻道停用nsfw。", color=0xF1411C)
                        else:
                            await message.channel.edit(nsfw=True, reason="{0}使用了y!nsfw指令".format(message.author))
                            embed = discord.Embed(title="nsfw", description="已為此頻道啟用nsfw。", color=0xF1411C)
                    elif str(message.guild.owner) == "None":
                        embed = discord.Embed(title="nsfw", description="無法取得伺服器擁有者的資訊。", color=0xF1411C)
                    else:
                        if message.channel.is_nsfw():
                            nsfw_status = "啟用"
                        else:
                            nsfw_status = "停用"
                        embed = discord.Embed(title="nsfw", description="目前此頻道{0}nsfw。\n你並非伺服器擁有者。請向**{1}**要求更改設定。"
                                              .format(nsfw_status, message.guild.owner), color=0xF1411C)
                    final_msg_list.append(embed)
                elif parameter[:10] == "setchannel":
                    try:
                        await message.channel.edit(name="黃金百合聖教會-{0}地區分會".format(message.guild.name),
                                                   reason="{0}使用了y!setchannel指令".format(message.author))
                        embed = discord.Embed(title="setchannel", description="已為此頻道重新命名為黃金百合聖教會-{0}地區分會。"
                                              .format(message.guild.name), color=0xFEE4E4)
                        final_msg_list.append(embed)
                    except Exception as e:
                        if "Missing Permissions" in str(e):
                            e = "權限不足。"
                        embed = discord.Embed(title="頻道設定", description="設定頻道失敗。原因：{0}".format(e), color=0xF1411C)
                        final_msg_list.append(embed)
                elif parameter[:4] == "ping":
                    embed = discord.Embed(title="ping", description="延遲：{0}ms"
                                          .format(str(round(client.latency * 1000))), color=0xFEE4E4)
                    final_msg_list.append(embed)
                elif parameter[:7] == "sendlog":
                    if str(message.author) == str(client.get_user(657519721138094080)):
                        embed = discord.Embed(title="sendlog", description="已嘗試傳送`log.txt`至聊天室。", color=0xFEE4E4)
                        final_msg_list.append(discord.File("log.txt"))
                    else:
                        embed = discord.Embed(title="sendlog", description="你並非{0}，因此無權查看紀錄文件。"
                                              .format(client.get_user(657519721138094080)), color=0xF1411C)
                    final_msg_list.append(embed)
                elif parameter[:4] == "poem":
                    embed = discord.Embed(title="poem",
                                          description="所以，現在是讚嘆百合的時間！請跟著下面的文字一起念！\n\n**"
                                                      "百合百合 百年好合 幸福長久 唯有百合\n入坑百合 神又如何 開口閉口 句句百合\n百合結婚 毫不違和 我嗑百合 有品有德"
                                                      "**\n--*教主 劉采妮*",
                                          color=0xFEE4E4)
                    final_msg_list.append(embed)
                elif parameter[:5] == "about":
                    embed = discord.Embed(title="about",
                                          description="**Yuri Bot**是Allen Wei使用discord.py所製作出的Discord Bot。",
                                          color=0xFEE4E4)
                    embed.add_field(name="程式碼與授權", value="程式碼可在[GitHub](https://github.com/Alllen95Wei/YuriBot)查看。"
                                                         "\n本程式依據GPL-3.0 License授權。你可以在[這裡]"
                                                         "(https://github.com/Alllen95Wei/YuriBot/blob/master/LICENSE)"
                                                         "查看條款。")
                    embed.add_field(name="聯絡", value="如果你有任何問題，請聯絡Allen Why#5877。")
                    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/963578274909392957"
                                            "/0f67fa0d6f9a80ef840936ab21cba1da.webp?size=1024")
                    embed.set_footer(text="©Copyright Allen Wei, 2022.")
                    final_msg_list.append(embed)
                elif parameter[:6] == "update":
                    if str(message.author) == str(client.get_user(657519721138094080)):
                        embed = discord.Embed(title="update", description="已嘗試從GitHub取得更新。請稍待。", color=0xFEE4E4)
                        update.update(os.getpid())
                        final_msg_list.append(embed)
                    else:
                        embed = discord.Embed(title="update", description="你並非{0}，因此無權更新程式。"
                                              .format(client.get_user(657519721138094080)), color=0xF1411C)
                        final_msg_list.append(embed)
            elif msg_in == "y!setchannel":
                try:
                    await message.channel.edit(name="黃金百合聖教會-{0}地區分會".format(message.guild.name),
                                               reason="{0}使用了y!setchannel指令".format(message.author))
                    embed = discord.Embed(title="setchannel", description="已為此頻道重新命名為黃金百合聖教會-{0}地區分會。"
                                          .format(message.guild.name), color=0xFEE4E4)
                    final_msg_list.append(embed)
                except Exception as e:
                    if "Missing Permissions" in str(e):
                        e = "權限不足。"
                    embed = discord.Embed(title="頻道設定", description="設定頻道失敗。原因：{0}".format(e), color=0xF1411C)
                    final_msg_list.append(embed)
            else:
                embed = discord.Embed(title="頻道錯誤", description="請在「百合」頻道使用此機器人。", color=0xFEE4E4)
                final_msg_list.append(embed)
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
    final_msg_list.clear()


# 取得TOKEN
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(base_dir, "TOKEN.env"))
TOKEN = str(os.getenv("TOKEN"))
client.run(TOKEN)
