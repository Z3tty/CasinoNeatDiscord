@title Casino Neat Diceroller ~ Setup
@echo off
cls
set /p token=Please enter your bot token:
echo Setting up directories ...
mkdir enc
mkdir DB
mkdir rpgdata
echo Done!
echo Creating token file ...
cd enc
@echo %token%>token.cncrypt
cd ..
echo Done!
echo Setting up DB ...
cd DB
type NUL > database.json
cd ..
echo Done!
echo Now just use the run file and enjoy the bot!
pause
