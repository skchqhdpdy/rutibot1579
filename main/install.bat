@echo off

:main
cls
echo �Ȧ�������������������������������������������������������������
echo ��
echo ��     Nodejs�� ��ǻ�Ϳ� ��ġ�Ǿ� �ֳ���? (y/n)
echo ��     ������ = exit
echo �� 
echo �Ʀ�������������������������������������������������������������


set/p isnodejsinstall=y �Ǵ� n�� ���� �� Enter : 
if %isnodejsinstall%==y goto nodejsinstalled
if %isnodejsinstall%==n goto nodejsnotinstalled
if %isnodejsinstall%==exit exit


:nodejsinstalled
cls
npm i
goto e

:nodejsnotinstalled
cls
start https://collabo.lol/img/discord/��Ƽ��%%20install.bat%%20����.png
start https://offbyone.tistory.com/441
start https://nodejs.org/ko
goto main

:e
cls
echo �Ȧ�������������������������������������������������������������
echo ��
echo ��     Nodejs ��ġ �� �ϼ�����, start.bat ���Ϸ� ���� �����ϸ� �˴ϴ�!
echo �� 
echo �Ʀ�������������������������������������������������������������

pause
exit