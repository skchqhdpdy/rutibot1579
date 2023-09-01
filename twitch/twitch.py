import socket
import threading
import discord

# Twitch IRC 서버 정보
TWITCH_SERVER = "irc.chat.twitch.tv"
TWITCH_PORT = 6667
TWITCH_CHANNEL = "#"
TWITCH_TOKEN = ""

# Discord 봇 관련 정보
DISCORD_TOKEN = ""
DISCORD_CHANNEL_ID = ""

# Twitch IRC 연결을 관리하는 클래스
class TwitchChatBot:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect((TWITCH_SERVER, TWITCH_PORT))
        self.socket.send(f"PASS {TWITCH_TOKEN}\n".encode("utf-8"))
        self.socket.send(f"NICK justinfan12345\n".encode("utf-8"))
        self.socket.send(f"JOIN {TWITCH_CHANNEL}\n".encode("utf-8"))
        
    def receive_messages(self):
        while True:
            message = self.socket.recv(2048).decode("utf-8")
            if message.startswith("PING"):
                self.socket.send("PONG\n".encode("utf-8"))
            elif "PRIVMSG" in message:
                username = message.split("!")[0][1:]
                content = message.split("PRIVMSG")[1].split(":")[1:]
                content = ":".join(content).strip()
                print(f"Twitch Chat - {username}: {content}")
                discord_channel = self.discord_bot.get_channel(DISCORD_CHANNEL_ID)
                self.discord_bot.loop.create_task(discord_channel.send(f"Twitch Chat - {username}: {content}"))

# Discord 봇 초기화
discord_bot = discord.Client()

# Discord 봇이 준비되었을 때 실행되는 이벤트 핸들러
@discord_bot.event
async def on_ready():
    print(f"We have logged in as {discord_bot.user}")
    twitch_bot = TwitchChatBot()
    twitch_bot.discord_bot = discord_bot
    threading.Thread(target=twitch_bot.receive_messages).start()

# Discord 봇 실행
discord_bot.run(DISCORD_TOKEN)
