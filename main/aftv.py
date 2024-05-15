import aiohttp
from discord.ext import commands

import functions
from lets_common_log import logUtils as log

config = functions.db().fetch("SELECT * FROM rutibot_setting", param=None)
if config is None:
    log.error(f"config | DB에 설정값이 존재 하지 않음!!!")
    exit()

prefix = config["prefix"]
token = config["token"]
guild_id = config["guild_id"]
discord_log_channel = config["discord_log_channel"]
welcome_channel = config["welcome_channel"]
welcome_role_id = config["welcome_role_id"]
#Twitch_token = config["Twitch_token"]
#manito_category_id = config["manito_category_id"]
manager_role_id = config["manager_role_id"]

# 디스코드 봇 설정
bot = commands.Bot(command_prefix="!")

# 아프리카TV 채팅 API URL
africa_chat_url = "http://api.afreecatv.com/broad/africa_chat"

# 디스코드 봇 시작 시 실행되는 이벤트
@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user.name}")

# 아프리카TV 채팅 가져오기
async def get_africa_chat():
    async with aiohttp.ClientSession() as session:
        async with session.get(africa_chat_url) as response:
            data = await response.json()
            return data

# 주기적으로 아프리카TV 채팅을 가져와 디스코드로 전송
async def update_discord():
    await bot.wait_until_ready()
    channel_id = 123456789012345678  # 디스코드 채널 ID 입력

    while not bot.is_closed():
        africa_chat_data = await get_africa_chat()
        message = africa_chat_data["chat"]

        channel = bot.get_channel(channel_id)
        await channel.send(f"AfreecaTV Chat: {message}")

        await asyncio.sleep(60)  # 60초마다 업데이트

# 디스코드 봇 실행
bot.loop.create_task(update_discord())
bot.run("YOUR_DISCORD_BOT_TOKEN")
