const Discord = require('discord.js');
const { json } = require('express');
const client = new Discord.Client({
    partials: ['MESSAGE', 'REACTION'], // 이 부분을 추가하여 메시지와 반응 데이터를 캐시합니다.
});
const { prefix, token } = require("./config.json");

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}`);
    const guild = client.guilds.cache.get("1107568623050047550"); //1107568623050047550 (스트리머 서버)

    // 스트리머 역할을 가진 멤버 목록을 추출합니다.
    const streamerRole = guild.roles.cache.find((r) => r.name === "스트리머");
    const streamerMembers = guild.members.cache.filter((member) => member.roles.cache.has(streamerRole.id));
    const streamers = []
    streamerMembers.forEach((member) => {
        streamers.push(member.user.id)
    });

    
    setInterval(() => {
        for (const userID of streamers) {
            // 역할 목록을 배열로 저장할 변수를 선언합니다.
            const rolesArray = [];
        
            // 서버의 모든 역할을 반복하여 원하는 조건을 충족하는 역할을 찾습니다.
            guild.roles.cache.forEach((role) => {
                // 역할 이름이 'color'로 시작하는 역할을 찾습니다.
                if (role.name.startsWith('color')) {
                    rolesArray.push(role.name); // 조건을 충족하는 역할을 배열에 추가합니다.
                }
            });

            console.debug(userID)
            console.debug(rolesArray)
            
            const baseMember = guild.members.cache.get("657145673296117760");//1143492519276060752 (루티봇 ID), 657145673296117760 (유리냥이 ID)
            const member = guild.members.cache.get(userID)
            
            let role = ""
            let nextRole = ""
            let arrNum = ""
            
            //루티봇#1579의 역할을 기준으로 다음 역할 검색
            for (const i of rolesArray) {
                arrNum = rolesArray.indexOf(i)
                role = baseMember.roles.cache.find((r) => r.name === i)
                if ((arrNum < rolesArray.length - 1) && role) {
                    guild.roles.cache.forEach((role) => {
                        if (role.name === rolesArray[arrNum + 1]) {
                            nextRole = role
                        }
                    });
                    break
                } else {
                    guild.roles.cache.forEach((role) => {
                        if (role.name === rolesArray[0]) {
                            nextRole = role
                        }
                    });
                }
            }

            console.debug(nextRole.name)

            // 다음 역할 부여
            member.roles.add(nextRole)
            .then(() => {
            })
            .catch((error) => {
                console.error(`다음 역할 추가 에러! : ${error}`);
            });
            
            try {
                // 기존 역할 제거
                member.roles.remove(role)
                .then(() => {
                })
                .catch((error) => {
                    console.error(`기존 역할 제거 에러! : ${error}`);
                });
            } catch (error) {
                console.error(`color 역할 자체가 없어서 첫 한번만 역할제거 안함 : ${error}`);
            }
            
        }
    }, 5000);
});

client.login(token);
