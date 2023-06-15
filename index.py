import time
from contextlib import contextmanager

import RPi.GPIO as GPIO

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

pin_list = [2, 3, 4, 17, 27, 22, 9, 10]
GPIO.setmode(GPIO.BCM)

@contextmanager
def lifespan(app):
    GPIO.cleanup()


for i in pin_list:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

# app = FastAPI(lifespan=lifespan)
app = FastAPI();


@app.get("/api/relays")
def relays():
    return {"meta": { "count": 8 }, "data": [
        {"pin": 2,  "relay": 0, "state": "off"},
        {"pin": 3,  "relay": 1, "state": "off"},
        {"pin": 4,  "relay": 2, "state": "off"},
        {"pin": 17, "relay": 3, "state": "off"},
        {"pin": 27, "relay": 4, "state": "off"},
        {"pin": 22, "relay": 5, "state": "off"},
        {"pin": 9,  "relay": 6, "state": "off"},
        {"pin": 10, "relay": 7, "state": "off"},
    ]}

@app.put("/api/relays/{relay_id}")
def toggle_relay(relay_id, state):
    relay_id = int(relay_id)
    if relay_id > len(pin_list):
        return {"error": "invalid relay id", "status_url": "https://http.cat/status/400"}

    if state == "off":
        GPIO.output(pin_list[relay_id], GPIO.HIGH)
    
    elif state == "on":
        GPIO.output(pin_list[relay_id], GPIO.LOW)

    else:
        return {"error": f"invalud state, valid states are \"on\", \"off\". You sent {state}"}

    return {"message": f"relay id {relay_id} turned {state}"}


app.mount("/", StaticFiles(directory="static", html=True), name="static")

# counter = 2

# for i in pin_list:
#    GPIO.output(i, GPIO.LOW)
#    print(f"relay index: {counter}")
#    print(f"GPIO pin: {i}")
#    counter += 1
#    time.sleep(1)

    
