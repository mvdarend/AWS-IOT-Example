from gpiozero import LED
from gpiozero import MotionSensor
from datetime import datetime

global message
import requests
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

myMQTTClient = AWSIoTMQTTClient("ClientID")
myMQTTClient.configureEndpoint("xxxxxxxxx.iot.yourregion.amazonaws.com", 8883)

myMQTTClient.configureCredentials("/home/pi/pi-projects/root-CA.pem", "/home/pi/pi-projects/LED-private.pem.key", "/home/pi/pi-projects/LED.pem.crt")
 
print ('Initiating Realtime Data Transfer From Raspberry Pi...')

Myvar= myMQTTClient.connect()

date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
print (f"Timestamp:{date}")

red_led = LED(17)
pir = MotionSensor (4)
red_led.off()

while True:
    pir.wait_for_motion()
    print("Motion Detected")
    message= "Motion Detected"
    myMQTTClient.publish("topic/pi", "{\"MotionMessage\":\""+ message + "\", \"Timestamp\" :\""+ str(date)+ "\"}", 0)
    red_led.on()
    pir.wait_for_no_motion()
    red_led.off()
    print ("No Motion")
    message= "No Motion"
    myMQTTClient.publish("topic/pi", "{\"MotionMessage\":\""+ message + "\", \"Timestamp\" :\""+ str(date)+ "\"}", 0)
    time.sleep(1)