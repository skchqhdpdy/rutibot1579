const Discord = require('discord.js');
const { json } = require('express');
const client = new Discord.Client({
    partials: ['MESSAGE', 'REACTION'], // 이 부분을 추가하여 메시지와 반응 데이터를 캐시합니다.
});
const { prefix, token } = require("./config.json");
//rainbow color
//보류
/* const {
    serverID, 
    roleID, 
    interval 
} = require('./config.json') */
const fs = require('fs');
const { log } = require('console');

client.setMaxListeners(0)

client.on('ready', () => {
    console.log('루티봇#1579 온라인!');
	client.user.setActivity('!명령어', { type: 'LISTENING' })

    //rainbow color
    //보류
    /* let guild = client.guilds.cache.get(serverID) 
    if(!guild) throw `[ Error ] Server Peida Nashod: ${serverID}` 

    let role = guild.roles.cache.find(u => u.id === roleID) 
    if(!role) throw `[ Error ] Role Peida Nashod, Server Name: ${guild.name}` 
    
    if(interval < 60000) console.log(`\nRainbow Color | [!!!] Khatarnake Havaset bashe`) 

    setInterval(() => {
        role.edit({color: 'RANDOM'}).catch(err => console.log(`[ Error ] An error occurred during the role change.`));
    }, interval) */
});

//유저 디코입장
client.on('guildMemberAdd', (member) => {
    try {
        const channel = member.guild.channels.cache.find((ch) => ch.id === '1149986137377620029');
        if (!channel) return;
    
        // Embed 메시지를 생성하여 프로필 사진을 포함시킵니다.
        const embed = new Discord.MessageEmbed()
            .setAuthor("루티봇#1579", "https://collabo.lol/img/setAuthor.webp")
            .setTitle(`안녕하세요, \`${member.user.tag}\` 님! 서버에 가입하신 것을 환영합니다!`)
            .setColor("#F280EB")
            .setThumbnail(member.user.displayAvatarURL()) // 프로필 사진을 Embed에 추가
            .setTimestamp(new Date())
            .setFooter("Made By aodd.xyz", "https://collabo.lol/img/setFooter.webp")
    
        channel.send(`<@${member.user.id}>`, embed);
    } catch (error) {
        console.log(`guildMemberAdd 예외처리 됨 | error = ${error}`)
    }

});
//유저 디코 퇴장
client.on('guildMemberRemove', (member) => {
    try {
        const channel = member.guild.channels.cache.find((ch) => ch.id === '1149986137377620029');
        if (!channel) return;
    
        // Embed 메시지를 생성하여 프로필 사진을 포함시킵니다.
        const embed = new Discord.MessageEmbed()
            .setAuthor("루티봇#1579", "https://collabo.lol/img/setAuthor.webp")
            .setTitle(`안녕히 가세요, \`${member.user.tag}\` 님! 서버에서 나가셨습니다.`)
            .setColor("#FF5733")
            .setThumbnail(member.user.displayAvatarURL()) // 프로필 사진을 Embed에 추가
            .setTimestamp(new Date())
            .setFooter("Made By aodd.xyz", "https://collabo.lol/img/setFooter.webp")
    
        channel.send(`<@${member.user.id}>`, embed);
    } catch (error) {
        console.log(`guildMemberRemove 예외처리 됨 | error = ${error}`)
    }
});


//zira봇 역할
const CHANNEL_ID = '1107570796555149353'; // 이벤트를 감지할 채널 ID
const MESSAGE_ID = '1145201143023157298'; // 이벤트를 감지할 메시지 ID
const EMOJI_NAME = "minecraft"; // 반응에 사용할 이모지 이름
const ROLE_ID = '1145215725645074442'; // 부여할 역할 ID

function sendLogDiscord(channelId, content) {
    try {
        // 지정된 채널을 찾아서 메시지를 보냅니다.
        const targetChannel = client.channels.cache.get(channelId);
        if (targetChannel) {
            targetChannel.send(content);
        } else {
            console.log(`<#${channelId}> 해당 채널을 찾을 수 없음`)
        }
    } catch (error) {
        console.log(`sendLogDiscord() 함수 예외처리 됨 | error = ${error}`)
    }
}

client.on('messageReactionAdd', async (reaction, user) => {
    try {
        // 반응한 메시지가 지정한 채널에 있는지 확인합니다.
        if (reaction.message.channel.id !== CHANNEL_ID) return;
        
        // 반응한 메시지가 지정한 메시지인지 확인합니다.
        if (reaction.message.id === MESSAGE_ID && reaction.emoji.name === EMOJI_NAME) {
            const member = reaction.message.guild.members.cache.get(user.id);
            const role = reaction.message.guild.roles.cache.get(ROLE_ID);
            if (member && role) {
                await member.roles.add(role);
                msg = `[${user.tag}]에게 [${role.name}] 역할을 추가했습니다.`
                console.log(msg);
                sendLogDiscord("1152894841236246558", msg)
            }
        }
    } catch (error) {
        console.log(`messageReactionAdd 함수 예외처리 됨 | error = ${error}`)
    }
    
});
client.on('messageReactionRemove', async (reaction, user) => {
    try {
        // 반응한 메시지가 지정한 채널에 있는지 확인합니다.
        if (reaction.message.channel.id !== CHANNEL_ID) return;
    
        // 반응한 메시지가 지정한 메시지인지 확인합니다.
        if (reaction.message.id === MESSAGE_ID && reaction.emoji.name === EMOJI_NAME) {
            const member = reaction.message.guild.members.cache.get(user.id);
            const role = reaction.message.guild.roles.cache.get(ROLE_ID);
            if (member && role) {
                await member.roles.remove(role);
                msg = `[${user.tag}]에게 [${role.name}] 역할을 제거했습니다.`
                console.log(msg);
                sendLogDiscord("1152894841236246558", msg)
            }
        }
    } catch (error) {
        console.log(`messageReactionRemove 함수 예외처리 됨 | error = ${error}`)
    }
    
});

//메인
try {
    client.on('message', (message) => {
        if(message.content === `${prefix}명령어`) {
    
            const embed = new Discord.MessageEmbed()
            .setAuthor("루티봇#1579", "https://collabo.lol/img/setAuthor.webp")
            .setTitle("명령어")
            .setColor("FF0000")
            
            .setThumbnail("https://collabo.lol/img/setThumbnail.webp")
            
            .addFields(
                {name:"!명령어", value:"명령어를 보여줍니다."},
                {name:"!봇 초대", value:"봇 초대 주소입니다."},
                {name:"!ping", value:"봇의 서버핑을 보여줍니다. (음악봇 !ping이랑 중복됨)"},
                {name:"!투표", value:"O 또는 X 로 투표를 할수있습니다. \n사용법:!투표 투표할 내용"},
                {name:"!홈페이지", value:"운영중인 홈페이지 주소를 보여줍니다."},
                {name:"!github", value:"깃허브 페이지"},
                {name:"!clear {지울 만큼의 숫자}", value:"!clear 명렁어를 `포함한` 개수의 메세지 삭제"},
                {name:"!help (h)", value:"!help (h) 음악봇 관련 명령어 입니다."},
                {name:"!마니또 추첨", value:"마니또를 추첨하는 명령어 입니다. (합방 시작전에 관리자들 끼리 합의 하에 추첨을 하고 그걸 고정해서 사용할 예정)"},
            )
    
            .setTimestamp(new Date())
            .setFooter("Made By aodd.xyz", "https://collabo.lol/img/setFooter.webp")
    
            message.channel.send(embed);
    
        }
    
        if(message.content.substring(0,3) === `${prefix}투표`) {
            
            const 투표내용 /*(변수)*/ = message.content.substring(3);
    
            const embed = new Discord.MessageEmbed()
            .setAuthor("루티봇#1579", "https://collabo.lol/img/setAuthor.webp")
            .setTitle("👇 투표내용  (Voting contents)")
            .setDescription(투표내용)
            .setColor("FF0000")
    
            .setThumbnail("https://collabo.lol/img/setThumbnail.webp")
    
            message.reply(embed)
            .then((msg) => {
                msg.react("⭕")
                msg.react("❌")
            });
        }
    
        if(message.content === `${prefix}홈페이지` || message.content.startsWith(`${prefix}홈페이지`)) {
    
            const embed = new Discord.MessageEmbed()
            .setAuthor("루티봇#1579", "https://collabo.lol/img/setAuthor.webp")
            .setTitle("명령어")
            .setColor("FF0000")
            
            .setThumbnail("https://collabo.lol/img/setThumbnail.webp")
            
            .addFields(
                {name:"https://collabo.lol/pokemon", value:"마크 1.12.2 포켓몬 서버 홈페이지"},
                {name:"https://collabo.lol/pvp", value:"마크 1.20.1 PVP, 건축 서버 홈페이지"},
            )
    
            .setTimestamp(new Date())
            .setFooter("Made By aodd.xyz", "https://collabo.lol/img/setFooter.webp")
    
            message.channel.send(embed);
        }
        if (message.content === `${prefix}서버주소` || message.content === `${prefix}서버 주소` || message.content === `${prefix}마크`) {
            message.reply("``!홈페이지`` 명령어를 사용해주세요!")
            message.channel.send("!홈페이지 (봇이 대신 입력해드렸어요!! XD)")
        }
    
        if(message.content === `${prefix}github` || message.content === `${prefix}깃허브`) {
            const embed = new Discord.MessageEmbed()
            .setAuthor("루티봇#1579", "https://collabo.lol/img/setAuthor.webp")
            .setTitle("명령어")
            .setColor("FF0000")
            
            .setThumbnail("https://collabo.lol/img/setThumbnail.webp")
            
            .addFields(
                {name:"https://github.com/skchqhdpdy", value:"<@399535550832443392>의 github 페이지"},
                {name:"https://github.com/skchqhdpdy/rutibot1579", value:"<@1143492519276060752>의 소스코드"},
                {name:"https://github.com/skchqhdpdy/2024-Twitch-Streamer-Collabo", value:"web 페이지 소스코드?"},
            )
    
            .setTimestamp(new Date())
            .setFooter("Made By aodd.xyz", "https://collabo.lol/img/setFooter.webp")
    
            message.channel.send(embed);
        }
    
        if (message.content === `${prefix}트위치` || message.content === `${prefix}twitch`) {
            message.channel.send("<@399535550832443392> 야 너 기능 만들어!")
        }
    
        if (message.content.startsWith(`${prefix}clear`)) {
            if (!message.member.hasPermission("MANAGE_MESSAGES")) { //만약에 명령어를 입력한 사람 권한 중 MANAGE_MESSAGES 라는 권한이 없다면
                return message.reply("권한이 없습니다."); //전송
            }
            let purge = message.content.substring(6) * 1
                if (!purge || purge == "") { //만약 메세지가 비어있거나 안써져있다면
                    return message.reply("숫자를 입력해주세요,") //전송
                }
                if (purge > 100) { //만약 purge의 값이 100보다 크다면
                    return message.reply("1부터 100까지만 입력하세요.") //전송
                }
                if (purge < 1) { //만약 purge의 값이 1보다 작다면
                    return message.reply("1부터 100까지만 입력하세요.") //전송
                }
                if (isNaN(purge) == true) { //isNaN은 정수인지 판단하는 함수입니다. 문자열이 포함되어있을 경우 true를 반환합니다.
                    return message.reply("숫자만 입력하세요.") //전송
                } else { //아니라면
                    message.channel.bulkDelete(purge) //purge 변수 만큼 채널에세 메세지를 삭제합니다. //전송
                    .then(() => message.reply(`${purge}개의 메세지를 삭제했습니다. 이 메세지는 5초후 삭제 됩니다.`))
                    .catch(console.error)
    
                    setTimeout(() => {
                        message.channel.bulkDelete(1)
                    }, 5000);
                    
                }
        }

        //마니또 추첨
        if (message.content === `${prefix}마니또 추첨`) {
            const guildId = '1107568623050047550'; // 스트리머 역할을 찾을 서버(길드)의 ID를 입력하세요.
            const roleToFind = '스트리머'; // 찾을 역할의 이름을 입력하세요.
            
            // 서버(길드) 객체를 가져옵니다.
            const guild = client.guilds.cache.get(guildId);
            // 역할을 찾습니다.
            const role = guild.roles.cache.find((r) => r.name === roleToFind);
    
            if (!role) {
                console.error('역할을 찾을 수 없습니다.');
                return;
            }
    
            // 스트리머 역할을 가진 멤버 목록을 추출합니다.
            const streamerMembers = guild.members.cache.filter((member) => member.roles.cache.has(role.id));
    
            // 마니또 참가자 목록
            // 끼음, 복미, 오소희, 솜팡, 남야 님은 반확정이라서 넣어줘용
            // 저랑 쥐님이랑 공허님(hyp로시작하는분)빼고
            const participants = []; // 필요한 참가자 수만큼 추가하세요.
            const exceptUser = []
    
            // 스트리머 역할을 가진 멤버의 ID와 이름을 출력합니다.
            streamerMembers.forEach((member) => {
                //console.log(`유저 ID: ${member.user.id}, 유저 이름: ${member.user.tag}`);
                // @스트리머 역할중 3명 제외
                if (member.user.id !== "657145673296117760" && member.user.id !== "472607419474640897" && member.user.id !== "448274272104873984") {
                    participants.push(member.user.id)
                } else {
                    exceptUser.push(member.user.id)
                }
            });
            
            // 총 4명의 유저는 예외로 서로서로 마니또
            // 제외유저 추가
            let eachManito = []
            const participantsLength = participants.length
            for (let i = 0; i < 4;) {
                let r = Math.floor(Math.random() * participantsLength)
                
                if (eachManito.indexOf(participants[r]) === -1) {
                    eachManito.push(participants[r])
                    i++
                }
            }
            // 기존 유저에서 제외 유저 제거
            for (let i = 0; i < 4; i++) {
                const partIndex = participants.indexOf(eachManito[i])
                if (partIndex !== -1) {
                    participants.splice(partIndex, 1)
                }
            }
            
            // 참가자를 무작위로 섞기
            for (let i = participants.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [participants[i], participants[j]] = [participants[j], participants[i]];
            }
            
            let resultMember = []
            
            // 마니또 매칭
            for (let i = 0; i < participants.length; i++) {
                const giver = participants[i];
                const receiver = participants[(i + 1) % participants.length]; // 순환하도록 설정
                resultMember.push([giver, receiver])
            }
    
            let descript = `
                ----------------------------------------
                1번째 | <@${eachManito[0]}> --> <@${eachManito[1]}>
                2번째 | <@${eachManito[1]}> --> <@${eachManito[0]}>
                3번째 | <@${eachManito[2]}> --> <@${eachManito[3]}>
                4번째 | <@${eachManito[3]}> --> <@${eachManito[2]}>
                ----------------------------------------
            `
            let desNum = 5
            for (const i of resultMember) {
                descript += `${desNum}번째 | <@${i[0]}> --> <@${i[1]}> \n`
                desNum++
            }
            descript += `
                ----------------------------------------
                예외처리 (참가 안함)
            `
            for (const i of exceptUser) {
                descript += `<@${i}>\n`
                desNum++
            }
            descript += "----------------------------------------"
    
    
            // Embed 메시지를 생성하여 프로필 사진을 포함시킵니다.
            const embed = new Discord.MessageEmbed()
                .setAuthor("루티봇#1579", "https://collabo.lol/img/setAuthor.webp")
                .setTitle("마티또 추첨!")
                .setDescription(descript)
                .setColor("#F280EB")
                .setThumbnail("https://collabo.lol/img/마니또.jpg") // 프로필 사진을 Embed에 추가
                .setTimestamp(new Date())
                .setFooter("Made By aodd.xyz", "https://collabo.lol/img/setFooter.webp")
        
            message.channel.send(embed);
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
    
} catch (error) {
    console.log(`main 전체 예외처리 됨 | error = ${error}`)
}

client.login(token);