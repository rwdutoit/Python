#!/usr/bin/python
import paho.mqtt.publish as mqtt
import Adafruit_BBIO.ADC as ADC
import smbus
import time

class A(object):
    def __init__(self):
        self.MyBus = smbus.SMBus(1)

    def readPortExpander(self):
        try:
            #self.MyBus.write_byte_data(0x6b,0x05,0xfe)
            ReadData = self.MyBus.read_byte_data(0x23,0x00)
            return ReadData
        except:
            return -1

    def readTemp(self):
        try:
            value = ADC.read("P9_40") #ADC.read("AIN1")
            voltage = value * 1.8 * 10 #1.8V
            return voltage #random.randint(80,100)
        except:
            return -1

def main():
    a = A()
    mqtt.single("mqtt/message", "start", hostname="192.168.0.108")
    ADC.setup()
    counter = 0
    while True:
        counter+= 60
        temp = a.readTemp()
        portio = a.readPortExpander()
        mqtt.single("mqtt/message", counter, hostname="192.168.0.108")
        mqtt.single("mqtt/adc1", temp, hostname="192.168.0.108")
        mqtt.single("mqtt/portexpander", portio, hostname="192.168.0.108")
        print("message: ", counter, "adc1: ", temp, "portio: ", portio)
        time.sleep(60)

main()
