const Discord = require('discord.js');
const { json } = require('express');
const client = new Discord.Client({
    partials: ['MESSAGE', 'REACTION'], // 이 부분을 추가하여 메시지와 반응 데이터를 캐시합니다.
});
const { prefix, token } = require("./config.json");

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}`);
});

/* const clientId = 'obiycajiit10w2n3xasoi0mhyrnwu7';
const clientSecret = "oh5008yzo3qoac70fw0i7ao4hoj2xq"
const accessToken = 'ywz338c6b264xsm6uhtlf3wms6rnp6';
const streamerUsername = 'skchqhdpdy2'; */

client.on('message', (message) => {
  if (message.content === '!twitchfollow') {
    const axios = require('axios');

    // Twitch API 키
    const CLIENT_ID = 'obiycajiit10w2n3xasoi0mhyrnwu7';
    const CLIENT_SECRET = 'oh5008yzo3qoac70fw0i7ao4hoj2xq';

    // 스트리머의 Twitch 사용자명
    const streamerUsername = 'skchqhdpdy2';

    // OAuth2 토큰을 얻기 위한 함수
    async function getOAuthToken() {
      try {
        const response = await axios.post('https://id.twitch.tv/oauth2/token', null, {
          params: {
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            grant_type: 'client_credentials',
          },
        });

        return response.data.access_token;
      } catch (error) {
        console.error('OAuth2 토큰을 얻을 수 없습니다.', error);
      }
    }

    // 스트리머의 정보를 얻기 위한 함수
    async function getStreamerInfo(token) {
      try {
        const response = await axios.get(`https://api.twitch.tv/helix/users?login=${streamerUsername}`, {
          headers: {
            'Client-ID': CLIENT_ID,
            'Authorization': `Bearer ${token}`,
          },
        });

        const userId = response.data.data[0].id;

        // 스트리머의 정보를 얻은 후, 팔로우 수를 얻기 위한 함수 호출
        getFollowerCount(token, userId);
      } catch (error) {
        console.error('스트리머 정보를 얻을 수 없습니다.', error);
      }
    }

    // 스트리머의 팔로우 수를 얻기 위한 함수
    async function getFollowerCount(token, userId) {
      try {
        const response = await axios.get(`https://api.twitch.tv/helix/users/follows?to_id=${userId}`, {
          headers: {
            'Client-ID': CLIENT_ID,
            'Authorization': `Bearer ${token}`,
          },
        });

        const followerCount = response.data.total;
        console.log(`${streamerUsername}의 팔로우 수: ${followerCount}`);
      } catch (error) {
        console.error('스트리머의 팔로우 수를 얻을 수 없습니다.', error);
      }
    }

    // 메인 함수
    async function main() {
      const token = await getOAuthToken();
      if (token) {
        getStreamerInfo(token);
      }
    }

    main();

  }
});
//9ctmx5yx30now1wnid8vu4nqj2s4m8
client.login(token);