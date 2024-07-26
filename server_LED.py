from socket import *
import pickle

"""
    Script contains two function: serverLED establishes a TCP connection with a
    Raspberry PI and sends the most recent changes, the LED states, from the shared 
    LED queue between main and LED server; server_video creates an UDP connection
     for live video streaming of any changes, and updates the queue frames also
     shared with main. 
""" 

server_LED_Port = 6666
HOST = ""
server_video_port = 6669

def serverLED(qled):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((HOST,server_LED_Port))
    serverSocket.listen(1)
    print("[LED_process] LED Server ready for Raspberry PI and web server communication")

    rasp_conn, rasp_addr = serverSocket.accept()
    print(f"Raspberry PI IP: {rasp_addr}")

    while True:
        led_states = qled.get() #queue of led states
        rasp_conn.send(pickle.dumps(led_states))

def server_video(qframes):
    server_video_socket = socket(AF_INET,SOCK_DGRAM)
    server_video_socket.bind((HOST,server_video_port))

    print("[video_process] Video Server ready.")
    while True:
        payload = server_video_socket.recvfrom(1000000)
        data = payload[0]
        data = pickle.loads(data)
        qframes.put(data)
