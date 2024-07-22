from flask import Flask, render_template, request
import multiprocessing
from server_LED import serverLED

"""
   Program starts two servers: web server (Flask application) who updates the LED queue 
   with the web clients latest changes for the states of the three LEDs; LED server 
   responsible for sending latest changes to Raspberry PI, which is a separate
   process that shares the LED queue with main.
"""

app = Flask(__name__) #Flask web application

queueLEDs = multiprocessing.Queue() #shared data between main and LED server
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
    raspProcess = multiprocessing.Process(target=serverLED, args=(queueLEDs,))

    raspProcess.start() #start LED server 
    app.run(host="", port=9999) #start web server 
