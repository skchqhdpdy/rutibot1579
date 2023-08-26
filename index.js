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
            {name:"https://collabo.lol/pekemon", value:"마크 1.12.2 포켓몬 서버"},
            {name:"https://collabo.lol/pvp", value:"마크 1.20.1 PVP, 건축 서버"},
            {name:"https://pvp.collabo.lol", value:"하나의 주소로 관리하려고 없앰 (마크 1.20.1 PVP, 건축 서버)"},
        )

        .setTimestamp(new Date())
        .setFooter("Made By aodd.xyz", "https://collabo.lol/img/discord/setFooter.webp")

        message.channel.send(embed);
    }
    if (message.content === `${prefix}서버주소` || message.content === `${prefix}서버 주소` || message.content === `${prefix}마크`) {
        message.reply("``!홈페이지`` 명령어를 사용해주세요!")
        message.channel.send("!홈페이지 (봇이 대신 입력해드렸어요!! XD)")
    }

    if(message.content === `${prefix}github`) {
        const embed = new Discord.MessageEmbed()
        .setAuthor("루티봇#1579", "https://collabo.lol/img/discord/setAuthor.webp")
        .setTitle("명령어")
        .setColor("FF0000")
        
        .setThumbnail("https://collabo.lol/img/discord/setThumbnail.webp")
        
        .addFields(
            {name:"https://github.com/skchqhdpdy", value:"<@399535550832443392>의 github 페이지"},
            {name:"https://github.com/skchqhdpdy/rutibot1579", value:"<@1143492519276060752>의 소스코드"},
        )

        .setTimestamp(new Date())
        .setFooter("Made By aodd.xyz", "https://collabo.lol/img/discord/setFooter.webp")

        message.channel.send(embed);
    }

    if (message.content === `${prefix}트위치` || message.content === `${prefix}twitch`) {
        message.channel.send("<@399535550832443392> 야 너 기능 만들어!")
    }

////////////////////////////////////////////////////////////이스터 애그/////////////////////////////////////////////////////////////

    if (message.content === "비밀") {
        message.reply("꺅 비밀 들켜버렸다")
    }

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