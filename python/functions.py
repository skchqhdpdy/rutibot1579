import json
import pymysql

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

        if len(result) == 1:
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
def send_log_discord(bot, channel_id, content):
    try:
        target_channel = bot.get_channel(channel_id)
        if target_channel:
            target_channel.send(content)
        else:
            log.error(f"<#{channel_id}> 해당 채널을 찾을 수 없음")
    except Exception as error:
        log.error(f'send_log_discord() 함수 예외처리 됨 | error = {error}')

# 계란 꺠기 게임
