// tw.js

/* const tmi = require('tmi.js');
const { Client, GatewayIntentBits } = require('discord.js');

module.exports = {
  initTwitchBot: function(TWITCH_TOKEN, TWITCH_CHANNEL) {
    const twitchClient = new tmi.Client({
      options: { debug: true },
      connection: { reconnect: true },
      identity: { username: 'your_bot_username', password: TWITCH_TOKEN },
      channels: [TWITCH_CHANNEL],
    });

    twitchClient.connect();

    return twitchClient;
  },

  initDiscordBot: function(DISCORD_TOKEN) {
    const discordClient = new Client({
      intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
      ],
    });

    discordClient.once('ready', () => {
      console.log(`Twitch | Logged in as ${discordClient.user.tag}`);
    });

    discordClient.login(DISCORD_TOKEN);

    return discordClient;
  }
} */

// tw.js

const tmi = require('tmi.js');
const { Client, Intents } = require('discord.js');

module.exports = {
  initTwitchBot: function(TWITCH_TOKEN, TWITCH_CHANNEL) {
    const twitchClient = new tmi.Client({
      options: { debug: true },
      connection: { reconnect: true },
      identity: { username: 'your_bot_username', password: TWITCH_TOKEN },
      channels: [TWITCH_CHANNEL],
    });

    twitchClient.connect();

    return twitchClient;
  },

  initDiscordBot: function(DISCORD_TOKEN) {
    const discordClient = new Client({
      intents: [
        Intents.FLAGS.GUILDS,
        Intents.FLAGS.GUILD_MESSAGES,
      ],
    });

    discordClient.once('ready', () => {
      console.log(`Logged in as ${discordClient.user.tag}`);
    });

    discordClient.login(DISCORD_TOKEN);

    return discordClient;
  }
}
