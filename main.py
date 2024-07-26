from flask import Flask, render_template, request, Response
import multiprocessing
from server_LED import serverLED, server_video

"""
   Program starts three servers: web server (Flask application) who updates the LED queue 
   with the web clients latest changes for the states of the three LEDs; LED server 
   responsible for sending latest changes to Raspberry PI, and a video server
   for live viewing of any changes. Both LED and video servers are ran as separate
   processes and share the LED and frame queues with main.  
"""

HOST = "Enter your computer's IP"

app = Flask(__name__) #Flask web application

queueLEDs = multiprocessing.Queue() #shared data of LED states between main and LED server
queueFrames = multiprocessing.Queue() #Shared video frames between main and video server
stateR = "OFF" #state of red button
stateG = "OFF" #state of green button
stateY = "OFF" #state of yellow button

@app.route("/", methods=["GET","POST"])
def change_led():
    """Route for main page which toggles states of leds:
       red, green and yellow"""
    global stateR, stateG, stateY

    if request.method == "POST":
        if "redBtn" in request.form:
            print("Flip red led!")
            stateR = toggle(request.form["redBtn"])
        elif "greenBtn" in request.form:
            print("Flip green led!")
            stateG = toggle(request.form["greenBtn"])
        else: # yellow
            print("Flip yellow led!")
            stateY = toggle(request.form["yellowBtn"])
        queueLEDs.put(prepData([stateR,stateG,stateY]))
        print(queueLEDs.qsize())
        return render_template("ledPage.html", stateR=stateR, stateG=stateG,
                               stateY=stateY)
    return render_template("ledPage.html", stateR=stateR, stateG=stateG,
                           stateY=stateY)
                           
@app.route("/video_feed")
def video_feed():
    """Route for live video streaming the states of LEDs"""

    return Response(get_video_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def get_video_frames():
    """Extract frames from video frames queue and yield them as a byte stream for
    HTTP response streaming"""

    while True:
        frame = queueFrames.get()
        frame_bytes = frame.tobytes()

        # Yield the output frame in byte format
        yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def toggle(state):
    """Function toggles button text from on to off and vice versa"""
    if (state == "OFF"): return "ON"
    else: return "OFF"

def prepData(ledStates):
    """Raspberry pi code uses Boolean values for check states as opposed
       to using text, as done in the web client. So, this function performs
       this conversion."""

    modStates = []
    for state in ledStates:
        tempState = False if state == "OFF" else True
        modStates.append(tempState)
    return modStates

if __name__ == "__main__":
    queueLEDs.put([stateR,stateG,stateY]) #Initial states

    #Initialize video and led servers as separate processes
    led_Process = multiprocessing.Process(target=serverLED, args=(queueLEDs,))
    video_process = multiprocessing.Process(target=server_video, args=(queueFrames,))

    led_Process.start() #start LED server 
    video_process.start() #start video server
    app.run(host=HOST, port=9999) #start web server 
