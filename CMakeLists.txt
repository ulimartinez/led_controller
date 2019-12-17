cmake_minimum_required(VERSION 3.7)
# set the project name
project(led_controller)

include_directories("${PROJECT_SOURCE_DIR}/src")
# add the executable
add_executable(led_controller main.c pwm.c rpihw.c ws2811.c mailbox.c dma.c pcm.c pwm.c)

