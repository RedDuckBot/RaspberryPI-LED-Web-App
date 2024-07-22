from socket import * 
from gpiozero import LED
import pickle, threading, cv2

"""
    Program runs two threads on Raspberry PI: main controls three LED lights 
    by waiting on changes in states sent by LED server, and a video daemon
    that sends the latest frames to the video server.
"""

server_LED_ip = ""
server_LED_port = 6666
server_video_port = 6669

def main():

    main_socket = socket(AF_INET, SOCK_STREAM)
    main_socket.connect((server_LED_ip,server_LED_port))

    red_led = LED(22)
    red_led.off()
    yellow_led = LED(27)
    yellow_led.off()
    green_led = LED(17)
    green_led.off()

    print("[main] Connection with LED server established. Ready to receive changes.") 

    while True: 
        led_states_list = pickle.loads(main_socket.recv(1024))

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

def generate_frames():

    #Setup UDP socket
    client_video_UDP_socket = socket(AF_INET, SOCK_DGRAM)
    client_video_UDP_socket.setsockopt(SOL_SOCKET, SO_SNDBUF, 1000000)
   
    print("[video_thread] Ready for live video stream")

    #Setup camera
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    while cap.isOpened():
        ret, img = cap.read()
        ret, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

        serial_buffer = pickle.dumps(buffer)

        client_video_UDP_socket.sendto((serial_buffer),(server_LED_ip,server_video_port))

        if cv2.waitKey(5) & 0xFF == 113:
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    video_thread = threading.Thread(target=generate_frames, args=(),daemon=True)
    video_thread.start()
    main()
