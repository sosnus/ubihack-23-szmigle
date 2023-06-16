import time
import network
# import uasyncio
import urequests as requests
from machine import Timer, Pin, PWM

ssid = "CyberwirusII"
password = "KrowaNaGranicy856)"
url = "http://srv18.mikr.us:40083/data"

wlan = None

def init():
    wlan = network.WLAN(network.STA_IF)
    connect_to_wifi(wlan, ssid, password)
    
    # sun_val, bulb_val, knob_sun, knob_bulb):
def send():
    payload = [
        {
            "variable": "knobsun256",
            "value": knobsun256
        },
        {
            "variable": "knobcfg256",
            "value":knobcfg256
        },
        {
            "variable": "sensor256",
            "value": sensor256
        },
        {
            "variable": "ledSun256",
            "value": ledSun256
        },
        {
            "variable": "ledBulb256",
            "value": ledBulb256
        }
    ]
    headers = {
        "Content-Type": "application/json",
        "device-token": "426ea0fb-6277-4541-ad9a-32c4eeb7a291"
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
led = PWM(Pin(2))
sun = PWM(Pin(12))

knobsun256 = 0
knobcfg256 = 0
sensor256 = 0
ledSun256 = 0
ledBulb256 = 0



def readAndSet(ledBulb256,ledSun256, sensor256, knobsun256, knobcfg256):
    # global ledBulb256
    sensor256 = adc0.read_u16() / 256
    knobsun256 = adc1.read_u16() / 256
    knobcfg256 = adc2.read_u16() / 256

    
    sun.duty_u16(int(knobsun256*256))
    if(knobcfg256 < sensor256):
        ledBulb256 = ledBulb256 + 1
    else:
        ledBulb256 = ledBulb256 - 1
    
    # sun.duty_u16(knobsun256*256)
    led.duty_u16(int(ledBulb256*256))
    # return (sun_val, red_val, light_ref_val, light_control_val)
    return (ledBulb256, ledSun256,sensor256, knobsun256, knobcfg256)

if __name__ == "__main__":
    prev_read = time.ticks_ms()
    prev_send = time.ticks_ms()
    
    while True:
        timestamp = time.ticks_ms()

        if timestamp - prev_read > 10:
            prev_read = timestamp
            ledBulb256, ledSun256, sensor256, knobsun256, knobcfg256 = readAndSet(ledBulb256, ledSun256, sensor256, knobsun256, knobcfg256)
            #sun_val, red_val, light_ref_val, light_control_val = read()
        elif timestamp - prev_send > 100:
            prev_send = timestamp
            send()
            # send(sun_val, red_val, light_ref_val, light_control_val)
            print("knobsun256 = ", knobcfg256)
            print("knobcfg256 = ", knobcfg256)
            print("sensor256  = ", sensor256)
            print("ledSun256  = ", ledSun256)
            print("ledBulb256 = ", ledBulb256)



