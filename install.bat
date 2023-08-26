@echo off

:main
cls
echo ┍───────────────────────────────
echo │
echo │     Nodejs가 컴퓨터에 설치되어 있나요? (y/n)
echo │     나가기 = exit
echo │ 
echo ┕───────────────────────────────


set/p isnodejsinstall=y 또는 n을 적은 후 Enter : 
if %isnodejsinstall%==y goto nodejsinstalled
if %isnodejsinstall%==n goto nodejsnotinstalled
if %isnodejsinstall%==exit exit


:nodejsinstalled
cls
npm i
goto e

:nodejsnotinstalled
cls
start https://collabo.lol/img/discord/루티봇%%20install.bat%%20문구.png
start https://offbyone.tistory.com/441
start https://nodejs.org/ko
goto main

:e
cls
echo ┍───────────────────────────────
echo │
echo │     Nodejs 설치 다 하셨으면, start.bat 파일로 봇을 실행하면 됩니다!
echo │ 
echo ┕───────────────────────────────

pause
exit