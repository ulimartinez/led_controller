#!/bin/bash
sudo killall led_controller
killall game_server.py
sudo /home/ulimartinez/repos/led_controller/build/led_controller > /dev/null &
/home/ulimartinez/repos/led_controller/game_server.py > /dev/null & 
