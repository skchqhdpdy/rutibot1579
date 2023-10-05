from flask import Flask, session, redirect, request, render_template
from requests_oauthlib import OAuth2Session
from common.config import Config
import requests
import lets_common_log.logUtils as log
from time import localtime, strftime

HOST = Config["host"]
PORT = Config["port"]
DEBUG = bool(Config["debug"])
CLIENT_ID = Config["ClientID"]
CLIENT_SECRET = Config["ClientSecret"]
REDIRECT_URI = Config["RedirectURL"]
API_BASE_URL = "https://discordapp.com/api"
AUTHORIZATION_BASE_URL = f"{API_BASE_URL}/oauth2/authorize"
TOKEN_URL = f"{API_BASE_URL}/oauth2/token"

app = Flask('DiscordOauth2Invite')
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = CLIENT_SECRET

def request_msg(request):
    # Logging the request IP address
    print("")
    try:
        real_ip = request.headers.get("Cf-Connecting-Ip")
        request_uri = request.headers.get("X-Forwarded-Proto") + "://" + request.host + request.full_path
        country_code = request.headers.get("Cf-Ipcountry")
    except Exception as e:
        log.warning("cloudflare를 거치지 않아서 country_code 조회가 안됨, real_ip는 nginx header에서 가져옴")
        try:
            real_ip = request.headers.get("X-Real-Ip")
            request_uri = request.headers.get("X-Forwarded-Proto") + "://" + request.host + request.full_path
            country_code = "XX"
        except Exception as e:
            log.warning("http로 접속시도함 | cloudflare를 거치지 않아서 country_code 조회가 안됨, real_ip는 http 요청이라서 바로 뜸")
            real_ip = request.remote_addr
            request_uri = request.scheme + "://" + request.host + request.full_path
            country_code = "XX"
    client_ip = request.remote_addr
    try:
        User_Agent = request.headers.get("User-Agent")
    except Exception as e:
        log.error("User-Agent 값이 존재하지 않음!")
        User_Agent = ""
    msg = f"Request from IP: {real_ip}, {client_ip} ({country_code}) | URL: {request_uri} | From: {User_Agent}"
    log.info(msg)

    # .txt로 IP 로그 남기기
    # 파일을 추가 모드로 열고 데이터 추가하기
    with open('log.txt', 'a') as file:
        file.write(f'[{strftime("%Y-%m-%d %H:%M:%S", localtime())}] - {msg}\n\n')



def token_updater(token):
    session['oauth2_token'] = token

def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)

@app.route("/")
def index():
    request_msg(request)
    scope = request.args.get(
        'scope',
        'identify guilds.join')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    request_msg(request)
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    url = request.url.replace("http://", "https://")
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=CLIENT_SECRET,
        authorization_response=url)
    session['oauth2_token'] = token
    userID = discord.get(f"{API_BASE_URL}/users/@me").json()["id"]
    res = requests.put(f"{API_BASE_URL}/guilds/{Config['ServerID']}/members/{userID}",
        headers = {
            "Authorization": f"Bot {Config['BotToken']}",
            "Content-Type": "application/json"
        },
        json = {
            'access_token': f"{session['oauth2_token']['access_token']}"
        })
    if res.status_code == 201 or res.status_code == 204:
        return render_template("redirect.html", server_id=Config["ServerID"])

if __name__ == '__main__':
    app.run(port=PORT, host=HOST, debug=DEBUG)