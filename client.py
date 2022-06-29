import paho.mqtt.client as mqtt
import math
from bluepy import btle
import time
import binascii
import csv
from datetime import datetime
import time
import numpy
from threading import Thread
from time import sleep, perf_counter

from pprint import pprint

from flask import Flask

from bluepy.btle import Scanner, DefaultDelegate



from bson import ObjectId
import json
import paho.mqtt.publish as publish
import paho.mqtt.publish as publish2
import sys
import Adafruit_DHT
import data
import os

import spidev
import RPi.GPIO as GPIO
import time
import sys

import board
import busio
import adafruit_veml7700

# Insert addresses of sensors here:
BLE_ADDRESS = data.sensor1
BLE_ADDRESS2 = data.sensor2
BLE_ADDRESS3 = data.sensor3
BLE_ADDRESS4 = data.sensor4
BLE_ADDRESS5 = data.sensor5
BLE_ADDRESS6 = data.sensor6
# BLE sensor service
BLE_SERVICE_UUID = "0000ff30-0000-1000-8000-00805f9b34fb"
# BLE UUID:
BLE_CHARACTERISTIC_UUID = "0000ff35-0000-1000-8000-00805f9b34fb"

array_input = []
control = 0
hora_entrada = time.time()*1000.0
caracter_controlo = 0

global dev2
global dev

global addr

addr = ""


novo_control = 0

global t1
global t2
global t3

global t4
global t5
global t6
device = " "


disconnect_sensor1 = 0
disconnect_sensor2 = 0
disconnect_sensor3 = 0
disconnect_sensor4 = 0
disconnect_sensor5 = 0
disconnect_sensor6 = 0

send_data_sensor1 = 0
send_data_sensor2 = 0
send_data_sensor3 = 0
send_data_sensor4 = 0
send_data_sensor5 = 0
send_data_sensor6 = 0

batery_raw_sensor1 = 0
batery_raw_sensor2 = 0
batery_raw_sensor3 = 0
batery_raw_sensor4 = 0
batery_raw_sensor5 = 0
batery_raw_sensor6 = 0

vibration_sensor1 = 0
vibration_sensor2 = 0
vibration_sensor3 = 0
vibration_sensor4 = 0
vibration_sensor5 = 0
vibration_sensor6 = 0

excepcao_task_sensor1 = 0
excepcao_task_sensor2 = 0
excepcao_task_sensor3 = 0
excepcao_task_sensor4 = 0
excepcao_task_sensor5 = 0
excepcao_task_sensor6 = 0

sensor1_sending_data = 0
sensor2_sending_data = 0
sensor3_sending_data = 0
sensor4_sending_data = 0
sensor5_sending_data = 0
sensor6_sending_data = 0

mongo_sensor1 = 0
mongo_sensor2 = 0
mongo_sensor3 = 0
mongo_sensor4 = 0
mongo_sensor5 = 0
mongo_sensor6 = 0

mongoAdmin = data.mongo_admin
mongo_password = data.mongo_psw
string_mongo = "mongodb://"+mongoAdmin+":"+mongo_password+"@localhost:27017/"

# print(string_mongo)
# "mongodb://admin3:asd123@localhost:27017/"




msg1 = " "
msg2 = " "
msg3 = " "
msg4 = " "
msg5 = " "
msg6 = " "
msg_env = " "

controla_pub_sensor1 = 0
controla_pub_sensor2 = 0
controla_pub_sensor3 = 0
controla_pub_sensor4 = 0
controla_pub_sensor5 = 0
controla_pub_sensor6 = 0

first_time_s1 = 0
first_time_s2 = 0
first_time_s3 = 0
first_time_s4 = 0
first_time_s5 = 0
first_time_s6 = 0

sensor1_y_inclination = 0
sensor2_y_inclination = 0
sensor3_y_inclination = 0
sensor4_y_inclination = 0
sensor5_y_inclination = 0
sensor6_y_inclination = 0

controla_pub_environ = 0
first_time_envi = 0

temperature = 0
humidity = 0

sensor1_disconnect = 0
sensor2_disconnect = 0
sensor3_disconnect = 0
sensor4_disconnect = 0
sensor5_disconnect = 0
sensor6_disconnect = 0

spi = spidev.SpiDev()  # create spi object
spi.open(0, 0)  # open spi port 0, device (CS) 0, for the MCP8008
spi.max_speed_hz=100000 # !!!

i2c = busio.I2C(board.SCL, board.SDA)
veml7700 = adafruit_veml7700.VEML7700(i2c)

def readadc(adcnum):  # read out the ADC
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    r = spi.xfer2([1, (8 + adcnum) << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        data = bytearray(data)
       # print("HERE")
        # print(data)
        # print("HERE")
        byte_array = bytearray.fromhex(" ")
        lenght_data = len(data)

        global control
        global hora_entrada
        global caracter_controlo
        global msg1
        global controla_pub_sensor1
        global sensor1_y_inclination
        time_medido = time.time()*1000.0

        addr = BLE_ADDRESS

        # According to the conversion in the manual, it converts acceleration into g:
        if lenght_data > 6:
            accX = ((data[2 * 0 + 3] & 0xff) << 8) | (data[2 * 0 + 2] & 0xff)
            if accX > 32767:
                accX = -(65534 - accX) * (4.0 / 32767)
            else:
                accX *= 4.0 / 32767

            accY = ((data[2 * 1 + 3] & 0xff) << 8) | (data[2 * 1 + 2] & 0xff)
            if accY > 32767:
                accY = -(65534 - accY) * (4.0 / 32767)
            else:
                accY *= 4.0 / 32767

            accZ = ((data[2 * 2 + 3] & 0xff) << 8) | (data[2 * 2 + 2] & 0xff)
            if accZ > 32767:
                accZ = -(65534 - accZ) * (4.0 / 32767)
            else:
                accZ *= 4.0 / 32767

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S:%f")

            normalizeOfG = math.sqrt(accX * accX + accY * accY + accZ * accZ)
            accX = accX / normalizeOfG
            accY = accY / normalizeOfG
            accZ = accZ / normalizeOfG
            xInclination = math.asin(accX) * (180 / math.pi)
            yInclination = math.acos(accY) * (180 / math.pi)
            zInclination = math.atan(accZ) * (180 / math.pi)

            sensor_record = [

                {

                    "time": current_time,

                    "sensor_id": addr,

                    "Angle values": [{"Angle_X": xInclination}, {"Angle_Y": yInclination}, {"Angle_Z": zInclination}]





                }

            ]
            # my_collection.insert_many(sensor_record)

            # Stores the acceleration values in an array
            array_input.append([addr, current_time, accX, accY, accZ])

            current_time_aux = str(current_time)
            aX_aux = str(xInclination)
            aY_aux = str(yInclination)
            aZ_aux = str(zInclination)
            addr_aux = str(addr)
            posture = ""

            sensor1_y_inclination = yInclination

            if yInclination > 50.0:
                posture = "incorrect"
            else:
                posture = "correct"

            msg1 = "{\"device_datail\": {\"time\": \""+current_time_aux+"\",\"sensor_MAC\": \""+addr_aux + \
                "\",\"angle_values\": [{\"posture\": \""+posture+"\"},{\"accx\": \"" + \
                aX_aux+"\"},{\"accy\": \""+aY_aux + \
                "\"},{\"accz\": \""+aZ_aux+"\"}]}}"

            if time_medido >= (hora_entrada + 2000):

                hora_entrada = time.time()*1000.0

                caracter_controlo = 1
                array_input.clear()


class MyDelegate2(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        data = bytearray(data)
        # print("HERE")
        # print(data)
        # print("HERE")
        byte_array = bytearray.fromhex(" ")
        lenght_data = len(data)

        global control
        global hora_entrada
        global caracter_controlo
        global msg2
        global controla_pub_sensor1

        global sensor2_y_inclination

        time_medido = time.time()*1000.0

        addr = BLE_ADDRESS2

        # According to the conversion in the manual, it converts acceleration into g:
        if lenght_data > 6:
            accX = ((data[2 * 0 + 3] & 0xff) << 8) | (data[2 * 0 + 2] & 0xff)
            if accX > 32767:
                accX = -(65534 - accX) * (4.0 / 32767)
            else:
                accX *= 4.0 / 32767

            accY = ((data[2 * 1 + 3] & 0xff) << 8) | (data[2 * 1 + 2] & 0xff)
            if accY > 32767:
                accY = -(65534 - accY) * (4.0 / 32767)
            else:
                accY *= 4.0 / 32767

            accZ = ((data[2 * 2 + 3] & 0xff) << 8) | (data[2 * 2 + 2] & 0xff)
            if accZ > 32767:
                accZ = -(65534 - accZ) * (4.0 / 32767)
            else:
                accZ *= 4.0 / 32767

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S:%f")

            normalizeOfG = math.sqrt(accX * accX + accY * accY + accZ * accZ)
            accX = accX / normalizeOfG
            accY = accY / normalizeOfG
            accZ = accZ / normalizeOfG
            xInclination = math.asin(accX) * (180 / math.pi)
            yInclination = math.acos(accY) * (180 / math.pi)
            zInclination = math.atan(accZ) * (180 / math.pi)

            sensor_record = [

                {

                    "time": current_time,

                    "sensor_id": addr,

                    "Angle values": [{"Angle_X": xInclination}, {"Angle_Y": yInclination}, {"Angle_Z": zInclination}]





                }

            ]
            # my_collection.insert_many(sensor_record)

            # Stores the acceleration values in an array
            array_input.append([addr, current_time, accX, accY, accZ])

            current_time_aux = str(current_time)
            aX_aux = str(xInclination)
            aY_aux = str(yInclination)
            aZ_aux = str(zInclination)
            addr_aux = str(addr)

            sensor2_y_inclination = yInclination

            if yInclination > 50.0:
                posture = "incorrect"
            else:
                posture = "correct"

            msg2 = "{\"device_datail\": {\"time\": \""+current_time_aux+"\",\"sensor_MAC\": \""+addr_aux + \
                "\",\"angle_values\": [{\"posture\": \""+posture+"\"},{\"accx\": \"" + \
                aX_aux+"\"},{\"accy\": \""+aY_aux + \
                "\"},{\"accz\": \""+aZ_aux+"\"}]}}"

            if time_medido >= (hora_entrada + 2000):

                hora_entrada = time.time()*1000.0

                caracter_controlo = 1
                array_input.clear()


class MyDelegate3(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        data = bytearray(data)
        # print("HERE")
        # print(data)
        # print("HERE")
        byte_array = bytearray.fromhex(" ")
        lenght_data = len(data)

        global control
        global hora_entrada
        global caracter_controlo
        global msg3
        global controla_pub_sensor1
        global sensor3_y_inclination

        time_medido = time.time()*1000.0

        addr = BLE_ADDRESS3

        # According to the conversion in the manual, it converts acceleration into g:
        if lenght_data > 6:
            accX = ((data[2 * 0 + 3] & 0xff) << 8) | (data[2 * 0 + 2] & 0xff)
            if accX > 32767:
                accX = -(65534 - accX) * (4.0 / 32767)
            else:
                accX *= 4.0 / 32767

            accY = ((data[2 * 1 + 3] & 0xff) << 8) | (data[2 * 1 + 2] & 0xff)
            if accY > 32767:
                accY = -(65534 - accY) * (4.0 / 32767)
            else:
                accY *= 4.0 / 32767

            accZ = ((data[2 * 2 + 3] & 0xff) << 8) | (data[2 * 2 + 2] & 0xff)
            if accZ > 32767:
                accZ = -(65534 - accZ) * (4.0 / 32767)
            else:
                accZ *= 4.0 / 32767

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S:%f")

            normalizeOfG = math.sqrt(accX * accX + accY * accY + accZ * accZ)
            accX = accX / normalizeOfG
            accY = accY / normalizeOfG
            accZ = accZ / normalizeOfG
            xInclination = math.asin(accX) * (180 / math.pi)
            yInclination = math.acos(accY) * (180 / math.pi)
            zInclination = math.atan(accZ) * (180 / math.pi)

            sensor_record = [

                {

                    "time": current_time,

                    "sensor_id": addr,

                    "Angle values": [{"Angle_X": xInclination}, {"Angle_Y": yInclination}, {"Angle_Z": zInclination}]





                }

            ]
            # my_collection.insert_many(sensor_record)

            # Stores the acceleration values in an array
            array_input.append([addr, current_time, accX, accY, accZ])

            current_time_aux = str(current_time)
            aX_aux = str(xInclination)
            aY_aux = str(yInclination)
            aZ_aux = str(zInclination)
            addr_aux = str(addr)

            sensor3_y_inclination = yInclination

            if yInclination > 50.0:
                posture = "incorrect"
            else:
                posture = "correct"

            msg3 = "{\"device_datail\": {\"time\": \""+current_time_aux+"\",\"sensor_MAC\": \""+addr_aux + \
                "\",\"angle_values\": [{\"posture\": \""+posture+"\"},{\"accx\": \"" + \
                aX_aux+"\"},{\"accy\": \""+aY_aux + \
                "\"},{\"accz\": \""+aZ_aux+"\"}]}}"

            if time_medido >= (hora_entrada + 2000):

                hora_entrada = time.time()*1000.0

                caracter_controlo = 1
                array_input.clear()


class MyDelegate4(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        data = bytearray(data)
        # print("HERE")
        # print(data)
        # print("HERE")
        byte_array = bytearray.fromhex(" ")
        lenght_data = len(data)

        global control
        global hora_entrada
        global caracter_controlo
        global msg4
        global controla_pub_sensor1
        global sensor4_y_inclination

        time_medido = time.time()*1000.0

        addr = BLE_ADDRESS4

        # According to the conversion in the manual, it converts acceleration into g:
        if lenght_data > 6:
            accX = ((data[2 * 0 + 3] & 0xff) << 8) | (data[2 * 0 + 2] & 0xff)
            if accX > 32767:
                accX = -(65534 - accX) * (4.0 / 32767)
            else:
                accX *= 4.0 / 32767

            accY = ((data[2 * 1 + 3] & 0xff) << 8) | (data[2 * 1 + 2] & 0xff)
            if accY > 32767:
                accY = -(65534 - accY) * (4.0 / 32767)
            else:
                accY *= 4.0 / 32767

            accZ = ((data[2 * 2 + 3] & 0xff) << 8) | (data[2 * 2 + 2] & 0xff)
            if accZ > 32767:
                accZ = -(65534 - accZ) * (4.0 / 32767)
            else:
                accZ *= 4.0 / 32767

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S:%f")

            normalizeOfG = math.sqrt(accX * accX + accY * accY + accZ * accZ)
            accX = accX / normalizeOfG
            accY = accY / normalizeOfG
            accZ = accZ / normalizeOfG
            xInclination = math.asin(accX) * (180 / math.pi)
            yInclination = math.acos(accY) * (180 / math.pi)
            zInclination = math.atan(accZ) * (180 / math.pi)

            sensor_record = [

                {

                    "time": current_time,

                    "sensor_id": addr,

                    "Angle values": [{"Angle_X": xInclination}, {"Angle_Y": yInclination}, {"Angle_Z": zInclination}]





                }

            ]
            # my_collection.insert_many(sensor_record)

            # Stores the acceleration values in an array
            array_input.append([addr, current_time, accX, accY, accZ])

            current_time_aux = str(current_time)
            aX_aux = str(xInclination)
            aY_aux = str(yInclination)
            aZ_aux = str(zInclination)
            addr_aux = str(addr)

            sensor4_y_inclination = yInclination

            if yInclination > 50.0:
                posture = "incorrect"
            else:
                posture = "correct"

            msg4 = "{\"device_datail\": {\"time\": \""+current_time_aux+"\",\"sensor_MAC\": \""+addr_aux + \
                "\",\"angle_values\": [{\"posture\": \""+posture+"\"},{\"accx\": \"" + \
                aX_aux+"\"},{\"accy\": \""+aY_aux + \
                "\"},{\"accz\": \""+aZ_aux+"\"}]}}"

            if time_medido >= (hora_entrada + 2000):

                hora_entrada = time.time()*1000.0

                caracter_controlo = 1
                array_input.clear()


class MyDelegate5(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        data = bytearray(data)
        # print("HERE")
        # print(data)
        # print("HERE")
        byte_array = bytearray.fromhex(" ")
        lenght_data = len(data)

        global control
        global hora_entrada
        global caracter_controlo
        global msg5
        global controla_pub_sensor1
        global sensor5_y_inclination

        time_medido = time.time()*1000.0

        addr = BLE_ADDRESS5

        # According to the conversion in the manual, it converts acceleration into g:
        if lenght_data > 6:
            accX = ((data[2 * 0 + 3] & 0xff) << 8) | (data[2 * 0 + 2] & 0xff)
            if accX > 32767:
                accX = -(65534 - accX) * (4.0 / 32767)
            else:
                accX *= 4.0 / 32767

            accY = ((data[2 * 1 + 3] & 0xff) << 8) | (data[2 * 1 + 2] & 0xff)
            if accY > 32767:
                accY = -(65534 - accY) * (4.0 / 32767)
            else:
                accY *= 4.0 / 32767

            accZ = ((data[2 * 2 + 3] & 0xff) << 8) | (data[2 * 2 + 2] & 0xff)
            if accZ > 32767:
                accZ = -(65534 - accZ) * (4.0 / 32767)
            else:
                accZ *= 4.0 / 32767

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S:%f")

            normalizeOfG = math.sqrt(accX * accX + accY * accY + accZ * accZ)
            accX = accX / normalizeOfG
            accY = accY / normalizeOfG
            accZ = accZ / normalizeOfG
            xInclination = math.asin(accX) * (180 / math.pi)
            yInclination = math.acos(accY) * (180 / math.pi)
            zInclination = math.atan(accZ) * (180 / math.pi)

            sensor_record = [

                {

                    "time": current_time,

                    "sensor_id": addr,

                    "Angle values": [{"Angle_X": xInclination}, {"Angle_Y": yInclination}, {"Angle_Z": zInclination}]





                }

            ]
            # my_collection.insert_many(sensor_record)

            # Stores the acceleration values in an array
            array_input.append([addr, current_time, accX, accY, accZ])

            current_time_aux = str(current_time)
            aX_aux = str(xInclination)
            aY_aux = str(yInclination)
            aZ_aux = str(zInclination)
            addr_aux = str(addr)

            sensor5_y_inclination = yInclination

            if yInclination > 50.0:
                posture = "incorrect"
            else:
                posture = "correct"

            msg5 = "{\"device_datail\": {\"time\": \""+current_time_aux+"\",\"sensor_MAC\": \""+addr_aux + \
                "\",\"angle_values\": [{\"posture\": \""+posture+"\"},{\"accx\": \"" + \
                aX_aux+"\"},{\"accy\": \""+aY_aux + \
                "\"},{\"accz\": \""+aZ_aux+"\"}]}}"

            if time_medido >= (hora_entrada + 2000):

                hora_entrada = time.time()*1000.0

                caracter_controlo = 1
                array_input.clear()


class MyDelegate6(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        data = bytearray(data)
        # print("HERE")
        # print(data)
        # print("HERE")
        byte_array = bytearray.fromhex(" ")
        lenght_data = len(data)

        global control
        global hora_entrada
        global caracter_controlo
        global msg6
        global controla_pub_sensor1
        global sensor6_y_inclination

        time_medido = time.time()*1000.0

        addr = BLE_ADDRESS6

        # According to the conversion in the manual, it converts acceleration into g:
        if lenght_data > 6:
            accX = ((data[2 * 0 + 3] & 0xff) << 8) | (data[2 * 0 + 2] & 0xff)
            if accX > 32767:
                accX = -(65534 - accX) * (4.0 / 32767)
            else:
                accX *= 4.0 / 32767

            accY = ((data[2 * 1 + 3] & 0xff) << 8) | (data[2 * 1 + 2] & 0xff)
            if accY > 32767:
                accY = -(65534 - accY) * (4.0 / 32767)
            else:
                accY *= 4.0 / 32767

            accZ = ((data[2 * 2 + 3] & 0xff) << 8) | (data[2 * 2 + 2] & 0xff)
            if accZ > 32767:
                accZ = -(65534 - accZ) * (4.0 / 32767)
            else:
                accZ *= 4.0 / 32767

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S:%f")

            normalizeOfG = math.sqrt(accX * accX + accY * accY + accZ * accZ)
            accX = accX / normalizeOfG
            accY = accY / normalizeOfG
            accZ = accZ / normalizeOfG
            xInclination = math.asin(accX) * (180 / math.pi)
            yInclination = math.acos(accY) * (180 / math.pi)
            zInclination = math.atan(accZ) * (180 / math.pi)

            sensor_record = [

                {

                    "time": current_time,

                    "sensor_id": addr,

                    "Angle values": [{"Angle_X": xInclination}, {"Angle_Y": yInclination}, {"Angle_Z": zInclination}]





                }

            ]
            # my_collection.insert_many(sensor_record)

            # Stores the acceleration values in an array
            array_input.append([addr, current_time, accX, accY, accZ])

            current_time_aux = str(current_time)
            aX_aux = str(xInclination)
            aY_aux = str(yInclination)
            aZ_aux = str(zInclination)
            addr_aux = str(addr)

            sensor6_y_inclination = yInclination

            if yInclination > 50.0:
                posture = "incorrect"
            else:
                posture = "correct"

            msg6 = "{\"device_datail\": {\"time\": \""+current_time_aux+"\",\"sensor_MAC\": \""+addr_aux + \
                "\",\"angle_values\": [{\"posture\": \""+posture+"\"},{\"accx\": \"" + \
                aX_aux+"\"},{\"accy\": \""+aY_aux + \
                "\"},{\"accz\": \""+aZ_aux+"\"}]}}"

            if time_medido >= (hora_entrada + 2000):

                hora_entrada = time.time()*1000.0

                caracter_controlo = 1
                array_input.clear()


def task_publish_sensor1():
    while True:
        while controla_pub_sensor1 == 1:
            if msg1 != "n":
            	e = 0


def task_publish_sensor2():
    while True:
        while controla_pub_sensor2 == 1:
            if msg2 != "n":
            	e = 0


def task_publish_sensor3():
    while True:
        while controla_pub_sensor3 == 1:
            if msg3 != "n":
                e = 0


def task_publish_sensor4():
    while True:
        while controla_pub_sensor4 == 1:
            if msg4 != "n":
                e = 0


def task_publish_sensor5():
    while True:
        while controla_pub_sensor5 == 1:
            if msg5 != "n":
                # print(msg2)
                e = 0


def task_publish_sensor6():
    while True:
        while controla_pub_sensor6 == 1:
            if msg6 != "n":
                # print(msg3)
                e = 0


def task_publish_env():
    global controla_pub_environ
    while True:
        while controla_pub_environ == 1:
            publish.single("sensor/env/", msg_env,
                           hostname="127.0.0.1")
            controla_pub_environ = 0
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S:%f")

            sensor_record = [

                {

                    "time": current_time,


                    "Environment values": [{"Temperature": temperature}, {"Humidity": humidity}]


                }

            ]
            my_collection.insert_many(sensor_record)


def task_mongo_guardar_S1_S2():
    global sensor1_y_inclination
    global sensor2_y_inclination
    global sensor1_disconnect
    global sensor2_disconnect
    while True:
        while (mongo_sensor1 == 1) and (mongo_sensor2 == 1):
            now = datetime.now()
            current_time = now.strftime("%d/%m/%y %H:%M:%S:%f")
            diff_y = 0
            diff_y = abs(sensor2_y_inclination - sensor1_y_inclination)
         
            
            if diff_y > 20:
                postura = "incorrecta"
                #print(diff_y)

            else:
                postura = "correcta"
                
            if sensor1_disconnect == 1 or sensor2_disconnect == 1:
                postura = "correcta"
                            
            sensor_record = [

                {

                    "time": current_time,

                    "sensor1_mac": BLE_ADDRESS,

                    "sensor2_mac": BLE_ADDRESS2,

                    "Inclina_Y_diff": diff_y,

                    "Postura": postura

                }

            ]
            publish.single("sensor/sensorS1S2/", json.dumps(sensor_record),
                               hostname="127.0.0.1")
            


def task_mongo_guardar_S3_S4():
    global sensor3_y_inclination
    global sensor4_y_inclination
    global sensor3_disconnect
    global sensor4_disconnect
    while True:
        while (mongo_sensor3 == 1) and (mongo_sensor4 == 1):

            now = datetime.now()
            current_time = now.strftime("%d/%m/%y %H:%M:%S:%f")
            diff_y = 0
            diff_y = abs(sensor3_y_inclination - sensor4_y_inclination)
            if diff_y > 20:
                postura = "incorrecta"
                #print(diff_y)

            else:
                postura = "correcta"

            if sensor3_disconnect == 1 or sensor4_disconnect == 1:
                postura = "correcta"
                
            sensor_record = [

                {

                    "time": current_time,

                    "sensor1_mac": BLE_ADDRESS3,

                    "sensor2_mac": BLE_ADDRESS4,

                    "Inclina_Y_diff": diff_y,

		    "Postura": postura
                }

            ]
            publish.single("sensor/sensorS3S4/", json.dumps(sensor_record),
                               hostname="127.0.0.1")
            


def task_mongo_guardar_S5_S6():
    global sensor5_y_inclination
    global sensor6_y_inclination
    global sensor5_disconnect
    global sensor6_disconnect
    while True:
        while (mongo_sensor5 == 1) and (mongo_sensor6 == 1):

            now = datetime.now()
            current_time = now.strftime("%d/%m/%y %H:%M:%S:%f")
            diff_y = 0
            diff_y = abs(sensor5_y_inclination - sensor6_y_inclination)
            if diff_y > 20:
                postura = "incorrecta"
                #print(diff_y)

            else:
                postura = "correcta"

            if sensor5_disconnect == 1 or sensor6_disconnect == 1:
                postura = "correcta"

            sensor_record = [

                {

                    "time": current_time,

                    "sensor1_mac": BLE_ADDRESS5,

                    "sensor2_mac": BLE_ADDRESS6,

                    "Inclina_Y_diff": diff_y,

		    "Postura": postura
                }

            ]
            publish.single("sensor/sensorS5S6/", json.dumps(sensor_record),
                               hostname="127.0.0.1")
            


def task():
    global addr
    global bleservice
    global uuid_config
    global batery_raw_sensor1
    global excepcao_task_sensor1
    global msg1
    controla_except = 0
    global sensor1_disconnect


    print('Starting a task...')

    print('done')

    print("Connecting...")

    try:
        dev = btle.Peripheral(BLE_ADDRESS)
        dev.setDelegate(MyDelegate())
        service_uuid = btle.UUID(BLE_SERVICE_UUID)
        ble_service = dev.getServiceByUUID(service_uuid)
        uuidConfig = btle.UUID(BLE_CHARACTERISTIC_UUID)
        data_chrc = ble_service.getCharacteristics(uuidConfig)[0]

        bleservice = ble_service
        uuid_config = uuidConfig

    # Enable the sensor, start notifications
        if send_data_sensor1 == 1:
            data_chrc.write(bytes('\x01', encoding='utf-8'))
        time.sleep(1)  # Allow sensor to stabilise
        uuidConfig_36 = btle.UUID("0000ff36-0000-1000-8000-00805f9b34fb")
        sensor1_disconnect = 0
    except:
        controla_except = 1
        msg1 = "n"
        print("trying to reconnect,wait")
        sensor1_disconnect = 1        

    while True:
        try:
            data_chrc_read = ble_service.getCharacteristics(uuidConfig_36)[0]
            t = data_chrc_read.read()
            batery_raw_sensor1 = (t[1] & 0xff) << 8 | (t[0] & 0xff)
            sensor1_disconnect = 0
        except:
            if controla_except == 0:
                msg1 = "n"
                t1 = Thread(target=task)
                t1.start()
                print("trying to reconnect,wait")
            sensor1_disconnect = 1

        try:
            if send_data_sensor1 == 0:
                data_chrc.write(bytes('\x00', encoding='utf-8'))
            else:
                data_chrc.write(bytes('\x01', encoding='utf-8'))

            if vibration_sensor1 == 1:
                data_chrc.write(bytes('\x07', encoding='utf-8'))
            else:
                data_chrc.write(bytes('\x08', encoding='utf-8'))
            
            sensor1_disconnect = 0

        except:
            if controla_except == 0:
                msg1 = "n"
                t1 = Thread(target=task)
                t1.start()
                print("trying to reconnect,wait")
            sensor1_disconnect = 1

        try:
            if dev.waitForNotifications(1.0):
                if disconnect_sensor1 == 1:
                    dev.disconnect()
                    break
                    print("adeus")
            # handleNotification() was called
                continue
            
            sensor1_disconnect = 0

        except:
            if controla_except == 0:
                msg1 = "n"
                t1 = Thread(target=task)
                t1.start()
                print("trying to reconnect,wait")
            break
            sensor1_disconnect = 1


def task2():
    global addr
    global bleservice2
    global uuid_config2
    global batery_raw_sensor2
    global excepcao_task_sensor2
    global msg2
    controla_except = 0
    global sensor2_disconnect

    print('Starting a task...')

    print('done')

    print("Connecting...")

    try:
        dev2 = btle.Peripheral(BLE_ADDRESS2)
        dev2.setDelegate(MyDelegate2())
        service_uuid2 = btle.UUID(BLE_SERVICE_UUID)
        ble_service2 = dev2.getServiceByUUID(service_uuid2)
        uuidConfig2 = btle.UUID(BLE_CHARACTERISTIC_UUID)
        data_chrc2 = ble_service2.getCharacteristics(uuidConfig2)[0]

        bleservice2 = ble_service2
        uuid_config2 = uuidConfig2

    # Enable the sensor, start notifications
        if send_data_sensor2 == 1:
            data_chrc2.write(bytes('\x01', encoding='utf-8'))
        time.sleep(1)  # Allow sensor to stabilise
        uuidConfig_36 = btle.UUID("0000ff36-0000-1000-8000-00805f9b34fb")
        sensor2_disconnect = 0

    except:
        controla_except = 1
        msg2 = "n"
        print("caiu aquIU!!!!!!!!-1")
        sensor2_disconnect = 1

    while True:
        try:
            data_chrc_read = ble_service2.getCharacteristics(uuidConfig_36)[0]
            t = data_chrc_read.read()
            batery_raw_sensor2 = (t[1] & 0xff) << 8 | (t[0] & 0xff)
            sensor2_disconnect = 0
        except:
            if controla_except == 0:
                msg2 = "n"
                t2 = Thread(target=task2)
                t2.start()
                print("caiu aquIU!!!!!!!!-2")
            sensor2_disconnect = 1

        try:
            if send_data_sensor2 == 0:
                data_chrc2.write(bytes('\x00', encoding='utf-8'))
            else:
                data_chrc2.write(bytes('\x01', encoding='utf-8'))

            if vibration_sensor2 == 1:
                data_chrc2.write(bytes('\x07', encoding='utf-8'))
            else:
                data_chrc2.write(bytes('\x08', encoding='utf-8'))
                
            sensor2_disconnect = 0

        except:
            if controla_except == 0:
                msg2 = "n"
                t2 = Thread(target=task2)
                t2.start()
                print("caiu aquIU!!!!!!!!-3")
            sensor2_disconnect = 1

        try:
            if dev2.waitForNotifications(1.0):
                if disconnect_sensor2 == 1:
                    dev2.disconnect()
                    break
                    print("adeus")
            # handleNotification() was called
                continue
            sensor2_disconnect = 0

        except:
            if controla_except == 0:
                msg2 = "n"
                t2 = Thread(target=task2)
                t2.start()
                print("caiu aquIU!!!!!!!!-4")
            break
            sensor2_disconnect = 1


def task3():
    global addr
    global bleservice3
    global uuid_config3
    global batery_raw_sensor3
    global excepcao_task_sensor3
    global msg3
    controla_except = 0
    global sensor3_disconnect
    print('Starting a task...')

    print('done')

    print("Connecting...")

    try:
        dev3 = btle.Peripheral(BLE_ADDRESS3)
        dev3.setDelegate(MyDelegate3())
        service_uuid3 = btle.UUID(BLE_SERVICE_UUID)
        ble_service3 = dev3.getServiceByUUID(service_uuid3)
        uuidConfig3 = btle.UUID(BLE_CHARACTERISTIC_UUID)
        data_chrc3 = ble_service3.getCharacteristics(uuidConfig3)[0]

        bleservice3 = ble_service3
        uuid_config3 = uuidConfig3
        sensor3_disconnect = 0

    # Enable the sensor, start notifications
        if send_data_sensor3 == 1:
            data_chrc3.write(bytes('\x01', encoding='utf-8'))
        time.sleep(1)  # Allow sensor to stabilise
        uuidConfig_36 = btle.UUID("0000ff36-0000-1000-8000-00805f9b34fb")

    except:
        controla_except = 1
        msg3 = "n"
        print("trying to reconnect,wait")
        sensor3_disconnect = 1

    while True:
        try:
            data_chrc_read = ble_service3.getCharacteristics(uuidConfig_36)[0]
            t = data_chrc_read.read()
            batery_raw_sensor3 = (t[1] & 0xff) << 8 | (t[0] & 0xff)
            sensor3_disconnect = 0
        except:
            if controla_except == 0:
                msg3 = "n"
                t3 = Thread(target=task3)
                t3.start()
                print("trying to reconnect,wait")
            sensor3_disconnect = 1

        try:
            if send_data_sensor3 == 0:
                data_chrc3.write(bytes('\x00', encoding='utf-8'))
            else:
                data_chrc3.write(bytes('\x01', encoding='utf-8'))

            if vibration_sensor3 == 1:
                data_chrc3.write(bytes('\x07', encoding='utf-8'))
            else:
                data_chrc3.write(bytes('\x08', encoding='utf-8'))
                
            sensor3_disconnect = 0

        except:
            if controla_except == 0:
                msg3 = "n"
                t3 = Thread(target=task3)
                t3.start()
                print("trying to reconnect,wait")
                
            sensor3_disconnect = 1

        try:
            if dev3.waitForNotifications(1.0):
                if disconnect_sensor3 == 1:
                    dev3.disconnect()
                    break
                    print("adeus")
            # handleNotification() was called
                continue
            sensor3_disconnect = 0

        except:
            if controla_except == 0:
                msg3 = "n"
                t3 = Thread(target=task3)
                t3.start()
                print("trying to reconnect,wait")
            break
            sensor3_disconnect = 1


def task4():
    global addr
    global bleservice4
    global uuid_config4
    global batery_raw_sensor4
    global excepcao_task_sensor4
    global msg4
    controla_except = 0
    global sensor4_disconnect

    print('Starting a task...')

    print('done')

    print("Connecting...")

    try:
        dev4 = btle.Peripheral(BLE_ADDRESS4)
        dev4.setDelegate(MyDelegate4())
        service_uuid4 = btle.UUID(BLE_SERVICE_UUID)
        ble_service4 = dev4.getServiceByUUID(service_uuid4)
        uuidConfig4 = btle.UUID(BLE_CHARACTERISTIC_UUID)
        data_chrc4 = ble_service4.getCharacteristics(uuidConfig4)[0]

        bleservice4 = ble_service4
        uuid_config4 = uuidConfig4
        sensor4_disconnect = 0

    # Enable the sensor, start notifications
        if send_data_sensor4 == 1:
            data_chrc4.write(bytes('\x01', encoding='utf-8'))
        time.sleep(1)  # Allow sensor to stabilise
        uuidConfig_36 = btle.UUID("0000ff36-0000-1000-8000-00805f9b34fb")

    except:
        controla_except = 1
        msg4 = "n"
        print("trying to reconnect,wait")
        sensor4_disconnect = 1

    while True:
        try:
            data_chrc_read = ble_service4.getCharacteristics(uuidConfig_36)[0]
            t = data_chrc_read.read()
            batery_raw_sensor4 = (t[1] & 0xff) << 8 | (t[0] & 0xff)
            sensor4_disconnect = 0
        except:
            if controla_except == 0:
                msg4 = "n"
                t4 = Thread(target=task4)
                t4.start()
                print("trying to reconnect,wait")
            sensor4_disconnect = 1


        try:
            if send_data_sensor4 == 0:
                data_chrc4.write(bytes('\x00', encoding='utf-8'))
            else:
                data_chrc4.write(bytes('\x01', encoding='utf-8'))

            if vibration_sensor4 == 1:
                data_chrc4.write(bytes('\x07', encoding='utf-8'))
            else:
                data_chrc4.write(bytes('\x08', encoding='utf-8'))
            sensor4_disconnect = 0

        except:
            if controla_except == 0:
                msg4 = "n"
                t4 = Thread(target=task4)
                t4.start()
                print("trying to reconnect,wait")
            sensor4_disconnect = 1

        try:
            if dev4.waitForNotifications(1.0):
                if disconnect_sensor4 == 1:
                    dev4.disconnect()
                    break
                    print("adeus")
            # handleNotification() was called
                continue
            sensor4_disconnect = 0

        except:
            if controla_except == 0:
                msg4 = "n"
                t4 = Thread(target=task4)
                t4.start()
                print("trying to reconnect,wait")
            break
            sensor4_disconnect = 1


def task5():
    global addr
    global bleservice5
    global uuid_config5
    global batery_raw_sensor5
    global excepcao_task_sensor5
    global msg5
    controla_except = 0
    global sensor5_disconnect

    print('Starting a task...')

    print('done')

    print("Connecting...")

    try:
        dev5 = btle.Peripheral(BLE_ADDRESS5)
        dev5.setDelegate(MyDelegate5())
        service_uuid5 = btle.UUID(BLE_SERVICE_UUID)
        ble_service5 = dev5.getServiceByUUID(service_uuid5)
        uuidConfig5 = btle.UUID(BLE_CHARACTERISTIC_UUID)
        data_chrc5 = ble_service5.getCharacteristics(uuidConfig5)[0]

        bleservice5 = ble_service5
        uuid_config5 = uuidConfig5
        sensor5_disconnect = 0

    # Enable the sensor, start notifications
        if send_data_sensor5 == 1:
            data_chrc5.write(bytes('\x01', encoding='utf-8'))
        time.sleep(1)  # Allow sensor to stabilise
        uuidConfig_36 = btle.UUID("0000ff36-0000-1000-8000-00805f9b34fb")

    except:
        controla_except = 1
        msg5 = "n"
        print("trying to reconnect,wait")
        sensor5_disconnect = 1

    while True:
        try:
            data_chrc_read = ble_service5.getCharacteristics(uuidConfig_36)[0]
            t = data_chrc_read.read()
            batery_raw_sensor5 = (t[1] & 0xff) << 8 | (t[0] & 0xff)
            sensor5_disconnect = 0
        except:
            if controla_except == 0:
                msg5 = "n"
                t5 = Thread(target=task5)
                t5.start()
                print("trying to reconnect,wait")
            sensor5_disconnect = 1

        try:
            if send_data_sensor5 == 0:
                data_chrc5.write(bytes('\x00', encoding='utf-8'))
            else:
                data_chrc5.write(bytes('\x01', encoding='utf-8'))

            if vibration_sensor5 == 1:
                data_chrc5.write(bytes('\x07', encoding='utf-8'))
            else:
                data_chrc5.write(bytes('\x08', encoding='utf-8'))
            sensor5_disconnect = 0

        except:
            if controla_except == 0:
                msg5 = "n"
                t5 = Thread(target=task5)
                t5.start()
                print("trying to reconnect,wait")
            sensor5_disconnect = 1

        try:
            if dev5.waitForNotifications(1.0):
                if disconnect_sensor5 == 1:
                    dev5.disconnect()
                    break
                    print("adeus")
            # handleNotification() was called
                continue
            sensor5_disconnect = 0

        except:
            if controla_except == 0:
                msg5 = "n"
                t5 = Thread(target=task5)
                t5.start()
                print("trying to reconnect,wait")
            break
            sensor5_disconnect = 1


def task6():
    global addr
    global bleservice6
    global uuid_config6
    global batery_raw_sensor6
    global excepcao_task_sensor6
    global msg6
    controla_except = 0
    global sensor6_disconnect

    print('Starting a task...')

    print('done')

    print("Connecting...")

    try:
        dev6 = btle.Peripheral(BLE_ADDRESS6)
        dev6.setDelegate(MyDelegate6())
        service_uuid6 = btle.UUID(BLE_SERVICE_UUID)
        ble_service6 = dev6.getServiceByUUID(service_uuid6)
        uuidConfig6 = btle.UUID(BLE_CHARACTERISTIC_UUID)
        data_chrc6 = ble_service6.getCharacteristics(uuidConfig6)[0]

        bleservice6 = ble_service6
        uuid_config6 = uuidConfig6
        sensor6_disconnect = 0

    # Enable the sensor, start notifications
        if send_data_sensor6 == 1:
            data_chrc6.write(bytes('\x01', encoding='utf-8'))
        time.sleep(1)  # Allow sensor to stabilise
        uuidConfig_36 = btle.UUID("0000ff36-0000-1000-8000-00805f9b34fb")

    except:
        controla_except = 1
        msg6 = "n"
        print("trying to reconnect,wait")
        sensor6_disconnect = 1

    while True:
        try:
            data_chrc_read = ble_service6.getCharacteristics(uuidConfig_36)[0]
            t = data_chrc_read.read()
            batery_raw_sensor6 = (t[1] & 0xff) << 8 | (t[0] & 0xff)
            sensor6_disconnect = 0
        except:
            if controla_except == 0:
                msg6 = "n"
                t6 = Thread(target=task6)
                t6.start()
                print("trying to reconnect,wait")
            sensor6_disconnect = 1

        try:
            if send_data_sensor6 == 0:
                data_chrc6.write(bytes('\x00', encoding='utf-8'))
            else:
                data_chrc6.write(bytes('\x01', encoding='utf-8'))

            if vibration_sensor6 == 1:
                data_chrc6.write(bytes('\x07', encoding='utf-8'))
            else:
                data_chrc6.write(bytes('\x08', encoding='utf-8'))
                
            sensor6_disconnect = 0

        except:
            if controla_except == 0:
                msg6 = "n"
                t6 = Thread(target=task6)
                t6.start()
                print("trying to reconnect,wait")
            sensor6_disconnect = 1

        try:
            if dev6.waitForNotifications(1.0):
                if disconnect_sensor6 == 1:
                    dev6.disconnect()
                    break
                    print("adeus")
            # handleNotification() was called
                continue
                
            sensor6_disconnect = 0

        except:
            if controla_except == 0:
                msg6 = "n"
                t6 = Thread(target=task6)
                t6.start()
                print("trying to reconnect,wait")
            break
            sensor6_disconnect = 1
            
            
def task_email():
       os.chdir("/home/pi/Desktop/ICU_COVID")        
       #os.system('sudo python3 database.py')


def task_nova():
    #while True:
       t_task_email = Thread(target=task_email)
       t_task_email.start()

       publish.single("sensor/topic", "connect/sensor1", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "start_data/sensor1", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "connect/sensor2", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "start_data/sensor2", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "connect/sensor3", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "start_data/sensor3", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "connect/sensor4", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "start_data/sensor4", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "connect/sensor5", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "start_data/sensor5", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "connect/sensor6", hostname="127.0.0.1")
       time.sleep(0.5)
       publish.single("sensor/topic", "start_data/sensor6", hostname="127.0.0.1")
       time.sleep(3.0)
       #t_task_react = Thread(target=task_react)
       #t_task_react.start()  
       time.sleep(20.0) 
       os.chdir("/home/pi/Desktop/ICU_COVID")        
       os.system('sudo python3 main2eng.py')
       

def task_batt_envi():
    while True:
       time.sleep(20)
       publish.single("sensor/topic", "get_battery/sensor1", hostname="127.0.0.1")
       publish.single("sensor/topic", "get_battery/sensor3", hostname="127.0.0.1")
       publish.single("sensor/topic", "get_battery/sensor5", hostname="127.0.0.1")
       publish.single("sensor/topic", "get_environment", hostname="127.0.0.1")
    	

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # SUBSCRIBING SERVICES:
    client.subscribe("sensor/topic")
    t_nova = Thread(target=task_nova)
    t_nova.start()

# The callback for when a PUBLISH message is received from the server.

def task_react():
       print("Ract app")
       os.chdir("/home/raspi/Desktop/codigo/dash3/")
       os.system("npm start")
       os.system("react-scripts start")


def battery_percent(bat_raw):
    print("ola!!!!")
    if bat_raw < 1090:
        bat_perc = 1
        return bat_perc
    if bat_raw == 1090:
        bat_perc = 5
        return bat_perc
    if (bat_raw > 1090) and (bat_raw < 1095):
        bat_perc = 7
        return bat_perc
    if bat_raw == 1095:
        bat_perc = 10
        return bat_perc

    if (bat_raw > 1095) and (bat_raw < 1100):
        bat_perc = 12
        return bat_perc
    if bat_raw == 1100:
        bat_perc = 15
        return bat_perc
    if (bat_raw > 1100) and (bat_raw < 1110):
        bat_perc = 17
        return bat_perc
    if bat_raw == 1110:
        bat_perc = 20
        return bat_perc

    if (bat_raw > 1110) and (bat_raw < 1120):
        bat_perc = 23
        return bat_perc
    if bat_raw == 1120:
        bat_perc = 25
        return bat_perc
    if (bat_raw > 1120) and (bat_raw < 1131):
        bat_perc = 28
        return bat_perc
    if bat_raw == 1131:
        bat_perc = 30
        return bat_perc

    if (bat_raw > 1131) and (bat_raw < 1145):
        bat_perc = 32
        return bat_perc
    if bat_raw == 1145:
        bat_perc = 35
        return bat_perc
    if (bat_raw > 1145) and (bat_raw < 1160):
        bat_perc = 38
        return bat_perc
    if bat_raw == 1160:
        bat_perc = 40
        return bat_perc

    if (bat_raw > 1160) and (bat_raw < 1180):
        bat_perc = 43
        return bat_perc
    if bat_raw == 1180:
        bat_perc = 45
        return bat_perc
    if (bat_raw > 1180) and (bat_raw < 1204):
        bat_perc = 47
        return bat_perc
    if bat_raw == 1204:
        bat_perc = 50
        return bat_perc

    if (bat_raw > 1204) and (bat_raw < 1228):
        bat_perc = 53
        return bat_perc
    if bat_raw == 1228:
        bat_perc = 55
        return bat_perc
    if (bat_raw > 1228) and (bat_raw < 1252):
        bat_perc = 57
        return bat_perc
    if bat_raw == 1252:
        bat_perc = 60
        return bat_perc

    if (bat_raw > 1252) and (bat_raw < 1267):
        bat_perc = 63
        return bat_perc
    if bat_raw == 1267:
        bat_perc = 65
        return bat_perc
    if (bat_raw > 1267) and (bat_raw < 1283):
        bat_perc = 67
        return bat_perc
    if bat_raw == 1283:
        bat_perc = 70
        return bat_perc

    if (bat_raw > 1283) and (bat_raw < 1296):
        bat_perc = 73
        return bat_perc
    if bat_raw == 1296:
        bat_perc = 75
        return bat_perc
    if (bat_raw > 1296) and (bat_raw < 1309):
        bat_perc = 77
        return bat_perc
    if bat_raw == 1309:
        bat_perc = 80
        return bat_perc

    if (bat_raw > 1309) and (bat_raw < 1320):
        bat_perc = 83
        return bat_perc
    if bat_raw == 1320:
        bat_perc = 85
        return bat_perc
    if (bat_raw > 1320) and (bat_raw < 1333):
        bat_perc = 87
        return bat_perc
    if bat_raw == 1333:
        bat_perc = 90
        return bat_perc

    if (bat_raw > 1333) and (bat_raw < 1370):
        bat_perc = 93
        return bat_perc
    if bat_raw == 1370:
        bat_perc = 95
        return bat_perc
    if (bat_raw > 1370) and (bat_raw < 1400):
        bat_perc = 97
        return bat_perc
    if (bat_raw == 1400) or (bat_raw > 1400):
        bat_perc = 100
        return bat_perc


def on_message(client, userdata, msg):

    global disconnect_sensor1
    global disconnect_sensor2
    global disconnect_sensor3
    global disconnect_sensor4
    global disconnect_sensor5
    global disconnect_sensor6
    global send_data_sensor1
    global send_data_sensor2
    global send_data_sensor3
    global send_data_sensor4
    global send_data_sensor5
    global send_data_sensor6

    global vibration_sensor1
    global vibration_sensor2
    global vibration_sensor3
    global vibration_sensor4
    global vibration_sensor5
    global vibration_sensor6
    global controla_pub_sensor1
    global controla_pub_sensor2
    global controla_pub_sensor3
    global controla_pub_sensor4
    global controla_pub_sensor5
    global controla_pub_sensor6

    global first_time_s1
    global first_time_s2
    global first_time_s3
    global first_time_s4
    global first_time_s5
    global first_time_s6

    global vibration_sensor1
    global vibration_sensor2
    global vibration_sensor3
    global vibration_sensor4
    global vibration_sensor5
    global vibration_sensor6
    global controla_pub_environ
    global first_time_envi
    global msg_env
    global sensor1_sending_data
    global sensor2_sending_data
    global sensor3_sending_data
    global sensor4_sending_data
    global sensor5_sending_data
    global sensor6_sending_data

    global mongo_sensor1
    global mongo_sensor2
    global mongo_sensor3
    global mongo_sensor4
    global mongo_sensor5
    global mongo_sensor6

    print(msg.topic+" "+str(msg.payload))

    if msg.payload.decode("utf-8") == "connect/sensor1":
        disconnect_sensor1 = 0
        t1 = Thread(target=task)
        t1.start()
        sensor1_sending_data = 1

        # Do something else

    if msg.payload.decode("utf-8") == "connect/sensor2":
        disconnect_sensor2 = 0
        t2 = Thread(target=task2)
        t2.start()
        sensor2_sending_data = 1

        # Do something else

    if msg.payload.decode("utf-8") == "connect/sensor3":
        disconnect_sensor3 = 0
        t3 = Thread(target=task3)
        t3.start()

    if msg.payload.decode("utf-8") == "connect/sensor4":
        disconnect_sensor4 = 0
        t4 = Thread(target=task4)
        t4.start()
        sensor4_sending_data = 1

        # Do something else

    if msg.payload.decode("utf-8") == "connect/sensor5":
        disconnect_sensor5 = 0
        t5 = Thread(target=task5)
        t5.start()
        sensor5_sending_data = 1

        # Do something else

    if msg.payload.decode("utf-8") == "connect/sensor6":
        disconnect_sensor6 = 0
        t6 = Thread(target=task6)
        t6.start()

    if msg.payload.decode("utf-8") == "disconnect/sensor1":
        disconnect_sensor1 = 1

        # Do something else

    if msg.payload.decode("utf-8") == "disconnect/sensor2":
        disconnect_sensor2 = 1

        # Do something else

    if msg.payload.decode("utf-8") == "disconnect/sensor3":
        disconnect_sensor3 = 1

    if msg.payload.decode("utf-8") == "disconnect/sensor4":
        disconnect_sensor4 = 1

        # Do something else

    if msg.payload.decode("utf-8") == "disconnect/sensor5":
        disconnect_sensor5 = 1

        # Do something else

    if msg.payload.decode("utf-8") == "disconnect/sensor6":
        disconnect_sensor6 = 1

        # Do something else

    if msg.payload.decode("utf-8") == "start_data/sensor1":
        send_data_sensor1 = 1
        controla_pub_sensor1 = 1
        mongo_sensor1 = 1
        if first_time_s1 == 0:
            t_publish_sensor1 = Thread(target=task_publish_sensor1)
            t_publish_sensor1.start()

            t_mongoS1S2 = Thread(target=task_mongo_guardar_S1_S2)
            t_mongoS1S2.start()
            first_time_s1 = 1

    if msg.payload.decode("utf-8") == "start_data/sensor2":
        send_data_sensor2 = 1
        controla_pub_sensor2 = 1
        mongo_sensor2 = 1
        if first_time_s2 == 0:
            t_publish_sensor2 = Thread(target=task_publish_sensor2)
            t_publish_sensor2.start()

            first_time_s2 = 1
            
            time.sleep(0.5)

            
            time.sleep(0.5)
            t_task_batt_envi = Thread(target=task_batt_envi)
            t_task_batt_envi.start()
            
            

    if msg.payload.decode("utf-8") == "start_data/sensor3":
        send_data_sensor3 = 1
        controla_pub_sensor3 = 1
        mongo_sensor3 = 1
        if first_time_s3 == 0:
            t_publish_sensor3 = Thread(target=task_publish_sensor3)
            t_publish_sensor3.start()

            t_mongoS3S4 = Thread(target=task_mongo_guardar_S3_S4)
            t_mongoS3S4.start()
            first_time_s3 = 1

    if msg.payload.decode("utf-8") == "start_data/sensor4":
        send_data_sensor4 = 1
        controla_pub_sensor4 = 1
        mongo_sensor4 = 1
        if first_time_s4 == 0:
            t_publish_sensor4 = Thread(target=task_publish_sensor4)
            t_publish_sensor4.start()
            first_time_s4 = 1

    if msg.payload.decode("utf-8") == "start_data/sensor5":
        send_data_sensor5 = 1
        controla_pub_sensor5 = 1
        mongo_sensor5 = 1
        if first_time_s5 == 0:
            t_publish_sensor5 = Thread(target=task_publish_sensor5)
            t_publish_sensor5.start()

            t_mongoS5S6 = Thread(target=task_mongo_guardar_S5_S6)
            t_mongoS5S6.start()
            first_time_s5 = 1

    if msg.payload.decode("utf-8") == "start_data/sensor6":
        send_data_sensor6 = 1
        controla_pub_sensor6 = 1
        mongo_sensor6 = 1
        if first_time_s6 == 0:
            t_publish_sensor6 = Thread(target=task_publish_sensor6)
            t_publish_sensor6.start()
            first_time_s6 = 1

    if msg.payload.decode("utf-8") == "end_data/sensor1":
        send_data_sensor1 = 0
        controla_pub_sensor1 = 0
        mongo_sensor1 = 0

    if msg.payload.decode("utf-8") == "end_data/sensor2":
        send_data_sensor2 = 0
        controla_pub_sensor2 = 0
        mongo_sensor2 = 0

    if msg.payload.decode("utf-8") == "end_data/sensor3":
        send_data_sensor3 = 0
        controla_pub_sensor3 = 0
        mongo_sensor3 = 0

    if msg.payload.decode("utf-8") == "end_data/sensor4":
        send_data_sensor4 = 0
        controla_pub_sensor4 = 0
        mongo_sensor4 = 0

    if msg.payload.decode("utf-8") == "end_data/sensor5":
        send_data_sensor5 = 0
        controla_pub_sensor5 = 0
        mongo_sensor5 = 0

    if msg.payload.decode("utf-8") == "end_data/sensor6":
        send_data_sensor6 = 0
        controla_pub_sensor6 = 0
        mongo_sensor6 = 0

    if msg.payload.decode("utf-8") == "start_vibration/sensor1":
        vibration_sensor1 = 1

        # Do something else

    if msg.payload.decode("utf-8") == "start_vibration/sensor2":
        vibration_sensor2 = 1

        # Do something else

    if msg.payload.decode("utf-8") == "start_vibration/sensor3":
        vibration_sensor3 = 1

    if msg.payload.decode("utf-8") == "start_vibration/sensor4":
        vibration_sensor4 = 1

        # Do something else

    if msg.payload.decode("utf-8") == "start_vibration/sensor5":
        vibration_sensor5 = 1

        # Do something else

    if msg.payload.decode("utf-8") == "start_vibration/sensor6":
        vibration_sensor6 = 1

    if msg.payload.decode("utf-8") == "end_vibration/sensor1":
        vibration_sensor1 = 0

        # Do something else

    if msg.payload.decode("utf-8") == "end_vibration/sensor2":
        vibration_sensor2 = 0

        # Do something else

    if msg.payload.decode("utf-8") == "end_vibration/sensor3":
        vibration_sensor3 = 0

    if msg.payload.decode("utf-8") == "end_vibration/sensor4":
        vibration_sensor4 = 0

        # Do something else

    if msg.payload.decode("utf-8") == "end_vibration/sensor5":
        vibration_sensor5 = 0

        # Do something else

    if msg.payload.decode("utf-8") == "end_vibration/sensor6":
        vibration_sensor6 = 0
        
    if msg.payload.decode("utf-8") == "get_mongo_data":
        cursor = my_collection.find()
        list_cur = list(cursor)
        jsonstring = JSONEncoder().encode(list_cur)
        string_json = str(jsonstring)
        publish.single("sensor/get_mongo_info/", string_json,
                               hostname="127.0.0.1")

    if msg.payload.decode("utf-8") == "get_battery/sensor1":
        bat_perc = battery_percent(batery_raw_sensor1)
        bat_perc_string = str(bat_perc)
        msg_bat = json.dumps({"battery_level": bat_perc_string})
        publish.single("sensor/battery_sensor1/", msg_bat,
                       hostname="127.0.0.1")

        # Do something else

    if msg.payload.decode("utf-8") == "get_battery/sensor2":
        bat_perc2 = battery_percent(batery_raw_sensor2)
        bat_perc_string2 = str(bat_perc2)
        msg_bat2 = json.dumps({"battery_level": bat_perc_string2})
        publish.single("sensor/battery_sensor2/", msg_bat2,
                       hostname="127.0.0.1")

        # Do something else

    if msg.payload.decode("utf-8") == "get_battery/sensor3":
        bat_perc3 = battery_percent(batery_raw_sensor3)
        bat_perc_string3 = str(bat_perc3)
        msg_bat3 = json.dumps({"battery_level": bat_perc_string3})
        publish.single("sensor/battery_sensor3/", msg_bat3,
                       hostname="127.0.0.1")

    if msg.payload.decode("utf-8") == "get_battery/sensor4":
        bat_perc4 = battery_percent(batery_raw_sensor4)
        bat_perc_string4 = str(bat_perc4)
        msg_bat4 = json.dumps({"battery_level": bat_perc_string4})
        publish.single("sensor/battery_sensor4/", msg_bat4,
                       hostname="127.0.0.1")

    if msg.payload.decode("utf-8") == "get_battery/sensor5":
        bat_perc5 = battery_percent(batery_raw_sensor5)
        bat_perc_string5 = str(bat_perc5)
        msg_bat5 = json.dumps({"battery_level": bat_perc_string5})
        publish.single("sensor/battery_sensor5/", msg_bat5,
                       hostname="127.0.0.1")

    if msg.payload.decode("utf-8") == "get_battery/sensor6":
        bat_perc6 = battery_percent(batery_raw_sensor6)
        bat_perc_string6 = str(bat_perc6)
        msg_bat6 = json.dumps({"battery_level": bat_perc_string6})
        publish.single("sensor/battery_sensor6/", msg_bat6,
                       hostname="127.0.0.1")

    if msg.payload.decode("utf-8") == "get_environment":

        controla_pub_environ = 1
        global temperature
        global humidity
        ambient_light = str(veml7700.light)
        

        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        temp_str = str(temperature)
        hum_str = str(humidity)
        adc = readadc(0)
        v = adc * (3.3 / 1023.0)  # Convert value to voltage ( changed to 3.3v )
        ppm=302.7*math.exp(1.0698*(v))
        ppm_str = str(round(ppm,2))
        msg_env = json.dumps({"Temperature": temp_str,"Humidity": hum_str,"Co2": ppm_str,"Light": ambient_light})        
 
        publish.single("sensor/env/", msg_env,
                       hostname="127.0.0.1")
        controla_pub_environ = 0
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:%f")

        sensor_record = [

            {

                "time": current_time,


                "Environment values": [{"Temperature": temperature}, {"Humidity": humidity}]


            }

        ]
        

    if msg.payload.decode("utf-8") == "list_devices":
        global device
        device = " "
        conta_dispo = 0
        # while True:
        service = DiscoveryService()
        devices = service.discover(2)
        addresArray = []

        # publish.single("sensor/return3/", msg, hostname="test.mosquitto.org")
        for address, name in devices.items():
            conta_dispo += 1
            print("Name: {}, address: {}".format(name, address))

            # addresArray.append(address)
            if address == "20:C3:8F:D0:CF:10":
                api_num = "1"
                device_name = "Device Name:" + api_num
                addresArray.append(device_name)
                device_mac = "Device MAC:" + address
                addresArray.append(device_mac)
            else:
                if address == "48:70:1E:10:6A:13":
                    api_num = "2"
                    device_name = "Device Name:" + api_num
                    addresArray.append(device_name)
                    device_mac = "Device MAC:" + address
                    addresArray.append(device_mac)
                    # device += address + '-endpoint:' + api_num + ', '
                else:
                    if address == "48:70:1E:10:6A:5A":
                        api_num = "3"
                        device_name = "Device Name:" + api_num
                        addresArray.append(device_name)
                        device_mac = "Device MAC:" + address
                        addresArray.append(device_mac)
                        # device += address + '-endpoint:' + api_num + ', '
                    else:
                        device_name = "Device Name:" + "unknown"
                        addresArray.append(device_name)
                        device_mac = "Device MAC:" + address
                        addresArray.append(device_mac)

            json_data = json.dumps(addresArray)
            print(json_data)


# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)





# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()
