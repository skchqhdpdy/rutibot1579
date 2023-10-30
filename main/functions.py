import json
import pymysql
import time
import datetime
import pytz

from lets_common_log import logUtils as log

# json 불러오기
def getConfig(file):
    with open(file, "r") as config_file:
        return json.load(config_file)
    
def setConfig(file, update):
    with open(file, "w") as config_file:
        json.dump(update, config_file, indent=4)

class db:
    def connect():
        config = getConfig("config.json")
        host = config["db"]["host"]
        port = int(config["db"]["port"])
        username = config["db"]["username"]
        password = config["db"]["password"]
        database = config["db"]["database"]

        pydb = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8')
        return pydb

    def select(sql):
        pydb = db.connect()
        cursor = pydb.cursor()
        cursor.execute(sql)

        columns = [column[0] for column in cursor.description]
        result = cursor.fetchall()
        pydb.close()

        if not result:
            return None
        elif len(result) == 1:
            data = {}
            for c, r in zip(columns, result[0]):
                data[c] = r
            return data
        else:
            d = []
            for i in result:
                data = {}
                for c, r in zip(columns, i):
                    data[c] = r
                d.append(data)
            return d
        
    def insert(sql):
        pydb = db.connect()
        cursor = pydb.cursor()
        cursor.execute(sql)
        pydb.commit()
        pydb.close()

    def update(sql):
        pydb = db.connect()
        cursor = pydb.cursor()
        cursor.execute(sql)
        pydb.commit()
        pydb.close()

    def delete(sql):
        pydb = db.connect()
        cursor = pydb.cursor()
        cursor.execute(sql)
        pydb.commit()
        pydb.close()

# 디코 채널 로그
async def send_log_discord(bot, channel_id, content, isEmbed=False):
    try:
        target_channel = bot.get_channel(channel_id)
        if target_channel:
            if isEmbed:
                await target_channel.send(content[0], embed=content[1])
            else:
                await target_channel.send(content)
        else:
            log.error(f"<#{channel_id}> 해당 채널을 찾을 수 없음")
    except Exception as error:
        log.error(f'send_log_discord() 함수 예외처리 됨 | error = {error}')

# 계란 꺠기 게임

# 유리냥이
class yurinyan:
    def __init__(self, discord, bot, message):
        config = db.select("SELECT prefix, guild_id, discord_log_channel FROM rutibot_setting")
        if config is None:
            log.error(f"config | DB에 설정값이 존재 하지 않음!!!")
            exit()
        self.prefix = config["prefix"]
        self.guild_id = config["guild_id"]
        self.discord_log_channel = config["discord_log_channel"]
        
        self.discord = discord
        self.bot = bot
        self.message = message

    async def pointSelAll(self):
        descript = ""
        data = db.select("SELECT * FROM yurinyan_")
        if data is None:
            return await self.message.reply(f"유저들의 데이터가 DB에 존재하지 않습니다! `{self.prefix}유리냥이 포인트 유저추가` 명령어로 먼저 유저를 추가하세요!")
        elif type(data) is list:
            for i in data:
                descript += f"<t:{i['last_update']}> 에 업데이트 됨. \n<@{i['discord_userid']}> == `{i['discord_point']}` Point \n\n"
        elif type(data) is dict:
            descript += f"<t:{data['last_update']}> 에 업데이트 됨. \n<@{data['discord_userid']}> == `{data['discord_point']}` Point"

        embed = self.discord.Embed(
            title=f'{self.prefix}유리냥이 포인트 전체조회',
            description=descript,
            color=0xFF0000
        )
        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
        embed.timestamp = datetime.datetime.now(pytz.utc)
        embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
        return embed

    async def midnightPoint(self):
        data = db.select("SELECT * FROM yurinyan_")
        if data is None:
            return None
        elif type(data) is list:
            for i in data:
                db.update(f"UPDATE yurinyan_ SET discord_point = {i['discord_point'] + 1}, last_update = '{time.time()}' WHERE discord_userid = {i['discord_userid']}")
        elif type(data) is dict:
            db.update(f"UPDATE yurinyan_ SET discord_point = {data['discord_point'] + 1}, last_update = '{time.time()}' WHERE discord_userid = {data['discord_userid']}")
        embed = await self.pointSelAll()

        channel = self.bot.get_channel(1162290295380131871)
        return await channel.send(embed=embed)

    async def commands(self):
        if self.message.content == f"{self.prefix}유리냥이":
            embed = self.discord.Embed(
                title=f'{self.prefix}유리냥이 관련 명령어',
                color=0xFF0000
            )
            embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url='https://collabo.lol/img/setThumbnail.webp')
            embed.add_field(name=f'{self.prefix}유리냥이', value=f'{self.prefix}유리냥이 관련 명령어를 보여줍니다.')
            embed.add_field(name=f'{self.prefix}유리냥이 포인트 조회', value=f'특정 유저의 포인트를 조회합니다. (`{self.prefix}유리냥이 포인트 조회 <유저아이디> <포인트>`)')
            embed.add_field(name=f'{self.prefix}유리냥이 포인트 전체조회', value=f'모든 유저의 포인트를 조회합니다. (`{self.prefix}유리냥이 포인트 전체조회`)')
            embed.add_field(name=f'{self.prefix}유리냥이 포인트 유저추가', value=f'포인트 관리를 할 수 있게 DB에 유저를 추가합니다. (`{self.prefix}유리냥이 포인트 유저추가 <유저아이디>`)')
            embed.add_field(name=f'{self.prefix}유리냥이 포인트 지급', value=f'특정 유저에게 포인트를 지급합니다. (`{self.prefix}유리냥이 포인트 지급 <유저아이디> <포인트>`)')
            embed.timestamp = self.message.created_at
            embed.set_footer(text='Made By aodd.xyz', icon_url='https://collabo.lol/img/setFooter.webp')
            return await self.message.reply(embed=embed)

        if self.message.content.startswith(f"{self.prefix}유리냥이 포인트"):           
            if "전체조회" in self.message.content:
                embed = await self.pointSelAll()
                return await self.message.reply(embed=embed)
            elif "조회" in self.message.content:
                try:
                    userID = int(self.message.content.split(' ')[3])
                except:
                    return await self.message.reply("유저 아이디가 감지되지 않습니다!")
                
                data = db.select(f"SELECT discord_point, last_update FROM yurinyan_ WHERE discord_userid = {userID}")
                if data is None:
                    return await self.message.reply(f"해당 유저의 데이터가 DB에 존재하지 않습니다! `{self.prefix}유리냥이 포인트 유저추가` 명령어로 먼저 유저를 추가하세요!")
                return await self.message.reply(f"<t:{data['last_update']}> 에 업데이트 됨. \n<@{userID}>의 포인트는 {data['discord_point']}포인트 입니다!")

            elif "유저추가" in self.message.content:
                try:
                    userID = int(self.message.content.split(' ')[3])
                except:
                    return await self.message.reply("유저 아이디가 감지되지 않습니다!")
                
                data = db.select(f"SELECT discord_userid FROM yurinyan_ WHERE discord_userid = {userID}")
                if data is None:
                    member = self.bot.get_user(userID)
                    db.insert(f"INSERT INTO yurinyan_ (discord_userid, discord_username, discord_point, last_update) VALUE ({userID}, '{member.name}', 'NULL', {time.time()})")
                    return await self.message.reply(f"<@{userID}> DB에 추가 완료!")
                else:
                    return await self.message.reply(f"해당 유저(<@{userID}>)는 이미 DB에 존재합니다!")
            elif "지급" in self.message.content:
                try:
                    userID = self.message.content.split(' ')[3]
                except:
                    return await self.message.reply("유저 아이디가 감지되지 않습니다!")
                try:
                    addPoint = int(self.message.content.split(' ')[4])
                except:
                    return await self.message.reply("지급할 포인트가 감지되지 않습니다!")
                
                data = db.select(f"SELECT * FROM yurinyan_ WHERE discord_userid = {userID}")
                if data is None:
                    return await self.message.reply(f"해당 유저의 데이터가 DB에 존재하지 않습니다! `{self.prefix}유리냥이 포인트 유저추가` 명령어로 먼저 유저를 추가하세요!") 
                db.update(f"UPDATE yurinyan_ SET discord_point = {data['discord_point'] + addPoint}, last_update = '{time.time()}' WHERE discord_userid = {data['discord_userid']}")
                return await self.message.reply(f"<@{userID}>에게 {addPoint}포인트 추가해서, 총 {data['discord_point'] + addPoint}포인트 입니다!")
            else:
                return await self.message.reply(f"`{self.prefix}유리냥이 포인트 전체조회`, `{self.prefix}유리냥이 포인트 조회`, `{self.prefix}유리냥이 포인트 유저추가` `{self.prefix}유리냥이 포인트 지급` \n\n형식으로 입력해주세요!")