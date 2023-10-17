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
const { channel } = require('diagnostics_channel');
const { clearTimeout } = require('timers');

try {
    client.setMaxListeners(0)
} catch (error) {
    console.error(`client.setMaxListeners(0) 예외처리 됨 | error = ${error}`)
}


try {
    client.on('message', (message) => {
        //계란 깨기 게임
        function exitEggGame(message, msg) {
            clearTimeout(timeoutID_eggGame)
            console.log(msg)
            message.channel.send(msg);
            message.channel.send("게임 오버! \n----------------------------------------------------------------------------------------------------")
            isGameActive_eggGame = false;
            brokeEggNumber_eggGame = []
            players_eggGame = {}
            channelID_eggGame = ""
            timeoutID_eggGame = ""
            return
        }
        function timerEggGame(message) {
            const r = setTimeout(() => {
                const msg = "5분간 이용하지 않아 계란깨기 게임이 중지됬습니다."
                exitEggGame(message, msg)
            }, 300000);
            return r
        }

        if (message.content === (`${prefix}계란깨기시작`) && !isGameActive_eggGame) {
            // 게임 시작
            isGameActive_eggGame = true;
            channelID_eggGame = message.channel.id
            timeoutID_eggGame = timerEggGame(message)

            console.log("")
            for (let i = 0; i < 5;) {
                let r = Math.floor(Math.random() * 100) + 1
                if (brokeEggNumber_eggGame.indexOf() === -1) {
                    brokeEggNumber_eggGame.push(r) // 1에서 100 사이의 랜덤 숫자
                    console.log(`날 계란 ${i + 1}의 번호: ${brokeEggNumber_eggGame[i]}`);
                    i++
                }
            }

            message.channel.send(`계란깨기 게임을 시작합니다!`);
        } else if (message.content === (`${prefix}계란깨기시작`) && isGameActive_eggGame) { // 더블 실행 방지
            message.reply(`<#${channelID_eggGame}> 채널에서 게임이 진행중 입니다!`);
        } else if (message.content === (`${prefix}계란깨기중지`) && isGameActive_eggGame) { //게임 중지 코드
            const msg = `<@${message.author.id}>님이 게임을 종료하였습니다.`
            exitEggGame(message, msg)
        } else if (message.content.startsWith(`${prefix}계란깨기`)) { // 게임 진행 코드
            if (!isGameActive_eggGame) {
                message.reply("`!계란깨기시작` 명령어로 게임을 먼저 시작하세요!")
            } else {
                // 게임 진행 중
                const userNumber = parseInt(message.content.split(' ')[1]);
    
                if (isNaN(userNumber) || userNumber < 1 || userNumber > 100) {
                    message.reply('1에서 100 사이의 숫자를 입력하세요!');
                    return;
                }
    
                if (players_eggGame[userNumber]) {
                    message.reply(`${userNumber}는 <@${players_eggGame[userNumber]}>님이 입력했던 숫자입니다. 다른 숫자를 입력하세요!`);
                    return;
                }
    
                if (brokeEggNumber_eggGame.includes(userNumber)) {
                    // 날 계란을 깼을 경우
                    const msg = `<@${message.author.id}>님이 날 계란 ${brokeEggNumber_eggGame} 중 (${userNumber}번 계란)을 깼습니다.`
                    exitEggGame(message, msg)
                } else {
                    // 삶은 계란일 경우
                    players_eggGame[userNumber] = message.author.id;
                    const remainingEggs = 100 - Object.keys(players_eggGame).length;
                    message.reply(`${userNumber}는 삶은 계란입니다. 남은 계란의 수는 ${remainingEggs}개 입니다.`);
                }
            }
        
        } else if (message.channel.id === channelID_eggGame && message.content.startsWith(prefix)) { //타임아웃 갱신
            clearTimeout(timeoutID_eggGame)
            timeoutID_eggGame = timerEggGame(message)
        }


    
    ////////////////////////////////////////////////////////////이스터 애그/////////////////////////////////////////////////////////////
    
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
    console.error(`main 전체 예외처리 됨 | error = ${error}`)
}

client.login(token);