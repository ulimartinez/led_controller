#!/bin/bash
sudo killall led_controller
killall nodejs
killall cheer_server.py
killall game_server.py
killall MasterController.py
sudo /home/ulimartinez/repos/led_controller/build/led_controller > /dev/null 2>&1 &
/home/ulimartinez/repos/led_controller/game_server.py 2>&1 & 
nodejs /home/ulimartinez/repos/led_controller/remote/index.js
