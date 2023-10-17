import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import json
from lets_common_log import logUtils as log
import asyncio
import random

import functions

with open('config.json') as config_file:
    config = json.load(config_file)

prefix = config["prefix"]
token = config["token"]

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.members = True

# 봇의 명령어 접두사(prefix)를 정의합니다.
bot = commands.Bot(command_prefix=prefix, intents=intents)

# 봇이 준비되었을 때 실행되는 이벤트 핸들러
@bot.event
async def on_ready():
    log.info('루티봇#1579 온라인!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f'{prefix}명령어'))
    
@bot.event
async def guildMemberAdd(member):
    channel = bot.get_channel(1149986137377620029)
    if channel is None:
        return

    embed = discord.Embed(
        title=f'안녕하세요, {member.name} 님! 서버에 가입하신 것을 환영합니다!',
        color=0xF280EB,
        timestamp=member.joined_at
    )
    embed.set_author(name='루티봇#1579', icon_url='https://collabo.lol/img/setAuthor.webp')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')

    await channel.send(f'<@{member.id}>', embed=embed)

    role_id_to_add = 1158693253999243325
    role_to_add = get(member.guild.roles, id=role_id_to_add)
    if role_to_add is not None:
        try:
            await member.add_roles(role_to_add)
            await functions.send_log_discord(bot, '1152894841236246558', f'<@{member.id}>에게 <@&{role_id_to_add}> 인증되지 않은 역할 부여함')
        except Exception as error:
            log.error(f'역할 추가 중 오류 발생: {error}')
    else:
        log.error(f'역할을 찾을 수 없음: {role_id_to_add}')

@bot.event
async def guildMemberRemove(member):
    channel = bot.get_channel(1149986137377620029)
    if channel is None:
        return

    embed = discord.Embed(
        title=f'안녕히 가세요, {member.name} 님! 서버에서 나가셨습니다.',
        color=0xFF5733,
        timestamp=member.joined_at
    )
    embed.set_author(name='루티봇#1579', icon_url='https://collabo.lol/img/setAuthor.webp')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')

    await channel.send(f'<@{member.id}>', embed=embed)

#zira봇 역할
CHANNEL_ID = 1107570796555149353  # 이벤트를 감지할 채널 ID
MESSAGE_ID = 1145201143023157298  # 이벤트를 감지할 메시지 ID
EMOJI_NAME = "minecraft"  # 반응에 사용할 이모지 이름
ROLE_ID = 1145215725645074442  # 부여할 역할 ID

@bot.event
async def on_raw_reaction_add(payload):
    # 반응한 메시지가 지정한 채널에 있는지 확인합니다.
    if payload.channel_id != CHANNEL_ID:
        return

    # 반응한 메시지가 지정한 메시지인지 확인합니다.
    if payload.message_id == MESSAGE_ID and str(payload.emoji) == EMOJI_NAME:
        member = bot.get_guild(payload.guild_id).get_member(payload.user_id)
        role = bot.get_guild(payload.guild_id).get_role(ROLE_ID)
        if member and role:
            await member.add_roles(role)
            msg = f"[{member.name}]에게 [{role.name}] 역할을 추가했습니다."
            log.info(msg)
            functions.send_log_discord(bot, "1152894841236246558", msg)

@bot.event
async def on_raw_reaction_remove(payload):
    # 반응한 메시지가 지정한 채널에 있는지 확인합니다.
    if payload.channel_id != CHANNEL_ID:
        return

    # 반응한 메시지가 지정한 메시지인지 확인합니다.
    if payload.message_id == MESSAGE_ID and str(payload.emoji) == EMOJI_NAME:
        member = bot.get_guild(payload.guild_id).get_member(payload.user_id)
        role = bot.get_guild(payload.guild_id).get_role(ROLE_ID)
        if member and role:
            await member.remove_roles(role)
            msg = f"[{member.name}]에게 [{role.name}] 역할을 제거했습니다."
            log.info(msg)
            functions.send_log_discord(bot, "1152894841236246558", msg)


#메인
#계란 깨기 게임
is_game_active_egg_game = False  # 게임 진행 여부
broke_egg_numbers_egg_game = []  # 날 계란 번호들
players_egg_game = {}  # 이미 나온 번호(유저) 기록
channel_id_egg_game = ""  # 게임을 시작한 채널의 ID
timeout_id_egg_game = ""  # timeout ID

@bot.command(aliases=["명령어"])
async def commands(ctx):
    embed = discord.Embed(
        title='명령어',
        color=0xFF0000
    )
    embed.set_author(name='루티봇#1579', icon_url='https://collabo.lol/img/setAuthor.webp')
    embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
    embed.add_field(name=f'{prefix}명령어', value='명령어를 보여줍니다.')
    embed.add_field(name=f'{prefix}봇 초대', value='봇 초대 주소입니다.')
    embed.add_field(name=f'{prefix}ping', value=f'봇의 서버핑을 보여줍니다. (음악봇 `{prefix}ping`이랑 중복됨)')
    embed.add_field(name=f'{prefix}투표', value=f'O 또는 X 로 투표를 할 수 있습니다.\n사용법: `{prefix}투표 투표할 내용`')
    embed.add_field(name=f'{prefix}홈페이지', value='운영중인 홈페이지 주소를 보여줍니다.')
    embed.add_field(name=f'{prefix}github', value='깃허브 페이지')
    embed.add_field(name=f'{prefix}clear [지울 만큼의 숫자]', value=f'`{prefix}clear` 명령어를 포함한 개수의 메세지 삭제')
    embed.add_field(name=f'{prefix}help (!h)', value=f'`{prefix}help` (`{prefix}h`) 음악봇 관련 명령어 입니다.')
    embed.add_field(name=f'{prefix}마니또 추첨', value='마니또를 추첨하는 명령어 입니다. (합방 시작 전에 관리자들 끼리 합의 하에 추첨을 하고 그걸 고정해서 사용할 예정)')
    embed.add_field(name=f'{prefix}게임', value=f'`{prefix}게임` 명령어로 어떤 게임들이 있는지 확인하는 명령어 입니다.')
    embed.set_timestamp(ctx.message.created_at)
    embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
    await ctx.send(embed=embed)

@bot.command(aliases=["게임"])
async def games(ctx):
    embed = discord.Embed(
        title='게임 명령어',
        color=0xFF0000
    )
    embed.set_author(name='루티봇#1579', icon_url='https://collabo.lol/img/setAuthor.webp')
    embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
    embed.add_field(name=f'{prefix}계란깨기시작', value='계란깨기 게임을 시작합니다.')
    embed.add_field(name=f'{prefix}계란깨기 [숫자]', value=f'예시로 `{prefix}계란깨기 44`를 입력하면 되고 숫자의 범위는 1~100입니다.')
    embed.add_field(name=f'{prefix}계란깨기중지', value='계란깨기 게임을 중지합니다.')
    embed.set_timestamp(ctx.message.created_at)
    embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
    await ctx.send(embed=embed)


@bot.command(aliases=["투표"])
async def vote(ctx, *, vote_content):
    embed = discord.Embed(
        title='👇 투표내용  (Voting contents)',
        description=vote_content,
        color=0xFF0000
    )
    embed.set_author(name='루티봇#1579', icon_url='https://collabo.lol/img/setAuthor.webp')
    embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
    
    message = await ctx.send(embed=embed)
    await message.add_reaction("⭕")
    await message.add_reaction("❌")

@bot.command(aliases=["홈페이지"])
async def homepage(ctx):
    embed = discord.Embed(
        title='명령어',
        color=0xFF0000
    )
    embed.set_author(name='루티봇#1579', icon_url='https://collabo.lol/img/setAuthor.webp')
    embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
    embed.add_field(name='https://collabo.lol/pokemon', value='마크 1.12.2 포켓몬 서버 홈페이지')
    embed.add_field(name='https://collabo.lol/pvp', value='마크 1.20.1 PVP, 건축 서버 홈페이지')
    embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
    
    await ctx.send(embed=embed)

@bot.command(aliases=["서버주소", "서버 주소", "마크"])
async def server_address(ctx):
    await ctx.reply(f'`{prefix}홈페이지` 명령어를 사용해주세요!')
    await ctx.send(f"{prefix}홈페이지 (봇이 대신 입력해드렸어요!! XD)")

@bot.command(aliases=["깃허브", "깃헙"])
async def github(ctx):
    embed = discord.Embed(
        title='Github links',
        color=0xFF0000
    )
    embed.set_author(name='루티봇#1579', icon_url='https://collabo.lol/img/setAuthor.webp')
    embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
    embed.add_field(name='https://github.com/skchqhdpdy', value='<@399535550832443392>의 github 페이지')
    embed.add_field(name='https://github.com/skchqhdpdy/rutibot1579', value='<@1143492519276060752>의 소스코드')
    embed.add_field(name='https://github.com/skchqhdpdy/2024-Twitch-Streamer-Collabo', value='web 페이지 소스코드?')
    embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
    
    await ctx.send(embed=embed)

@bot.command(aliases=["트위치"])
async def twitch(ctx):
    await ctx.send('<@399535550832443392> 야 너 기능 만들어!')

@bot.command()
async def clear(ctx, amount: int):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("권한이 없습니다.")
        return

    if amount <= 0 or amount > 100:
        await ctx.send("1부터 100까지의 숫자만 입력하세요.")
        return

    await ctx.channel.purge(limit=amount + 1)
    message = await ctx.send(f"{amount}개의 메시지를 삭제했습니다. 이 메시지는 3초 후 삭제됩니다.")
    await asyncio.sleep(3)
    await message.delete()

# 마니또 추첨
# 일정-알려주세요 채널에 메세지도 추가로 보내기 기능 추가하기
# !마니또 추첨 확정
# @해당스트리머 의 마니또는 @스트리머 입니다
@bot.command(aliases=["마니또"])
async def manito(ctx, *args):
    pick = False
    confirmed = False
    try:
        if args[0] == "추첨":
            pick = True

        if args[1] == "확정":
            confirmed = True
            log.info("마니또 확정! | 기능 만들기")
        else:
            log.debug(args)

    except:
        pass

    if pick:
        guild_id = 1107568623050047550
        role_to_find = '스트리머'
        guild = bot.get_guild(guild_id)
        role = discord.utils.get(guild.roles, name=role_to_find)

        if not role:
            print('역할을 찾을 수 없습니다.')
            return

        # 스트리머 역할을 가진 멤버 목록을 추출합니다.
        streamer_members = [member for member in guild.members if role in member.roles]

        # 마니또 참가자 목록
        # 끼음, 복미, 오소희, 솜팡, 남야 님은 반확정이라서 넣어줘용

        # 저랑 쥐님이랑 공허님(hyp로시작하는분)빼고
        # 레오욘
        # 아카나, 게임조선, 예외처리해주세요
        # (쥐 님은 서버 나감)

        participants = []
        except_user = [
            657145673296117760, 
            472607419474640897, 
            448274272104873984, 
            1091687087058731048, 
            608142953759637534, 
            901685620768915526
        ]

        for member in streamer_members:
            # @스트리머 역할중 6명 제외
            if member.id not in except_user:
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
        result_member = [(giver, participants[(i + 1) % len(participants)]) for i, giver in enumerate(participants)]

        descript = f"""
            ----------------------------------------
            1번째 | <@{each_manito[0]}> --> <@{each_manito[1]}>
            2번째 | <@{each_manito[1]}> --> <@{each_manito[0]}>
            3번째 | <@{each_manito[2]}> --> <@{each_manito[3]}>
            4번째 | <@{each_manito[3]}> --> <@{each_manito[2]}>
            ----------------------------------------
        """

        for idx, (giver, receiver) in enumerate(result_member, start=5):
            descript += f"{idx}번째 | <@{giver}> --> <@{receiver}>\n"

        descript += "----------------------------------------\n예외처리 (참가 안함)\n"

        for user in except_user:
            descript += f"<@{user}>\n"

        descript += "----------------------------------------"

        embed = discord.Embed(
            title="마티또 추첨!",
            description=descript,
            color=0xF280EB
        )

        embed.set_author(name="루티봇#1579", icon_url="https://collabo.lol/img/setAuthor.webp")
        embed.set_thumbnail(url="https://collabo.lol/img/마니또.jpg")
        embed.set_footer(text="Made By aodd.xyz", icon_url="https://collabo.lol/img/setFooter.webp")

        await ctx.send(embed=embed)
    
    if confirmed:
        msg = "위에서 기능 만들어서 연결하기"
        log.debug(msg)
        await ctx.reply(msg)

    if not pick and not confirmed:
        msg = "마니또 조회 만들기 (DB연결...?)"
        log.debug(msg)
        await ctx.reply(msg)

# 계란 꺠기 게임
# 게임 상태 변수
isGameActive_eggGame = False
brokeEggNumber_eggGame = []
players_eggGame = {}
channelID_eggGame = ""
timeoutID_eggGame = None
# TODO 나중에 기능 만들기
@bot.command(aliases=["계란깨기"])
async def egg(ctx):
    pass

##////////////////////////////////////////////////////////////이스터 애그/////////////////////////////////////////////////////////////##

# 비밀 메시지 처리
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content == "비밀":
        await message.reply("꺅 비밀 들켜버렸다")

    with open("./secretcode.json", "r", encoding="utf-8") as file:
        secret_code = json.load(file)

    if message.content in secret_code["SecretCode"] and message.channel.id == 1146725666348339323:
        await message.reply("이 시크릿 코드 어떻게 아셨나요? 때려맞추신건 아니겠죠? 어쨌든간에 정답입니다!!(?)")

    await bot.process_commands(message)

##/////////////////////////////////////////////////////////////따로뺴둠//////////////////////////////////////////////////////////////##

# 봇 초대 명령어
@bot.command(aliases=["봇", "봇초대"])
async def invite(ctx, *args):
    try:
        if args[0] == "초대":
            await ctx.reply("https://discord.com/api/oauth2/authorize?client_id=1143492519276060752&permissions=8&scope=bot")
    except:
        await ctx.reply("https://discord.com/api/oauth2/authorize?client_id=1143492519276060752&permissions=8&scope=bot")

# Ping 명령어
@bot.command(aliases=["핑"])
async def ping(ctx):
    time_take = round(bot.latency * 1000)  # 서버 핑을 밀리초(ms)로 계산
    await ctx.reply(f"서버 핑은 **{time_take}ms** 입니다.")
    log.info(f"서버 핑은 **{time_take}ms** 입니다.")

# 봇을 실행합니다.
bot.run(token)
