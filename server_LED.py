from socket import *
import pickle

"""
    Script contains a function serverLED that establishes a TCP connection with a
    Raspberry PI and sends the most recent changes, the LED states, from the shared 
    queue between main and LED server. 
""" 

server_LED_Port = 6666
server_LED_ip = ""

def serverLED(qled):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((server_LED_ip,server_LED_Port))
    serverSocket.listen(1)
    print("LED Server ready for Raspberry PI and web server communication")

    rasp_conn, rasp_addr = serverSocket.accept()
    print(f"Raspberry PI IP: {rasp_addr}")

    while True:
        led_states = qled.get() #queue of led states
        rasp_conn.send(pickle.dumps(led_states))
