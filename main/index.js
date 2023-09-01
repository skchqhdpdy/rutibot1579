const Discord = require('discord.js');
const { json } = require('express');
const client = new Discord.Client();
const { prefix, token } = require("./config.json");

client.setMaxListeners(0)

client.on('ready', () => {
    console.log('루티봇#1579 온라인!');
	client.user.setActivity('!명령어', { type: 'LISTENING' })
});

client.on('message', (message) => {
    if(message.content === `${prefix}명령어`) {

        const embed = new Discord.MessageEmbed()
        .setAuthor("루티봇#1579", "https://collabo.lol/img/discord/setAuthor.webp")
        .setTitle("명령어")
        .setColor("FF0000")
        
        .setThumbnail("https://collabo.lol/img/discord/setThumbnail.webp")
        
        .addFields(
            {name:"!명령어", value:"명령어를 보여줍니다."},
            {name:"!봇 초대", value:"봇 초대 주소입니다."},
            {name:"!ping", value:"봇의 서버핑을 보여줍니다."},
            {name:"!투표", value:"O 또는 X 로 투표를 할수있습니다. \n사용법:!투표 투표할 내용"},
            {name:"!홈페이지", value:"운영중인 홈페이지 주소를 보여줍니다."},
            {name:"!github", value:"깃허브 페이지"},
        )

        .setTimestamp(new Date())
        .setFooter("Made By aodd.xyz", "https://collabo.lol/img/discord/setFooter.webp")

        message.channel.send(embed);

    }

    if(message.content.substring(0,3) === `${prefix}투표`) {
        
        const 투표내용 /*(변수)*/ = message.content.substring(3);

        const embed = new Discord.MessageEmbed()
        .setAuthor("루티봇#1579", "https://collabo.lol/img/discord/setAuthor.webp")
        .setTitle("👇 투표내용  (Voting contents)")
        .setDescription(투표내용)
        .setColor("FF0000")

        .setThumbnail("https://collabo.lol/img/discord/setThumbnail.webp")

        message.reply(embed)
        .then((msg) => {
            msg.react("⭕")
            msg.react("❌")
        });
    }

    if(message.content === `${prefix}홈페이지` || message.content.startsWith(`${prefix}홈페이지`)) {

        const embed = new Discord.MessageEmbed()
        .setAuthor("루티봇#1579", "https://collabo.lol/img/discord/setAuthor.webp")
        .setTitle("명령어")
        .setColor("FF0000")
        
        .setThumbnail("https://collabo.lol/img/discord/setThumbnail.webp")
        
        .addFields(
            {name:"https://collabo.lol/pokemon", value:"마크 1.12.2 포켓몬 서버 홈페이지"},
            {name:"https://collabo.lol/pvp", value:"마크 1.20.1 PVP, 건축 서버 홈페이지"},
        )

        .setTimestamp(new Date())
        .setFooter("Made By aodd.xyz", "https://collabo.lol/img/discord/setFooter.webp")

        message.channel.send(embed);
    }
    if (message.content === `${prefix}서버주소` || message.content === `${prefix}서버 주소` || message.content === `${prefix}마크`) {
        message.reply("``!홈페이지`` 명령어를 사용해주세요!")
        message.channel.send("!홈페이지 (봇이 대신 입력해드렸어요!! XD)")
    }

    if(message.content === `${prefix}github` || message.content === `${prefix}깃허브`) {
        const embed = new Discord.MessageEmbed()
        .setAuthor("루티봇#1579", "https://collabo.lol/img/discord/setAuthor.webp")
        .setTitle("명령어")
        .setColor("FF0000")
        
        .setThumbnail("https://collabo.lol/img/discord/setThumbnail.webp")
        
        .addFields(
            {name:"https://github.com/skchqhdpdy", value:"<@399535550832443392>의 github 페이지"},
            {name:"https://github.com/skchqhdpdy/rutibot1579", value:"<@1143492519276060752>의 소스코드"},
            {name:"https://github.com/skchqhdpdy/2024-Twitch-Streamer-Collabo", value:"web 페이지 소스코드?"},
        )

        .setTimestamp(new Date())
        .setFooter("Made By aodd.xyz", "https://collabo.lol/img/discord/setFooter.webp")

        message.channel.send(embed);
    }

    if (message.content === `${prefix}트위치` || message.content === `${prefix}twitch`) {
        message.channel.send("<@399535550832443392> 야 너 기능 만들어!")
    }

////////////////////////////////////////////////////////////이스터 애그/////////////////////////////////////////////////////////////

    //config.json에서 설정 추가해서 활성화 명령어 입력시 활성화 시키게 만들기
    if (message.content === "비밀") {
        message.reply("꺅 비밀 들켜버렸다")
    }
    if (message.content === "몇명의 찬란한 연지인형" & message.channel.id === "1146725666348339323") {
        message.reply("님 이 시크릿 코드 어떻게 아셨나요? 때려맞추신건 아니겠죠? 어쨌든간에 정답입니다!!(?)")
    }
    //console.log(`${message.channel} | ${message.author}  ${message.content} | ${message.attachments} | ${message.system}`)

/////////////////////////////////////////////////////////////따로뺴둠//////////////////////////////////////////////////////////////

    if(message.content === `${prefix}봇 초대` || message.content === `${prefix}봇 초대`) {
        message.reply('https://discord.com/api/oauth2/authorize?client_id=1143492519276060752&permissions=8&scope=bot')
    }

    if(message.content === `${prefix}ping` || message.content === `${prefix}핑`) {
        const timeTake = Date.now() - message.createdTimestamp;
        message.reply(`서버핑은 **${timeTake}ms** 입니다.`);
        console.log(`서버핑은 **${timeTake}ms** 입니다.`);
    }
});

client.login(token);