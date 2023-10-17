#디코 채널 로그
def send_log_discord(bot, channel_id, content):
    try:
        target_channel = bot.get_channel(channel_id)
        if target_channel:
            target_channel.send(content)
        else:
            print(f"<#{channel_id}> 해당 채널을 찾을 수 없음")
    except Exception as error:
        print(f'send_log_discord() 함수 예외처리 됨 | error = {error}')

# 계란 꺠기 게임
