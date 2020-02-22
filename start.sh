#!/bin/bash
sudo killall led_controller
killall MasterController.py
killall  nodejs
killall game_server.py
sudo /home/ulimartinez/repos/led_controller/build/led_controller > /dev/null 2>&1 &
/home/ulimartinez/repos/led_controller/MasterController.py > /dev/null 2>&1 &
