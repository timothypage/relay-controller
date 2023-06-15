import time
from contextlib import contextmanager

try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO

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

relays = [
    {"pin": 2,  "relay": 0, "state": "off"},
    {"pin": 3,  "relay": 1, "state": "off"},
    {"pin": 4,  "relay": 2, "state": "off"},
    {"pin": 17, "relay": 3, "state": "off"},
    {"pin": 27, "relay": 4, "state": "off"},
    {"pin": 22, "relay": 5, "state": "off"},
    {"pin": 9,  "relay": 6, "state": "off"},
    {"pin": 10, "relay": 7, "state": "off"},
]

@app.get("/api/relays")
def get_relays():
    return {"meta": { "count": 8 }, "data": relays}

@app.put("/api/relays/{relay_id}")
def toggle_relay(relay_id, state):
    relay_id = int(relay_id)
    if relay_id > len(relays):
        return {"error": "invalid relay id", "status_url": "https://http.cat/status/400"}

    relay = relays[relay_id]

    if state == "off":
        GPIO.output(relay["pin"], GPIO.HIGH)
        relay["state"] = "off"
    
    elif state == "on":
        GPIO.output(relay["pin"], GPIO.LOW)
        relay["state"] = "on"

    elif state == "toggle":
        if relay["state"] == "off":
            GPIO.output(relay["pin"], GPIO.HIGH)
            relay["state"] = "on"
        elif relay["state"] == "on":
            GPIO.output(relay["pin"], GPIO.LOW)
            relay["state"] = "off"

    else:
        return {"error": f"invalid state, valid states are \"on\", \"off\", \"toggle\". You sent {state}"}

    return {"message": f"relay id {relay_id} turned {relay['state']}"}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
