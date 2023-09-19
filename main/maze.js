const Discord = require('discord.js');
const { json } = require('express');
const client = new Discord.Client({
    partials: ['MESSAGE', 'REACTION'], // 이 부분을 추가하여 메시지와 반응 데이터를 캐시합니다.
});
const { prefix, token } = require("./config.json");

// 미로 게임 객체를 저장할 맵
const mazeGames = new Map();

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}`);
});

client.on('message', (message) => {
  if (message.content === '!startmaze') {
    // 미로 게임 초기화
    const gameId = message.author.id;
    const maze = initializeMaze(); // 미로 초기화 함수
    mazeGames.set(gameId, { maze, position: { x: 0, y: 0 } });
    message.channel.send('미로 게임을 시작합니다. w, a, s, d로 이동하세요.');
    printMaze(message.channel, gameId);
  } else if (message.content.match(/^[wasd]$/i)) {
    // 사용자 입력 처리
    const gameId = message.author.id;
    if (mazeGames.has(gameId)) {
      const { maze, position } = mazeGames.get(gameId);
      const move = message.content.toLowerCase();
      const newPosition = movePlayer(position, move, maze);
      if (newPosition) {
        mazeGames.set(gameId, { maze, position: newPosition });
        printMaze(message.channel, gameId);
        if (isGameComplete(newPosition, maze)) {
          message.channel.send('미로 게임 클리어!');
          mazeGames.delete(gameId);
        }
      }
    } else {
      message.channel.send('미로 게임을 시작하세요: !startmaze');
    }
  }
});

function initializeMaze() {
  // 미로 초기화 로직을 구현하세요.
  // 여기에서 미로를 생성하고 반환합니다.
  // 미로는 배열 또는 문자열 형태로 표현될 수 있습니다.
  // 예: [['S', ' ', 'X'], ['X', ' ', 'X'], ['X', 'E', ' ']]
}

function printMaze(channel, gameId) {
  // 미로를 채팅에 출력하는 로직을 구현하세요.
  // channel.send()를 사용하여 미로를 출력합니다.
}

function movePlayer(position, move, maze) {
  // 플레이어 이동 로직을 구현하세요.
  // 플레이어의 새 위치를 반환하거나, 이동이 불가능한 경우 null을 반환합니다.
}

function isGameComplete(position, maze) {
  // 게임 클리어 조건을 구현하세요.
  // 플레이어가 목표 지점에 도달하면 true를 반환합니다.
}

client.login(token);