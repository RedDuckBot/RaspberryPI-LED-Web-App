from socket import * 
from gpiozero import LED
import pickle

"""
    Program runs on Raspberry PI to control three LED lights by waiting on changes in states from LED server.
"""

server_LED = ""
server_LED_port = 6666
pi_socket = socket(AF_INET, SOCK_STREAM)
pi_socket.connect((server_LED,server_LED_port))

red_led = LED(22)
red_led.off()
yellow_led = LED(27)
yellow_led.off()
green_led = LED(17)
green_led.off()

print("Connection with LED server established. Ready to receive changes.") 


while True: 
    led_states_list = pickle.loads(pi_socket.recv(1024))

    if led_states_list[0] == True: #Red LED
        red_led.on() 
    else:
        red_led.off()

    if led_states_list[1] == True: #Green LED
        green_led.on()
    else:
        green_led.off()

    if led_states_list[2] == True: #Yellow LED
        yellow_led.on()
    else:
        yellow_led.off()
        
