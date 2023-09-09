const Discord = require('discord.js');
const { json } = require('express');
const client = new Discord.Client();
const { prefix, token } = require("./config.json");
const fs = require('fs');
const { log } = require('console');

client.setMaxListeners(0)

client.on('ready', () => {
    console.log('루티봇#1579 온라인!');
	client.user.setActivity('!명령어', { type: 'LISTENING' })
});

//유저 디코입장
client.on('guildMemberAdd', (member) => {
    const channel = member.guild.channels.cache.find((ch) => ch.id === '1149986137377620029');
    if (!channel) return;

    // Embed 메시지를 생성하여 프로필 사진을 포함시킵니다.
    const embed = new Discord.MessageEmbed()
        .setAuthor("루티봇#1579", "https://collabo.lol/img/discord/setAuthor.webp")
        .setTitle(`안녕하세요, \`${member.user.tag}\` 님! 서버에 가입하신 것을 환영합니다!`)
        .setColor("#F280EB")
        .setThumbnail(member.user.displayAvatarURL()) // 프로필 사진을 Embed에 추가
        .setTimestamp(new Date())
        .setFooter("Made By aodd.xyz", "https://collabo.lol/img/discord/setFooter.webp")

    channel.send(`<@${member.user.id}>`, embed);
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
    let { SecretCode } = require("./secretcode.json");

    /* if (message.content === `${prefix}secretcode`) {
        let { secretcode_status } = require("./secretcode.json");
        message.channel.send(secretcode_status)
        changeSecretCodeStatus("./secretcode.json")
    } */

    if (message.content === "비밀") {
        message.reply("꺅 비밀 들켜버렸다")
    }
    if (message.content === SecretCode[0] & message.channel.id === "1146725666348339323") {
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

//secretcode.json 상태 변경 코드
/* function changeSecretCodeStatus(filePath, status) {
    // JSON 파일 읽기
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('파일을 읽을 수 없습니다.', err);
            return;
        }
        // JSON 데이터 파싱
        const jsonData = JSON.parse(data);
        // jsonData를 수정하거나 변경합니다.
        jsonData.secretcode_status = status;
        // 수정된 JSON 데이터를 파일에 씁니다.
        fs.writeFile(filePath, JSON.stringify(jsonData, null, 2), 'utf8', (err) => {
            if (err) {
                console.error('파일을 쓸 수 없습니다.', err);
                return;
            }
            console.log('파일이 성공적으로 수정되었습니다.');
        });
    });
} */

function changeSecretCodeStatus(filePath) {
    // JSON 파일 읽기
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            console.error('파일을 읽을 수 없습니다.', err);
            return;
        }

        // JSON 데이터 파싱
        let jsonData = JSON.parse(data);

        // JSON 데이터를 수정하여 스위치처럼 true 또는 false 값을 변경합니다.
        jsonData = {
            ...jsonData,
            secretcode_status: !jsonData.secretcode_status, // 스위치 값을 반전시킵니다.
        };

        // 수정된 데이터를 다시 JSON 문자열로 변환합니다.
        const updatedData = JSON.stringify(jsonData, null, 2);

        // 수정된 JSON 데이터를 파일에 씁니다.
        fs.writeFile(filePath, updatedData, 'utf8', (err) => {
        if (err) {
            console.error('파일을 쓸 수 없습니다.', err);
            return;
        }
        console.log('파일이 성공적으로 수정되었습니다.');
        });
    });

}

client.login(token);