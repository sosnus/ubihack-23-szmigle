import time
import network
import uasyncio
import urequests as requests
from machine import Timer, Pin, PWM

ssid = "network"
password = "pass"
url = "http://example.com"

wlan = None

def init():
    wlan = network.WLAN(network.STA_IF)
    connect_to_wifi(wlan, ssid, password)
    
def send(sun_val, red_val, light_ref_val, light_control_val):
    payload = [
        {
            "variable": "sun_emulator",
            "value": sun_val
        },
        {
            "variable": "bulb_emulator",
            "value": red_val
        },
        {
            "variable": "sensor_reference",
            "value": light_ref_val
        },
        {
            "variable": "sensor_control",
            "value": light_control_val
        }
    ]
    headers = {
        "Content-Type": "application/json",
        "device-token": "xxxxx"
    }
    r = requests.request("POST", url, json=payload, headers=headers)

    print(r.text)
    r.close()
      
def connect_to_wifi(wlan = None, ssid = "", password = ""):
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep_ms(1000)
    print("WiFi "+ ssid + " connected!")
    
init()

adc0 = machine.ADC(0)
adc1 = machine.ADC(1)
adc2 = machine.ADC(2)
sun = PWM(Pin(2))
red = PWM(Pin(3))

def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def read():
    light_ref = adc0.read_u16()
    light_control = adc1.read_u16()
    knob_adc = adc2.read_u16()
            
    knob = min(100, round(knob_adc/65535.0*1000 , 2))
    
    sun_val = int(convert(knob, 3, 100, 0, 65534))
    red_val = int(convert(light_ref, 20000, 65534, 65534, 0))
    light_ref_val = int(convert(light_ref, 0, 65534,  0, 100))
    light_control_val = int(convert(light_control, 0, 65534,  0, 100))

    
    print("knob              =", knob)
    print("light_ref_val     =", light_ref_val)
    print("light_control_val =", light_control_val)
    print("sun_val           =", sun_val)
    print("red_val           =", red_val)
    
    sun.duty_u16(sun_val)
    red.duty_u16(red_val)
    return (sun_val, red_val, light_ref_val, light_control_val)

if __name__ == "__main__":
    prev_read = time.ticks_ms()
    prev_send = time.ticks_ms()
    
    while True:
        timestamp = time.ticks_ms()

        if timestamp - prev_read > 10:
            prev_read = timestamp
            sun_val, red_val, light_ref_val, light_control_val = read()
        elif timestamp - prev_send > 10_000:
            prev_send = timestamp
            send(sun_val, red_val, light_ref_val, light_control_val)
