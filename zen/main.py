import time
import machine

led = machine.Pin(2, machine.Pin.OUT)

while True:
  led.value(True)
  time.sleep(2.0)
  led.value(False)
  time.sleep(5.0)
