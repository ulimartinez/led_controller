#!/bin/bash
sudo killall led_controller
killall game_server.py
killall nodejs
sudo /home/ulimartinez/repos/led_controller/build/led_controller > /dev/null 2>&1 &
/home/ulimartinez/repos/led_controller/game_server.py 2>&1 & 
nodejs /home/ulimartinez/repos/led_controller/remote/index.js 2>&1 &
