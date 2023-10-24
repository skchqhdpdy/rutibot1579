const tmi = require('tmi.js');
const mysql = require('mysql');
const { Client, GatewayIntentBits } = require('discord.js');
const { db } = require("./config.json");

let DISCORD_TOKEN = ""
let TWITCH_TOKEN = ""
let TWITCH_CHANNEL = ""
let DISCORD_CHANNEL_ID = ""

// MySQL 서버에 연결
const connection = mysql.createConnection({
    host: db["host"],
    user: db["username"],
    password: db["password"],
    database: db["database"]
});

connection.connect((err) => {});

// 데이터베이스 쿼리 실행 예제
connection.query("SELECT token, Twitch_token FROM rutibot_setting", (err, rows) => {
    DISCORD_TOKEN = rows[0]["token"]
    TWITCH_TOKEN = rows[0]["Twitch_token"]
});

connection.query("SELECT twitch_id, Discord_channel_ID FROM rutibot_twitch WHERE twitch_id = 'mongjel'", (err, rows) => {
    TWITCH_CHANNEL = rows[0]["twitch_id"]
    DISCORD_CHANNEL_ID = rows[0]["Discord_channel_ID"]
});

connection.end((err) => {});

setTimeout(() => {
    // Twitch 봇 초기화
    const twitchClient = new tmi.Client({
        options: { debug: true },
        connection: { reconnect: true },
        identity: { username: 'rutibot1579', password: TWITCH_TOKEN },
        channels: [TWITCH_CHANNEL],
    });

    twitchClient.connect();

    // Discord 봇 초기화
    const discordClient = new Client({
        intents: [
            GatewayIntentBits.Guilds,
            GatewayIntentBits.GuildMessages,
    ],
    });

    discordClient.once('ready', () => {
        console.log(`Logged in as ${discordClient.user.tag}`);
    });

    discordClient.login(DISCORD_TOKEN);

    // Twitch 채팅을 Discord로 전송
    twitchClient.on('message', (channel, user, message) => {
        if (channel === `#${TWITCH_CHANNEL}`) {
            const discordChannel = discordClient.channels.cache.get(DISCORD_CHANNEL_ID);
            if (discordChannel) {
            discordChannel.send(`Twitch Chat - ${user.username}: ${message}`);
            }
        }
    });
}, 1000);




