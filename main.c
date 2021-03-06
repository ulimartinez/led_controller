
// Server side C/C++ program to demonstrate Socket programming 
#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 
#include <sys/time.h>
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
	int server_fd, new_socket, valread, client_socket[30],
		max_clients = 30, activity, i, sd, addrlen; 
	int max_sd;
	struct sockaddr_in address; 
	int opt = 1; 
	char buffer[4096] = {0}; 
	fd_set readfds;

	for(i=o; i< max_clients; i++){
		client_socket[i] = 0;
	}
	
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

	addrlen = sizeof(address);
	//setup matrix information
	int running = 1;
	int ret=ws2811_init(&ledstring);
	matrix = malloc(sizeof(ws2811_led_t) * led_count);
	if(ret != WS2811_SUCCESS){
		fprintf(stderr, "ws2811_init failed: %s\n", ws2811_get_return_t_str(ret));
	}
	else{

		while(running){
			FD_ZERO(&readfds);
			FD_SET(server_fd, &readfds);
			imax_sd = server_fd;
			for(i=0; i<max_clients; i++){
				sd = client_socket[i];
				if(sd>0)
					FD_SET(sd, &readfds);
				if(sd > max_sd)
					max_sd = sd;
			}
			activity = select(max_sd+1, &readfds, NULL, NULL, NULL);

			if((activity < 0) && (errno!=EINTR)){
				printf("select errror");
			}

			if(FD_ISSET(server_fd, &readfds)){
					if((new_socket = accept(server_fd,
									(struct sockaddr *)&address,
									socklen_t*)&addrlen))<0){
						perror("accept");
						exit(EXIT_FAILURE);
					}

					for(i=0; i<max_clients; i++){
						if(client_socket[i] == 0){
							client_socket[i] = new_socket;
							break;
						}
					}
			}	
			for(i=0; i < max_clients; i++){
				sd = client_socket[i];
				if(FD_ISSET(sd, &readfds)){
					if((valread=read(sd, buffer, sizeof(buffer)))==0){
						//got dissconect
						close(sd);
						client_socket[i] = 0;
					} else{

						if(strstr(buffer, "close") != NULL){
							close(sd);
							client_socket[i] = 0;
						}
						msg_to_matrix(buffer, valread);
					}
				}
			}
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

void msg_to_matrix(char* message, int valread){
	uint32_t *p=(uint32_t*)message;
	size_t len = valread / sizeof(uint32_t);
	printf("got %d ints", len);
	for(int i = 0; i < len; i++){
		matrix[copy_index] = p[i];
		if(copy_index == led_count-1){
			copy_index=-1;
			matrix_render();
			ws2811_render(&ledstring);
			matrix_clear();
		}
		copy_index++;
		printf("matrix is at %d capacity\n", copy_index);
	}
}

