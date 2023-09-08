const tmi = require('tmi.js');
const { Client, GatewayIntentBits } = require('discord.js');
const { token, Twitch_token, Twitch_channels } = require("./config.json");

// Twitch 봇 및 Discord 봇 토큰
const TWITCH_TOKEN = Twitch_token;
const DISCORD_TOKEN = token;

// Twitch 채널 및 Discord 채널 ID
const TWITCH_CHANNEL = Twitch_channels[4]["twitch_id"];
const DISCORD_CHANNEL_ID = Twitch_channels[4]["Discord_channel_ID"];

// Twitch 봇 초기화
const twitchClient = new tmi.Client({
  options: { debug: true },
  connection: { reconnect: true },
  identity: { username: 'your_bot_username', password: TWITCH_TOKEN },
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
