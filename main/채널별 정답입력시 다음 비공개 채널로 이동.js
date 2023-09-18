const Discord = require('discord.js');
const { json } = require('express');
const client = new Discord.Client({
    partials: ['MESSAGE', 'REACTION'], // 이 부분을 추가하여 메시지와 반응 데이터를 캐시합니다.
});
const { prefix, token } = require("./config.json");



const channelId = '1107572367242305577'; // 확인할 비공개 채널의 ID를 입력하세요.
const userId = '399535550832443392'; // 확인할 유저의 ID를 입력하세요.

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}`);
});


client.on('message', (message) => {
    if (message.content.startsWith("대충 퀴즈 정답임") && message.channel.id === "1153259983228633099") {
        //a0, a1, a2 ... a9 형식임
        const user = message.author
        const chanName = message.channel.name
        const chanNameNext = chanName[0] + ((chanName[1] * 1) + 1)

        const newChannel = message.guild.channels.cache.find(ch => ch.name === chanNameNext);
        if (!newChannel) {
            message.reply(`채널 "${chanNameNext}"을 찾을 수 없습니다.`);
            return;
        }

        try {
            // 채널에 유저 추가
            newChannel.updateOverwrite(user, {
                VIEW_CHANNEL: true,
                SEND_MESSAGES: true,
                READ_MESSAGE_HISTORY: true,
            });
        } catch (error) {
            console.error('권한 부여 실패:', error);
            message.reply(`권한 부여 실패! | chanName = ${chanName}, chanNameNext = ${chanNameNext}, user = ${user}`)
        }

        message.channel.bulkDelete(1)
        .then(() => message.reply(`님 축하합니다! 정답입니다! 다음 채널이 열렸습니다! 이 메세지는 10초후 삭제 됩니다.`))
        .catch(console.error)

        setTimeout(() => {
            message.channel.bulkDelete(1)
        }, 10000);
    }
});

client.login(token);
