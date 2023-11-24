import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
import json
from lets_common_log import logUtils as log
import asyncio
import random
from time import time, localtime, strftime
import datetime
import pytz

import functions

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

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.members = True

bot = discord.Client(intents=intents)

# 주기적으로 0시를 체크하는 태스크
@tasks.loop(seconds=1)
async def check_midnight():
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0:
        # 0시에 실행할 작업을 여기에 추가
        r = await functions.yurinyan(discord, bot, message="").midnightPoint()
        if r is None:
            await functions.send_log_discord(bot, 1162290295380131871, "`yurinyan_` 테이블에 유저 정보가 없음! (포인트)")

# 봇이 준비되었을 때 실행되는 이벤트 핸들러
@bot.event
async def on_ready():
    log.info('루티봇#1579 온라인!')
    check_midnight.start()
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f'{prefix}명령어'))

@bot.event
async def on_member_join(member):
    if member.guild.id == guild_id:
        channel = bot.get_channel(welcome_channel)
        if channel is None:
            return

        embed = discord.Embed(
            title=f'안녕하세요, {member.name} 님! 서버에 가입하신 것을 환영합니다!',
            color=0xF280EB
        )
        embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.timestamp = datetime.datetime.now(pytz.utc)
        embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')

        await channel.send(f'<@{member.id}>', embed=embed)

        role_id_to_add = welcome_role_id
        role_to_add = get(member.guild.roles, id=role_id_to_add)
        if role_to_add is not None:
            try:
                await member.add_roles(role_to_add)
                await functions.send_log_discord(bot, discord_log_channel, f'<@{member.id}>에게 <@&{role_id_to_add}> 인증되지 않은 역할 부여함')
            except Exception as error:
                log.error(f'역할 추가 중 오류 발생: {error}')
        else:
            log.error(f'역할을 찾을 수 없음: {role_id_to_add}')

@bot.event
async def on_member_remove(member):
    if member.guild.id == guild_id:
        channel = bot.get_channel(welcome_channel)
        if channel is None:
            return

        embed = discord.Embed(
            title=f'안녕히 가세요, {member.name} 님! 서버에서 나가셨습니다.',
            color=0xFF5733
        )
        embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.timestamp = datetime.datetime.now(pytz.utc)
        embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')

        await channel.send(f'<@{member.id}>', embed=embed)

#zira봇 역할
zira = functions.db().fetch("SELECT * FROM rutibot_zira WHERE type = %s", ("minecraft"))
if zira is None:
    log.error(f"zira | DB에 설정값이 존재 하지 않음!!!")
else:
    CHANNEL_ID = zira["CHANNEL_ID"]  # 이벤트를 감지할 채널 ID
    MESSAGE_ID = zira["MESSAGE_ID"]  # 이벤트를 감지할 메시지 ID
    EMOJI_NAME = zira["EMOJI_NAME"]  # 반응에 사용할 이모지 이름
    ROLE_ID = zira["ROLE_ID"]  # 부여할 역할 ID

@bot.event
async def on_raw_reaction_add(payload):
    # 반응한 메시지가 지정한 채널에 있는지 확인합니다.
    if payload.channel_id != CHANNEL_ID:
        return

    # 반응한 메시지가 지정한 메시지인지 확인합니다.
    if payload.message_id == MESSAGE_ID and payload.emoji.name == EMOJI_NAME:
        member = bot.get_guild(payload.guild_id).get_member(payload.user_id)
        role = bot.get_guild(payload.guild_id).get_role(ROLE_ID)
        if member and role:
            await member.add_roles(role)

            embed = discord.Embed(
                title=f"[{member.name}]에게 [{role.name}] 역할을 추가했습니다.",
                description=f"<@{member.id}>에게 <@&{role.id}> 역할을 추가했습니다.",
                color=0xFF5733
            )
            embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.timestamp = datetime.datetime.now(pytz.utc)
            embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
            await functions.send_log_discord(bot, discord_log_channel, ["", embed], isEmbed=True)

@bot.event
async def on_raw_reaction_remove(payload):
    # 반응한 메시지가 지정한 채널에 있는지 확인합니다.
    if payload.channel_id != CHANNEL_ID:
        return

    # 반응한 메시지가 지정한 메시지인지 확인합니다.
    if payload.message_id == MESSAGE_ID and payload.emoji.name == EMOJI_NAME:
        member = bot.get_guild(payload.guild_id).get_member(payload.user_id)
        role = bot.get_guild(payload.guild_id).get_role(ROLE_ID)
        if member and role:
            await member.remove_roles(role)
            
            embed = discord.Embed(
                title=f"[{member.name}]에게 [{role.name}] 역할을 제거했습니다.",
                description=f"<@{member.id}>에게 <@&{role.id}> 역할을 제거했습니다.",
                color=0xFF5733
            )
            embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.timestamp = datetime.datetime.now(pytz.utc)
            embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
            await functions.send_log_discord(bot, discord_log_channel, ["", embed], isEmbed=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    chatLog = f"Server:{message.guild} | Channel:{message.channel} | User: {message.author} | Message:{message.content}"
    log.chat(chatLog)
    # 파일을 추가 모드로 열고 데이터 추가하기
    with open('chatlog.txt', 'a', encoding="UTF-8") as file:
        file.write(f'[{strftime("%Y-%m-%d %H:%M:%S", localtime())}] - {chatLog}\n\n')


    if message.content == f"{prefix}명령어" or message.content == f"{prefix}command" or message.content == f"{prefix}commands":
        embed = discord.Embed(
            title='명령어',
            color=0xFF0000
        )
        embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
        embed.add_field(name=f'{prefix}명령어', value='명령어를 보여줍니다.')
        embed.add_field(name=f'{prefix}봇 초대', value='봇 초대 주소입니다.')
        embed.add_field(name=f'{prefix}ping', value=f'봇의 서버핑을 보여줍니다. (음악봇 `{prefix}ping`이랑 중복됨)')
        embed.add_field(name=f'{prefix}투표', value=f'O 또는 X 로 투표를 할 수 있습니다.\n사용법: `{prefix}투표 투표할 내용`')
        embed.add_field(name=f'{prefix}홈페이지', value='운영중인 홈페이지 주소를 보여줍니다.')
        embed.add_field(name=f'{prefix}github', value='깃허브 페이지')
        embed.add_field(name=f'{prefix}clear [지울 만큼의 숫자]', value=f'입력받은 개수의 메세지 삭제 (`{prefix}clear` 명령어는 포함하지 않음)')
        embed.add_field(name=f'{prefix}help (!h)', value=f'`{prefix}help` (`{prefix}h`) 음악봇 관련 명령어 입니다.')
        embed.add_field(name=f'{prefix}마니또 추첨', value='마니또를 추첨하는 명령어 입니다. (합방 시작 전에 관리자들 끼리 합의 하에 추첨을 하고 그걸 고정해서 사용할 예정)')
        embed.add_field(name=f'{prefix}게임', value=f'`{prefix}게임` 명령어로 어떤 게임들이 있는지 확인하는 명령어 입니다.')
        embed.add_field(name=f'{prefix}유리냥이', value=f'<@657145673296117760> 만 사용 가능한 명령어')
        embed.timestamp = message.created_at
        embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
        return await message.reply(embed=embed)

    if message.content == f"{prefix}게임":
        embed = discord.Embed(
            title='게임 명령어',
            color=0xFF0000
        )
        embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
        embed.add_field(name=f'{prefix}계란깨기시작', value='계란깨기 게임을 시작합니다.')
        embed.add_field(name=f'{prefix}계란깨기 [숫자]', value=f'예시로 `{prefix}계란깨기 44`를 입력하면 되고 숫자의 범위는 1~100입니다.')
        embed.add_field(name=f'{prefix}계란깨기종료', value='계란깨기 게임을 종료합니다.')
        embed.timestamp = message.created_at
        embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
        return await message.reply(embed=embed)


    if message.content.startswith(f"{prefix}투표"):
        try:
            des = message.content.split(' ')[1]
        except:
            return await message.reply("투표할 내용이 감지되지 않습니다!")

        embed = discord.Embed(
            title='👇 투표내용  (Voting contents)',
            description=des,
            color=0xFF0000
        )
        embed.set_author(name='루티봇#1579', icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
        embed.timestamp = message.created_at
        embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
        
        message = await message.reply(embed=embed)
        await message.add_reaction("⭕")
        await message.add_reaction("❌")
        return

    if message.content.startswith(f"{prefix}홈페이지"):
        embed = discord.Embed(
            title='명령어',
            color=0xFF0000
        )
        embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
        embed.add_field(name='https://collabo.lol/pokemon', value='마크 1.12.2 포켓몬 서버 홈페이지')
        embed.add_field(name='https://collabo.lol/pvp', value='마크 1.20.1 PVP, 건축 서버 홈페이지')
        embed.timestamp = message.created_at
        embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
        
        return await message.reply(embed=embed)

    if message.content == f"{prefix}서버주소" or message.content == f"{prefix}서버 주소" or message.content == f"{prefix}마크":
        return await message.reply(f'`{prefix}홈페이지` 명령어를 사용해주세요!')

    if message.content == f"{prefix}github" or message.content == f"{prefix}깃허브" or message.content == f"{prefix}깃헙":
        embed = discord.Embed(
            title='Github links',
            color=0xFF0000
        )
        embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
        embed.add_field(name='https://github.com/skchqhdpdy', value='<@399535550832443392>의 github 페이지')
        embed.add_field(name='https://github.com/skchqhdpdy/rutibot1579', value='<@1143492519276060752>의 소스코드')
        embed.add_field(name='https://github.com/skchqhdpdy/2024-Twitch-Streamer-Collabo', value='web 페이지 소스코드?')
        embed.timestamp = message.created_at
        embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
        
        return await message.reply(embed=embed)

    if message.content == f"{prefix}트위치" or message.content == f"{prefix}twitch":
        await message.reply('<@399535550832443392> 야 너 기능 만들어! (유저 추가 하셈 ㅇㅇ)')

        descript = ""
        streamerList = functions.db().fetch("SELECT * FROM streamerList", param=None)
        if streamerList is None:
            return await message.reply(f"스트리머들의 데이터가 DB에 존재하지 않습니다! 관리자한테 문의해 주세요!")
        elif type(streamerList) is list:
            for i in streamerList:
                descript += f"https://twitch.tv/{i['twitch_id']} | `{i['twitch_name']}`의 트위치 <@{i['discord_userid']}> \n\n"
        elif type(streamerList) is dict:
            descript += f"https://twitch.tv/{streamerList['twitch_id']} | `{streamerList['twitch_name']}`의 트위치 <@{streamerList['discord_userid']}>"
        
        embed = discord.Embed(
            title='스트리머 리스트',
            description=descript,
            color=0xFF0000
        )
        embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
        embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
        embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')

        return await message.reply(embed=embed)

    if message.content.startswith(f"{prefix}clear"):
        if not message.author.guild_permissions.manage_messages:
            return await message.reply("권한이 없습니다.")

        try:
            amount = int(message.content.split(' ')[1])
        except:
            amount = 0

        if amount < 1 or amount > 100:
            await message.reply("1부터 100까지의 숫자만 입력하세요.")
            return

        await message.channel.purge(limit=amount + 1)
        #무조건 message.channel.send 쓰기
        msg = await message.channel.send(f"{amount}개의 메시지를 삭제했습니다. 이 메시지는 3초 후 삭제됩니다.")
        await asyncio.sleep(1)

        for i in range(2, 0, -1):
            await msg.edit(content=f"{amount}개의 메시지를 삭제했습니다. 이 메시지는 {i}초 후 삭제됩니다.")
            await asyncio.sleep(1)

        return await msg.delete()

    # 마니또 추첨
    async def manitoResult(member_lists, except_users):
        descript = ""
        for i in member_lists:
            userCashe = bot.get_user(i["from"])
            if i["order"] == 1:
                descript += "----------------------------------------\n"
                descript += f"{i['order']}번째 | <@{i['from']}> --> <@{i['to']}>\n"
            elif i["order"] == 4:
                descript += f"{i['order']}번째 | <@{i['from']}> --> <@{i['to']}>\n"
                descript += "----------------------------------------\n"
            else:
                descript += f"{i['order']}번째 | <@{i['from']}> --> <@{i['to']}>\n"

        descript += "----------------------------------------\n예외처리 (참가 안함)\n"

        for user in except_users:
            descript += f"<@{user}>\n"

        descript += f"----------------------------------------\n혹시 유저이름이 보이지 않고 숫자만 보인다면 `<@유저ID>` (그냥 파란색 부분 전체 복사 하면 됨) 를 아무 채팅방에 입력하면 상대방을 멘션해서 누군지 알 수 있습니다. (대신 대상자가 해당 채널을 읽을 수 있다면 알람이 가기 떄문에 {bot.user.mention} 에게 갠디로 하는 것을 추천합니다.)\n----------------------------------------"
        return descript

    if message.content.startswith(f"{prefix}마니또"):
        if "조회" in message.content:
            if "전체조회" in message.content:
                sel = False
                selAll = True
            else:
                sel = True
                selAll = False
        else:
            sel = False
            selAll = False

        if "추첨" in message.content:
            pick = True
        else:
            pick = False

        if "확정" in message.content:
            if pick:
                confirmed = True
            else:
                return await message.reply(f"`{prefix}마니또 전체조회`(관리자용), `{prefix}마니또 추첨`, `{prefix}마니또 추첨 확정` \n\n형식으로 입력해주세요!")
        else:
            confirmed = False

        if confirmed and not message.author.guild_permissions.manage_messages:
            return await message.reply("마니또 확정 권한이 없습니다.")

        if pick:
            role_to_find = '스트리머'
            guild = bot.get_guild(guild_id)
            role = discord.utils.get(guild.roles, name=role_to_find)

            if not role:
                return await message.reply('역할을 찾을 수 없습니다.')

            # 스트리머 역할을 가진 멤버 목록을 추출합니다.
            streamer_members = [member for member in guild.members if role in member.roles]

            # 마니또 참가자 목록
            # 끼음, 복미, 오소희, 솜팡, 남야 님은 반확정이라서 넣어줘용

            # 저랑 쥐님이랑 공허님(hyp로시작하는분)빼고
            # 레오욘
            # 아카나, 게임조선, 예외처리해주세요
            # (쥐 님은 서버 나감)
            # 유채란, 하니, 하야애

            participants = []
            except_users = [
                657145673296117760,
                472607419474640897,
                448274272104873984,
                1091687087058731048,
                608142953759637534,
                901685620768915526,
                911662717037846599,
                1075352635961524224,
                506451468719751178,
                479254872739545089
            ]

            for member in streamer_members:
                # @스트리머 역할중 6명 제외
                if member.id not in except_users:
                    participants.append(member.id)

            # 총 4명의 유저는 예외로 서로서로 마니또
            # 제외유저 추가
            each_manito = random.sample(participants, k=4)

            # 기존 유저에서 제외 유저 제거
            for manito in each_manito:
                participants.remove(manito)

            # 참가자를 무작위로 섞기
            random.shuffle(participants)
            # 마니또 매칭
            part_member = [(giver, participants[(i + 1) % len(participants)]) for i, giver in enumerate(participants)]

            member_lists = [
                {"order": 1, "from": each_manito[0], "to": each_manito[1]},
                {"order": 2, "from": each_manito[1], "to": each_manito[0]},
                {"order": 3, "from": each_manito[2], "to": each_manito[3]},
                {"order": 4, "from": each_manito[3], "to": each_manito[2]}
            ]

            for idx, (giver, receiver) in enumerate(part_member, start=5):
                member_lists.append({"order": idx, "from": giver, "to": receiver})

            descript = await manitoResult(member_lists, except_users)

            embed = discord.Embed(
                title="마티또 추첨!",
                description=descript,
                color=0xF280EB
            )

            embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
            embed.set_thumbnail(url="https://collabo.lol/img/manito.jpg")
            embed.timestamp = message.created_at
            embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')

            await message.reply(embed=embed)

            functions.db().execute("INSERT INTO rutibot_manito (id, data_users, except_users, confirmed, datetime) VALUE (%s, %s, %s, %s, %s)", ('NULL', json.dumps(member_lists), str(except_users), confirmed, time()))
        
        if confirmed:
            mt = functions.db().fetch("SELECT * FROM rutibot_manito WHERE confirmed = %s ORDER BY datetime DESC LIMIT 1", (1))
            if mt is None:
                log.error(f"mt | DB에 설정값이 존재 하지 않음!!!")
                return await message.reply("마니또 추첨 확정 데이터가 없습니다!")
            data_users = json.loads(mt["data_users"])
            except_users = json.loads(mt["except_users"])
            orderTime = mt['datetime']
            
            await message.reply(f"<t:{orderTime}> 에 마니또 확정됨!")

            guild = bot.get_guild(guild_id)
            manito_category_id = functions.db().fetch("SELECT manito_category_id FROM rutibot_setting", param=None)["manito_category_id"]
            ct = discord.utils.get(guild.categories, id=manito_category_id)
            ewol = []
            for i in [member for member in guild.members if discord.utils.get(guild.roles, id=manager_role_id) in member.roles]:
                ewol.append(i.id)

            for chans in ct.channels:
                user = 0
                for j in chans.members:
                    if not j.id in ewol:
                        user = j.id
                        break
                userdata = {}
                for i in data_users:
                    if i["from"] == user:
                        descript = await manitoResult([i], except_users)

                        embed = discord.Embed(
                            title="마니또 결과!",
                            description=descript,
                            color=0xF280EB
                        )

                        embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
                        embed.set_thumbnail(url="https://collabo.lol/img/manito.jpg")
                        embed.add_field(name=chans, value=i)
                        embed.timestamp = message.created_at
                        embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')

                        msg_pin = await chans.send(f"<#{message.channel.id}> 채널에서 `{prefix}마니또 추첨 확정` 명령어를 사용하여 마니또의 결과가 나왔습니다!", embed=embed)
                        return await msg_pin.pin()

        if selAll and not pick and not confirmed:
            if not message.author.guild_permissions.manage_messages:
                return await message.reply("권한이 없습니다.")

            mt = functions.db().fetch("SELECT * FROM rutibot_manito WHERE confirmed = %s ORDER BY datetime DESC LIMIT 1", (1))
            if mt is None:
                log.error(f"mt | DB에 설정값이 존재 하지 않음!!!")
                return await message.reply("마니또 추첨 확정 데이터가 없습니다!")
            data_users = json.loads(mt["data_users"])
            except_users = json.loads(mt["except_users"])
            orderTime = mt['datetime']

            descript = await manitoResult(data_users, except_users)
            
            embed = discord.Embed(
                title=f"마티또 조회! \n\n마지막 추첨 : <t:{orderTime}>",
                description=descript,
                color=0xF280EB
            )

            embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
            embed.set_thumbnail(url="https://collabo.lol/img/manito.jpg")
            embed.timestamp = message.created_at
            embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')

            return await message.reply(f"마지막 추첨은 <t:{orderTime}>에 추첨되었습니다!", embed=embed)

        if not sel and not selAll and not pick and not confirmed:
            return await message.reply(f"`{prefix}마니또 전체조회`(관리자용), `{prefix}마니또 추첨`, `{prefix}마니또 추첨 확정` \n\n형식으로 입력해주세요!")

        return

    # 계란 꺠기 게임
    # 게임 상태 변수
    game_egg = functions.db().fetch("SELECT * from rutibot_game_egg", param=None)
    if game_egg is None:
        log.error(f"game_egg | DB에 설정값이 존재 하지 않음!!!")
    else:
        timer_sec = game_egg["timer_sec"]
        eggCount = game_egg["eggCount"]
        eggCountMax = game_egg["eggCountMax"]
        isGameActive_eggGame = True if game_egg["isGameActive_eggGame"] == 1 else False #False
        brokeEggNumber_eggGame = json.loads(game_egg["brokeEggNumber_eggGame"]) #[]
        players_eggGame = json.loads(game_egg["players_eggGame"]) #{}
        channelID_eggGame = game_egg["channelID_eggGame"] #None
        start_time = game_egg["start_time"] #None

    def timerEggGame(message):
        async def game_timeout():
            msg = '5분간 이용하지 않아 계란깨기 게임이 중지되었습니다.'
            exitEggGame(message, msg)

        return bot.loop.call_later(300, game_timeout)

    async def exitEggGame(message, msg):
        functions.db().execute("""
            UPDATE rutibot_game_egg
            SET
                isGameActive_eggGame = %s,
                brokeEggNumber_eggGame = %s,
                players_eggGame = %s,
                channelID_eggGame = %s,
                start_time = %s
        """, (0, '[]', '{}', 'NULL', 'NULL'))
        await message.reply(msg)
        return await message.channel.send('게임 오버!\n--------------------------------------')

    if message.content == f'{prefix}계란깨기시작' and not isGameActive_eggGame:

        functions.db().execute("""
            UPDATE rutibot_game_egg
            SET
                isGameActive_eggGame = %s,
                channelID_eggGame = %s,
                start_time = %s
        """, (1, message.channel.id, time()))

        await message.reply('계란깨기 게임을 시작합니다!')

        # 1부터 100까지의 숫자 중에서 5개를 선택
        brokeEggNumber_eggGame = random.sample(range(1, eggCountMax + 1), eggCount)
        functions.db().execute("UPDATE rutibot_game_egg SET brokeEggNumber_eggGame = %s", (str(brokeEggNumber_eggGame)))

        print(f"날 계란목록 : {brokeEggNumber_eggGame}")
        return

    elif message.content == f'{prefix}계란깨기시작' and isGameActive_eggGame:
        return await message.reply(f'<#{channelID_eggGame}> 채널에서 게임이 진행 중입니다!')
    
    elif (message.content == f'{prefix}계란깨기종료' or message.content == f'{prefix}계란깨기중지') and isGameActive_eggGame:
        msg = f'<@{message.author.id}>님이 게임을 종료하였습니다.'
        return await exitEggGame(message, msg)
    
    elif message.content.startswith(f'{prefix}계란깨기'):
        if not isGameActive_eggGame:
            return await message.reply(f'`{prefix}계란깨기시작` 명령어로 게임을 먼저 시작하세요!')
        else:
            try:
                userNumber = int(message.content.split(' ')[1])
            except:
                userNumber = 0

            if userNumber < 1 or userNumber > eggCountMax:
                return await message.reply(f'1에서 {eggCountMax} 사이의 숫자를 입력하세요!')
            elif str(userNumber) in players_eggGame:
                return await message.reply(f'{userNumber}는 <@{players_eggGame[str(userNumber)]}>님이 입력했던 숫자입니다. 다른 숫자를 입력하세요!')
            elif userNumber in brokeEggNumber_eggGame:
                msg = f'<@{message.author.id}>님이 날 계란 {brokeEggNumber_eggGame} 중 ({userNumber}번 계란)을 깼습니다.'
                return await exitEggGame(message, msg)
            else:
                players_eggGame[str(userNumber)] = message.author.id
                functions.db().execute("UPDATE rutibot_game_egg SET players_eggGame = %s", (json.dumps(players_eggGame)))
                remainingEggs = eggCountMax - len(players_eggGame)
                return await message.reply(f'{userNumber}는 삶은 계란입니다. 남은 계란의 수는 {remainingEggs}개 입니다.')

    #elif message.channel.id == channelID_eggGame and message.content.startswith(prefix):
    else:
        exfired_check = functions.db().fetch("SELECT timer_sec, isGameActive_eggGame, channelID_eggGame, start_time from rutibot_game_egg", param=None)
        if exfired_check is None:
            log.error(f"exfired_check | DB에 설정값이 존재 하지 않음!!!")
        else:
            timer_sec = exfired_check["timer_sec"]
            isGameActive_eggGame = True if exfired_check["isGameActive_eggGame"] == 1 else False
            channelID_eggGame = exfired_check["channelID_eggGame"]
            start_time = exfired_check["start_time"]
            now = round(time())

        if isGameActive_eggGame and (start_time + timer_sec) < now:
            return await bot.get_channel(channelID_eggGame).send(f"{round(timer_sec / 60)}분 제한중, {round((now - start_time) / 60)}분간 이용하지 않아 계란깨기 게임이 중지되었습니다.")

##////////////////////////////////////////////////////////////이스터 애그/////////////////////////////////////////////////////////////##

    # 비밀 메시지 처리
    if message.content == "비밀":
        return await message.reply("꺅 비밀 들켜버렸다")

    secret_code = functions.db().fetch("SELECT * FROM rutibot_secretcode", param=None)
    if secret_code is None:
        log.error(f"secret_code | DB에 설정값이 존재 하지 않음!!!")
    
    secretCodeStatus = True if secret_code["secretcode_status"] == 1 else False
    secretCode = json.loads(secret_code["SecretCode"])
    secretCodeCh = secret_code["message_channel_id"]
    isFound_and_uid = json.loads(secret_code["isFound_and_uid"])

    for i, j, num in zip(secretCode, isFound_and_uid, range(len(isFound_and_uid))):
        if secretCodeStatus and message.content == i and message.channel.id == secretCodeCh:
            if j == 0:
                isFound_and_uid[num] = message.author.id
                functions.db().execute("UPDATE rutibot_secretcode SET isFound_and_uid = %s", (json.dumps(isFound_and_uid)))
                return await message.reply("이 시크릿 코드 어떻게 아셨나요? 때려맞추신건 아니겠죠? 어쨌든간에 정답입니다!!(?)")
            else:
                return await message.reply(f"<@{j}> 님이 이미 해당 시크릿 코드를 맞췄습니다!")

##/////////////////////////////////////////////////////////////따로뺴둠//////////////////////////////////////////////////////////////##

# 봇 초대 명령어
    if message.content == f"{prefix}봇" or message.content == f"{prefix}봇 초대" or message.content == f"{prefix}봇초대" or message.content == f"{prefix}invite":
        return await message.reply(f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot")

# Ping 명령어
    if message.content == f"{prefix}핑" or message.content == f"{prefix}ping":
        time_take = round(bot.latency * 1000)  # 서버 핑을 밀리초(ms)로 계산
        msg = f"서버 핑은 **{time_take}ms** 입니다."
        log.info(msg)
        return await message.reply(msg)


##/////////////////////////////////////////////////////////////유리냥이//////////////////////////////////////////////////////////////##

    if message.content.startswith(f"{prefix}유리냥이"):
        if message.author.id == 657145673296117760 or message.author.id == 399535550832443392:
            return await functions.yurinyan(discord, bot, message).commands()
        else:
            return await message.reply(f"{prefix}유리냥이 관련 명령어는 <@657145673296117760> 만 사용가능합니다!")

# 봇을 실행합니다.
bot.run(token)