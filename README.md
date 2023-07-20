##### Game launch:
- git clone https://github.com/eldoranstars/invadersinvasion.git
- cd InvadersInvasion
- pip install -r requirements.txt
- python game.py

##### Game structure:
- основной цикл игры game.py;
- все игровые ф-ции вынесены в game_functions.py;
- все параметры вынесены в settings.py;
- все настройки состояния вынесены в stats.py;
- все остальные модули это шаблоны изображений.

##### xbox one control
- Left Stick -- movement
- Right Trigger -- shoot
- Start Button -- pause
- Left Bumper -- fullscreen while pause
- Right Bumper -- music while pause
- Back Button -- quit while pause

##### keyboard control
- arrows -- movement
- space -- shoot
- q -- pause
- f -- fullscreen while pause
- m -- music while pause
- esc -- quit while pause

##### Compile
pyinstaller -F --add-data "media/*:media/" --icon=favicon.ico game.py # linux
pyinstaller -F --add-data "media\*;media\" --icon=favicon.ico game.py # windows