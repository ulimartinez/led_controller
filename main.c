
// Server side C/C++ program to demonstrate Socket programming 
#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 
#include "ws2811.h"
#include "led_wall.h"
#define PORT 8080 



#define ARRAY_SIZE(stuff)       (sizeof(stuff) / sizeof(stuff[0]))

// defaults for cmdline options
#define TARGET_FREQ             WS2811_TARGET_FREQ
#define GPIO_PIN                18
#define DMA                     10
//#define STRIP_TYPE            WS2811_STRIP_RGB		// WS2812/SK6812RGB integrated chip+leds
#define STRIP_TYPE              WS2811_STRIP_GBR		// WS2812/SK6812RGB integrated chip+leds
//#define STRIP_TYPE            SK6812_STRIP_RGBW		// SK6812RGBW (NOT SK6812RGB)

#define WIDTH                   20
#define HEIGHT                  25
#define LED_COUNT               (WIDTH * HEIGHT)

int width = WIDTH;
int height = HEIGHT;
int led_count = LED_COUNT;
int copy_index = 0;
ws2811_led_t *matrix;
ws2811_t ledstring =
{
    .freq = TARGET_FREQ,
    .dmanum = DMA,
    .channel =
    {
        [0] =
{
            .gpionum = GPIO_PIN,
            .count = LED_COUNT,
            .invert = 0,
            .brightness = 255,
            .strip_type = STRIP_TYPE,
        },
        [1] =
        {
            .gpionum = 0,
            .count = 0,
            .invert = 0,
            .brightness = 0,
        },
    },
};

static uint8_t running = 1;

void matrix_render(void)
{

	for(int i =0; i < led_count; i++){
		//to the leds
		ledstring.channel[0].leds[i] = matrix[i];

	}
}

int main(int argc, char const *argv[]) 
{ 
	//setup socket for communication
	int server_fd, new_socket, valread; 
	struct sockaddr_in address; 
	int opt = 1; 
	int addrlen = sizeof(address); 
	char buffer[4096] = {0}; 
	char *hello = "Hello from server"; 
	
	// Creating socket file descriptor 
	if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) 
	{ 
		perror("socket failed"); 
		exit(EXIT_FAILURE); 
	} 
	
	// Forcefully attaching socket to the port 8080 
	if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) 
	{ 
		perror("setsockopt"); 
		exit(EXIT_FAILURE); 
	} 
	address.sin_family = AF_INET; 
	address.sin_addr.s_addr = INADDR_ANY; 
	address.sin_port = htons( PORT ); 
	
	// Forcefully attaching socket to the port 8080 
	if (bind(server_fd, (struct sockaddr *)&address, sizeof(address))<0) 
	{ 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	} 
	if (listen(server_fd, 3) < 0) 
	{ 
		perror("listen"); 
		exit(EXIT_FAILURE); 
	} 
	if ((new_socket = accept(server_fd, (struct sockaddr *)&address, 
					(socklen_t*)&addrlen))<0) { 
		perror("accept"); 
		exit(EXIT_FAILURE); 
	} 
	//setup matrix information
	int running = 1;
	int ret=ws2811_init(&ledstring);
	matrix = malloc(sizeof(ws2811_led_t) * led_count);
	if(ret != WS2811_SUCCESS){
		fprintf(stderr, "ws2811_init failed: %s\n", ws2811_get_return_t_str(ret));
	}
	else{

		while(running){
			valread = read( new_socket , buffer, sizeof(buffer)); 
			if(strstr(buffer, "close") != NULL){
				close(new_socket);
				running = 0;
				break;
			}
			msg_to_matrix(buffer);
			//translate the value read into the matrix
			//render the matrix
			//sleep
		}
	}
	
	return 0; 
} 
void matrix_clear(void)
{
    int x, y;

    for (y = 0; y < (height ); y++)
    {
        for (x = 0; x < width; x++)
        {
            matrix[y * width + x] = 0;
        }
    }
}

void msg_to_matrix(char* message){
	//translating goes here
	printf("message length is %d\n", strlen(message));
	for(int i = 0; i+3 < strlen(message); i+=4){
		matrix[copy_index] = (ws2811_led_t)message[i] << 24 |
					(ws2811_led_t)message[i+1] << 16 |
					(ws2811_led_t)message[i+2] << 8 |
					(ws2811_led_t)message[i+3];
		copy_index++;
		printf("matrix is at %d capacity\n", copy_index);
		if(copy_index == led_count-1){
			copy_index = 0;
			matrix_render();
		}
	}
}

