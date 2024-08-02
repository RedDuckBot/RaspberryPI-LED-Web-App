# Simple LED Web Application 

Locally control three LEDs through a web browser, and get a live video stream 
of any changes made. The setup involves a web server made using the python 
framework Flask, Raspberry PI 3B+, and python OpenCV to operate a USB camera.

<p align="center">
  <img title='LED Web App Clip' src=docs/led_web_app_video.gif width="600">
</p>

## Architecture
<p align="center">
  <img title='LED Web App Architecture' src=docs/software_architecture.png width="800", height="200">
</p>

The above diagram shows how the project's software components were setup, involving three servers, who are started in "main.py", and a program running on the Raspberry PI, called "control_LEDs.py", containing two threads that are responsible for operating the USB camera and LEDs. 

## Running the Application
Before starting the programs, connect the USB camera and LEDs to the Raspberry PI's GPIO pins: 
- Red ---> GPIO22 
- Yellow ---> GPIO27
- Green ---> GPIO17

Install require python packages:
```
pip install -r ./docs/requirements.txt
```
Next, identify the IP address for your machine that you'll be running the servers on. Then, in the files "main.py", "control_LEDs.py", and "server_LED.py", set the global variable "HOST" to this IP. Now the programs can be started.

Start the servers on the computer hosting them:
```
python main.py
```

Then, start "control_LEDs.py" on the Raspberry PI. 

Finally, access a browser from any computer on your local network and enter the
following into the omni box: "[HOST IP address]:9999"

When done with the application, all the running programs can be closed by hitting Ctrl + c.



