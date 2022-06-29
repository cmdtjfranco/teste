import time
import tkinter
from tkinter import *
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading
import json
from PIL import ImageTk, Image
from datetime import datetime
import os
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

tx = "1"
i = 0
end = False
sensor1 = json.dumps([{"value": "none"}])
sensor2 = json.dumps([{"value": "none"}])
sensor3 = json.dumps([{"value": "none"}])
battery1 = json.dumps([{"value": "none"}])
battery2 = json.dumps([{"value": "none"}])
battery3 = json.dumps([{"value": "none"}])
env = json.dumps([{"value": "none"}])


class View(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        # root window
        self.root = parent
        self.root.title('Dashboard')
        self.root.configure(bg='#f0f0f0')

        # get info screen
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        root.geometry(str(self.screen_width) + "x" + str(self.screen_height))
        #root.geometry(str(1520) + "x" + str(680))

        # configure the grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=4)

        # frame_row_top
        self.frame_row_top = Frame(self.root, bg="#f0f0f0")
        self.frame_row_top.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_row_top.columnconfigure(0, weight=1)
        self.frame_row_top.columnconfigure(1, weight=10)
        self.frame_row_top.columnconfigure(2, weight=10)
        self.frame_row_top.columnconfigure(3, weight=10)
        self.frame_row_top.rowconfigure(0, weight=1)
        
        # frame_row_bottom
        self.frame_row_bottom = Frame(root, bg="#f0f0f0")
        self.frame_row_bottom.grid(column=0, row=1, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_row_bottom.columnconfigure(0, weight=0)
        self.frame_row_bottom.columnconfigure(1, weight=50)
        self.frame_row_bottom.columnconfigure(2, weight=50)
        self.frame_row_bottom.columnconfigure(3, weight=50)
        self.frame_row_bottom.columnconfigure(4, weight=50)

        self.frame_row_bottom.rowconfigure(0, weight=5)
        self.frame_row_bottom.rowconfigure(1, weight=5)
        self.frame_row_bottom.rowconfigure(2, weight=5)
        
        # frame_third_bottom
        self.frame_third_bottom = Frame(root, bg="#f0f0f0")
        self.frame_third_bottom.grid(column=0, row=3, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_third_bottom.columnconfigure(0, weight=1)
        self.frame_third_bottom.columnconfigure(1, weight=10)
        self.frame_third_bottom.columnconfigure(2, weight=10)
        self.frame_third_bottom.columnconfigure(3, weight=10)
        self.frame_third_bottom.rowconfigure(0, weight=1)
        
        """
        self.frame_third_bottom.columnconfigure(0, weight=0)
        self.frame_third_bottom.columnconfigure(1, weight=50)
        self.frame_third_bottom.columnconfigure(2, weight=50)
        self.frame_third_bottom.columnconfigure(3, weight=50)
        self.frame_third_bottom.columnconfigure(4, weight=50)

        self.frame_third_bottom.rowconfigure(0, weight=5)
        self.frame_third_bottom.rowconfigure(1, weight=5)
        self.frame_third_bottom.rowconfigure(2, weight=5)        
        """
        """
        self.frame_row_bottom.columnconfigure(0, weight=50)
        self.frame_row_bottom.columnconfigure(1, weight=50)
        self.frame_row_bottom.columnconfigure(2, weight=50)
        self.frame_row_bottom.columnconfigure(3, weight=50)
        
        self.frame_row_bottom.columnconfigure(4, weight=5)
        
        self.frame_row_bottom.rowconfigure(0, weight=2)
        self.frame_row_bottom.rowconfigure(1, weight=2)
        self.frame_row_bottom.rowconfigure(2, weight=2)
        self.frame_row_bottom.rowconfigure(3, weight=2)
        self.frame_row_bottom.rowconfigure(4, weight=2)
        #self.frame_row_bottom.rowconfigure(5, weight=2)
        """


        # frame_image
        self.frame_image = Frame(self.frame_row_top, bg="#f0f0f0")
        self.frame_image.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_image.rowconfigure(0, weight=1)
        self.frame_image.columnconfigure(0, weight=1)

        # image_logo
        self.img_logo = ImageTk.PhotoImage(Image.open("novo_logo.png"))
        self.l_img_sensor_2 = Label(self.frame_image, image=self.img_logo, bg="#f0f0f0")
        self.l_img_sensor_2.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)

        # frame_temperature
        self.frame_temperature = Frame(self.frame_row_top, bg="white", highlightthickness=2,
                                       highlightbackground='#e6e6e6')
        self.frame_temperature.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_temperature.columnconfigure(0, weight=1)
        self.frame_temperature.columnconfigure(1, weight=2)
        self.frame_temperature.rowconfigure(0, weight=1)

        # frame_temperature_image
        self.frame_temperature_image = Frame(self.frame_temperature, bg='white')
        self.frame_temperature_image.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.image_temperature = Image.open("temperature.png")
        self.image_resize = self.image_temperature.resize((int(self.root.winfo_screenwidth()/14), int(self.root.winfo_screenwidth()/14)),Image.ANTIALIAS)
        self.temperature_img = ImageTk.PhotoImage(self.image_resize)
        self.lbl_temp = Label(self.frame_temperature_image, image=self.temperature_img, bg='white')
        self.lbl_temp.temperature_img = self.temperature_img
        self.lbl_temp.place(relx=0.5, rely=0.5, anchor='center')

        # frame_temperature_text
        self.frame_temperature_text = Frame(self.frame_temperature, bg="white")
        self.frame_temperature_text.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.lbl_temp_title = Label(self.frame_temperature_text, text='Temperature', bg='white', fg='#6e6e6e')
        self.lbl_temp_title.config(font=('Monoton', int(self.root.winfo_screenwidth() / 100)))
        self.lbl_temp_title.place(relx=0.5, rely=0.1, anchor='n')
        self.lbl_temp_value = Label(self.frame_temperature_text, text='--', bg='white', fg='#474747')
        self.lbl_temp_value.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 50), 'bold'))
        self.lbl_temp_value.place(relx=0.5, rely=0.6, anchor='center')

        # frame_humidity
        self.frame_humidity = Frame(self.frame_row_top, bg="white", highlightthickness=2, highlightbackground='#e6e6e6')
        self.frame_humidity.grid(column=2, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_humidity.columnconfigure(0, weight=1)
        self.frame_humidity.columnconfigure(1, weight=1)
        self.frame_humidity.rowconfigure(0, weight=1)
        
        
        # frame_humidity2

        
       

        # frame_humidity_image
        self.frame_humidity_image = Frame(self.frame_humidity, bg='white')
        self.frame_humidity_image.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.image_humidity = Image.open("humidity.png")
        self.image_humidity_resize = self.image_humidity.resize((int(self.root.winfo_screenwidth()/14), int(self.root.winfo_screenwidth()/14)),Image.ANTIALIAS)
        self.humidity_img = ImageTk.PhotoImage(self.image_humidity_resize)
        self.lbl_hum = Label(self.frame_humidity_image, image=self.humidity_img, bg='white')
        self.lbl_hum.humidity_img = self.humidity_img
        self.lbl_hum.place(relx=0.5, rely=0.5, anchor='center')

        # frame_humidity_text
        self.frame_humidity_text = Frame(self.frame_humidity, bg='white')
        self.frame_humidity_text.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.lbl_hum_title = Label(self.frame_humidity_text, text='Humidity', bg='white', fg='#6e6e6e')
        self.lbl_hum_title.config(font=('Monoton', int(self.root.winfo_screenwidth() / 100)))
        self.lbl_hum_title.place(relx=0.5, rely=0.1, anchor='n')
        self.lbl_hum_value = Label(self.frame_humidity_text, text='--', bg='white', fg="#474747")
        self.lbl_hum_value.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 50), 'bold'))
        self.lbl_hum_value.place(relx=0.5, rely=0.6, anchor='center')
        
        # frame_co
        self.frame_co = Frame(self.frame_row_bottom, bg="white", highlightthickness=2,
                                       highlightbackground='#e6e6e6')
        self.frame_co.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_co.columnconfigure(0, weight=1)
        self.frame_co.columnconfigure(1, weight=1)
        self.frame_co.rowconfigure(0, weight=1)
        # frame_co_image
        self.frame_co_image = Frame(self.frame_co, bg='white')
        self.frame_co_image.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.image_co = Image.open("co2.png")
        self.image_co_resize = self.image_co.resize((int(self.root.winfo_screenwidth()/14), int(self.root.winfo_screenwidth()/14)),Image.ANTIALIAS)
        self.co_img = ImageTk.PhotoImage(self.image_co_resize)
        self.lbl_co = Label(self.frame_co_image, image=self.co_img, bg='white')
        self.lbl_co.co_img = self.co_img
        self.lbl_co.place(relx=0.5, rely=0.5, anchor='center')
        # frame_co_text
        self.frame_co_text = Frame(self.frame_co, bg="white")
        self.frame_co_text.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.lbl_co_title = Label(self.frame_co_text, text='CO2', bg='white', fg='#6e6e6e')
        self.lbl_co_title.config(font=('Monoton', int(self.root.winfo_screenwidth() / 100)))
        self.lbl_co_title.place(relx=0.5, rely=0.1, anchor='n')
        self.lbl_co_value = Label(self.frame_co_text, text='--', bg='white', fg='#474747')
        self.lbl_co_value.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 110), 'bold'))
        self.lbl_co_value.place(relx=0.5, rely=0.6, anchor='center')
        
        
        self.frame_light = Frame(self.frame_row_bottom, bg="white", highlightthickness=2,
                                       highlightbackground='#e6e6e6')
        self.frame_light.grid(column=2, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_light.columnconfigure(0, weight=1)
        self.frame_light.columnconfigure(1, weight=2)
        self.frame_light.rowconfigure(0, weight=1)
        # frame_light_image
        self.frame_light_image = Frame(self.frame_light, bg='white')
        self.frame_light_image.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.image_light = Image.open("light.png")
        self.image_light_resize = self.image_light.resize((int(self.root.winfo_screenwidth()/20), int(self.root.winfo_screenwidth()/14)),Image.ANTIALIAS)
        self.light_img = ImageTk.PhotoImage(self.image_light_resize)
        self.lbl_light = Label(self.frame_light_image, image=self.light_img, bg='white')
        self.lbl_light.light_img = self.light_img
        self.lbl_light.place(relx=0.5, rely=0.5, anchor='center')
        # frame_light_text
        self.frame_light_text = Frame(self.frame_light, bg="white")
        self.frame_light_text.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.lbl_light_title = Label(self.frame_light_text, text='Light', bg='white', fg='#6e6e6e')
        self.lbl_light_title.config(font=('Monoton', int(self.root.winfo_screenwidth() / 100)))
        self.lbl_light_title.place(relx=0.5, rely=0.1, anchor='n')
        self.lbl_light_value = Label(self.frame_light_text, text='--', bg='white', fg='#474747')
        self.lbl_light_value.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 110), 'bold'))
        self.lbl_light_value.place(relx=0.5, rely=0.6, anchor='center')
        

        # frame_time
        self.frame_time = Frame(self.frame_row_top, bg="white", highlightthickness=2, highlightbackground='#e6e6e6')
        self.frame_time.grid(column=3, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_time.columnconfigure(0, weight=1)
        self.frame_time.columnconfigure(1, weight=1)
        self.frame_time.rowconfigure(0, weight=1)

        # frame_time_image
        self.frame_time_image = Frame(self.frame_time, bg='white')
        self.frame_time_image.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.image_time = Image.open("time.png")
        self.image_time_resize = self.image_time.resize((int(self.root.winfo_screenwidth()/14), int(self.root.winfo_screenwidth()/14)),Image.ANTIALIAS)
        self.time_img = ImageTk.PhotoImage(self.image_time_resize)
        self.lbl_time = Label(self.frame_time_image, image=self.time_img, bg='white')
        self.lbl_time.time_img = self.time_img
        self.lbl_time.place(relx=0.5, rely=0.5, anchor='center')

        # frame_time_text
        self.frame_time_text = Frame(self.frame_time, bg='white')
        self.frame_time_text.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.lbl_time_title = Label(self.frame_time_text, text='Time', bg='white', fg='#6e6e6e')
        self.lbl_time_title.config(font=('Monoton', int(self.root.winfo_screenwidth() / 100)))
        self.lbl_time_title.place(relx=0.5, rely=0.1, anchor='n')
        self.lbl_time_value = Label(self.frame_time_text, text="", bg='white', fg="#474747")
        self.lbl_time_value.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 80), 'bold'))
        self.lbl_time_value.place(relx=0.5, rely=0.6, anchor='center')

        
        # frame_sensor1
        self.frame_sensor1 = Frame(self.frame_row_bottom, bg="white", highlightthickness=2,
                                   highlightbackground='#e6e6e6')
        self.frame_sensor1.grid(column=3, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_sensor1.rowconfigure(0, weight=1)
        self.frame_sensor1.rowconfigure(1, weight=1)
        self.frame_sensor1.rowconfigure(2, weight=2)
        self.frame_sensor1.rowconfigure(3, weight=1)
        self.frame_sensor1.columnconfigure(0, weight=1)

        # label_info_1
        self.label_info_1 = Label(self.frame_sensor1, text=str("Sensor 1"), bg="white", fg='#6e6e6e')
        self.label_info_1.config(font=('Monoton', int(self.root.winfo_screenwidth() / 90)))
        self.label_info_1.grid(column=0, row=0, stick=NE, padx=25, pady=10)

        # image_sensor1
        self.image_sensor_1 = Image.open("unknown.png")
        self.image_sensor_1_resize = self.image_sensor_1.resize((int(self.root.winfo_screenwidth()/6), int(self.root.winfo_screenwidth()/6)),Image.ANTIALIAS)
        self.sensor_1_img = ImageTk.PhotoImage(self.image_sensor_1_resize)
        self.l_img_sensor_1 = Label(self.frame_sensor1, image=self.sensor_1_img, bg="white")
        self.l_img_sensor_1.grid(column=0, row=1, stick=(N + S + E + W), padx=5, pady=5)
        # self.l_img_sensor_1.place(relx=0.5, rely=0.8, anchor='center')

        # label_status_1
        self.label_status_1 = Label(self.frame_sensor1, text=str("Unknown Status"), bg="white", fg='#474747')
        self.label_status_1.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 60)))
        self.label_status_1.grid(column=0, row=2, stick=(N + S + E + W), padx=5, pady=5)
        self.label_status_1.place(relx=0.5, rely=0.8, anchor='center')

        # frame_sensor1_battery
        self.frame_sensor1_battery = Frame(self.frame_sensor1, bg='white')
        self.frame_sensor1_battery.grid(column=0, row=3, stick=(N + S + E + W))
        self.lbl_s1_batt = Label(self.frame_sensor1_battery, text='-', bg='white', fg='#6e6e6e')
        self.lbl_s1_batt.config(font=('Monoton', int(self.root.winfo_screenwidth() / 120)))
        self.lbl_s1_batt.place(relx=0.5, rely=0.5, anchor='center')

        # frame_sensor2
        self.frame_sensor2 = Frame(self.frame_row_bottom, bg="white", highlightthickness=2,
                                   highlightbackground='#e6e6e6')
        self.frame_sensor2.grid(column=4, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_sensor2.rowconfigure(0, weight=1)
        self.frame_sensor2.rowconfigure(1, weight=1)
        self.frame_sensor2.rowconfigure(2, weight=2)
        self.frame_sensor2.rowconfigure(3, weight=1)
        self.frame_sensor2.columnconfigure(0, weight=1)

        # label_info_2
        self.label_info_2 = Label(self.frame_sensor2, text=str("Sensor 2"), bg="white", fg='#6e6e6e')
        self.label_info_2.config(font=('Monoton', int(self.root.winfo_screenwidth() / 90)))
        self.label_info_2.grid(column=0, row=0, stick=NE, padx=25, pady=10)

        # image_sensor2
        self.image_sensor_2 = Image.open("unknown.png")
        self.image_sensor_2_resize = self.image_sensor_2.resize((int(self.root.winfo_screenwidth()/6), int(self.root.winfo_screenwidth()/6)),Image.ANTIALIAS)
        self.sensor_2_img = ImageTk.PhotoImage(self.image_sensor_2_resize)
        self.l_img_sensor_2 = Label(self.frame_sensor2, image=self.sensor_1_img, bg="white")
        self.l_img_sensor_2.grid(column=0, row=1, stick=(N + S + E + W), padx=5, pady=5)

        # label_status_2
        self.label_status_2 = Label(self.frame_sensor2, text=str("Unknown Status"), bg="white", fg='#474747')
        self.label_status_2.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 60)))
        self.label_status_2.grid(column=0, row=2, stick=(N + S + E + W), padx=5, pady=5)
        self.label_status_2.place(relx=0.5, rely=0.8, anchor='center')

        # frame_sensor2_battery
        self.frame_sensor2_battery = Frame(self.frame_sensor2, bg='white')
        self.frame_sensor2_battery.grid(column=0, row=3, stick=(N + S + E + W))
        self.lbl_s2_batt = Label(self.frame_sensor2_battery, text='-', bg='white', fg='#6e6e6e')
        self.lbl_s2_batt.config(font=('Monoton', int(self.root.winfo_screenwidth() / 120)))
        self.lbl_s2_batt.place(relx=0.5, rely=0.5, anchor='center')        
        


        
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.thread_sensor_1 = threading.Thread(target=thread_sensor_1,
                                                  args=(self.l_img_sensor_1, self.label_status_1, self.root))
        
        
        self.thread_sensor_1.daemon = True
        self.thread_sensor_1.start()

        self.thread_sensor_2 = threading.Thread(target=thread_sensor_2,
                                                args=(self.l_img_sensor_2, self.label_status_2, self.root))
        self.thread_sensor_2.daemon = True
        self.thread_sensor_2.start()

        self.thread_battery_1 = threading.Thread(target=thread_battery_1,
                                                 args=(self.lbl_s1_batt,))
        self.thread_battery_1.daemon = True
        self.thread_battery_1.start()

        self.thread_battery_2 = threading.Thread(target=thread_battery_2,
                                                 args=(self.lbl_s2_batt,))
        self.thread_battery_2.daemon = True
        self.thread_battery_2.start()
        
        self.thread_env = threading.Thread(target=thread_env,args=(self.lbl_temp_value, self.lbl_hum_value,self.lbl_co_value,self.lbl_light_value))
        self.thread_env.daemon = True
        self.thread_env.start()

        self.thread_time = threading.Thread(target=thread_time,
                                           args=(self.lbl_time_value,))
        self.thread_time.daemon = True
        self.thread_time.start()

        self.thread_mqtt = threading.Thread(target=init_mqtt, )
        self.thread_mqtt.daemon = True
        self.thread_mqtt.start()

    def on_closing(self):
        global end
        print("By dev")
        end = True
        self.thread_mqtt.join(0.1)
        self.thread_sensor_1.join(0.1)
        self.thread_sensor_2.join(0.1)
        self.thread_sensor_3.join(0.1)
        self.master.destroy()


def thread_sensor_1(image, status, root):
    global i
    global end
    global sensor1
    lasted_value = ""
    publish.single("sensor/topic", "get_battery/sensor1", hostname="127.0.0.1")
    publish.single("sensor/topic", "get_battery/sensor2", hostname="127.0.0.1")
    publish.single("sensor/topic", "get_battery/sensor3", hostname="127.0.0.1")
    width = int(root.winfo_screenwidth()/6)
    print(width)
    while True:
        time.sleep(0.1)
        value = json.loads(sensor1)
        if "Postura" in value[0]:
            if value[0]['Postura'] == "correcta":
                if value[0]['Postura'] != lasted_value:
                    image_sensor_1 = Image.open("ok.png")
                    image_sensor_1_resize = image_sensor_1.resize((width, width), Image.ANTIALIAS)
                    sensor_1_img = ImageTk.PhotoImage(image_sensor_1_resize)
                    image.config(image=sensor_1_img)
                    status.config(text="Correct Position!", fg="#6eb171")
                    publish.single("sensor/topic", "end_vibration/sensor1", hostname="127.0.0.1")
            elif value[0]['Postura'] == "incorrecta":
                if value[0]['Postura'] != lasted_value:
                    image_sensor_1 = Image.open("cancel.png")
                    image_sensor_1_resize = image_sensor_1.resize((width, width), Image.ANTIALIAS)
                    sensor_1_img = ImageTk.PhotoImage(image_sensor_1_resize)
                    image.config(image=sensor_1_img)
                    status.config(text="Please adjust your position", fg="#d16d6a")
                    publish.single("sensor/topic", "start_vibration/sensor1", hostname="127.0.0.1")
            else:
                if value[0]['Postura'] != lasted_value:
                    image_sensor_1 = Image.open("unknown.png")
                    image_sensor_1_resize = image_sensor_1.resize((width, width), Image.ANTIALIAS)
                    sensor_1_img = ImageTk.PhotoImage(image_sensor_1_resize)
                    image.config(image=sensor_1_img)
                    status.config(text="Unknown Status", fg="#474747")
            lasted_value = value[0]['Postura']
        if end is True:
            break


def thread_sensor_2(image, status, root):
    global i
    global end
    global sensor1
    lasted_value = ""
    width = int(root.winfo_screenwidth()/6)
    while True:
        time.sleep(0.1)
        value = json.loads(sensor2)
        if "Postura" in value[0]:
            if value[0]['Postura'] == "correcta":
                if value[0]['Postura'] != lasted_value:
                    image_sensor_2 = Image.open("ok.png")
                    image_sensor_2_resize = image_sensor_2.resize((width, width), Image.ANTIALIAS)
                    sensor_2_img = ImageTk.PhotoImage(image_sensor_2_resize)
                    image.config(image=sensor_2_img)
                    status.config(text="Correct Position!", fg="#6eb171")
                    publish.single("sensor/topic", "end_vibration/sensor3", hostname="127.0.0.1")
            elif value[0]['Postura'] == "incorrecta":
                if value[0]['Postura'] != lasted_value:
                    image_sensor_2 = Image.open("cancel.png")
                    image_sensor_2_resize = image_sensor_2.resize((width, width), Image.ANTIALIAS)
                    sensor_2_img = ImageTk.PhotoImage(image_sensor_2_resize)
                    image.config(image=sensor_2_img)
                    status.config(text="Please adjust your position", fg="#d16d6a")
                    publish.single("sensor/topic", "start_vibration/sensor3", hostname="127.0.0.1")
            else:
                if value[0]['Postura'] != lasted_value:
                    image_sensor_2 = Image.open("unknown.png")
                    image_sensor_2_resize = image_sensor_2.resize((width, width), Image.ANTIALIAS)
                    sensor_2_img = ImageTk.PhotoImage(image_sensor_2_resize)
                    image.config(image=sensor_2_img)
                    status.config(text="Unknown Status", fg="#474747")
            lasted_value = value[0]['Postura']
        if end is True:
            break


def thread_battery_1(label):
    global i
    global end
    global battery1
    while True:
        time.sleep(0.1)
        value = json.loads(battery1)
        if "battery_level" in value:
            label.config(text=("Battery Level: " + value['battery_level'] + "%"))
        if end is True:
            break


def thread_battery_2(label):
    global i
    global end
    global battery2
    while True:
        time.sleep(0.1)
        value = json.loads(battery2)
        if "battery_level" in value:
            label.config(text=("Battery Level: " + value['battery_level'] + "%"))
        if end is True:
            break


def thread_env(label_temperature, label_humidity,label_co2,label_light):
    global i
    global end
    global env
    while True:
        time.sleep(0.1)
        value = json.loads(env)
        if "Temperature" in value:
            label_temperature.config(text=(value['Temperature'] + "°"))
            label_humidity.config(text=(value['Humidity'] + "%"))
            label_co2.config(text=(value['Co2'] + "ppm"))
            label_co2.config(text=(value['Co2'] + "ppm"))
            label_light.config(text=(value['Light'] + "lux"))
        if end is True:
            break


def thread_time(label_time):
    while True:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d\n%H:%M:%S")
        label_time.config(text=current_time)
        time.sleep(1)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sensor/sensorS1S2/")
    client.subscribe("sensor/sensor2/")
    client.subscribe("sensor/sensorS3S4/")
    client.subscribe("sensor/sensor4/")
    client.subscribe("sensor/sensorS5S6/")
    client.subscribe("sensor/sensor6/")

    client.subscribe("sensor/battery_sensor1/")
    client.subscribe("sensor/battery_sensor2/")
    client.subscribe("sensor/battery_sensor3/")
    client.subscribe("sensor/battery_sensor4/")
    client.subscribe("sensor/battery_sensor5/")
    client.subscribe("sensor/battery_sensor6/")
    client.subscribe("sensor/env/")
    client.subscribe("sensor/get_mongo_info/")


def on_message(client, userdata, msg):
    global tx
    global sensor1
    global sensor2
    global sensor3
    global battery1
    global battery2
    global battery3
    global env
    if msg.topic == "sensor/sensorS1S2/":
        sensor1 = msg.payload.decode("utf-8")
        print(msg.payload.decode("utf-8"))
    elif msg.topic == "sensor/sensorS3S4/":
        sensor2 = msg.payload.decode("utf-8")
        print(msg.payload.decode("utf-8"))
    elif msg.topic == "sensor/sensorS5S6/":
        sensor3 = msg.payload.decode("utf-8")
        print(msg.payload.decode("utf-8"))
    elif msg.topic == "sensor/battery_sensor1/":
        battery1 = msg.payload.decode("utf-8")
        print(msg.payload.decode("utf-8"))
    elif msg.topic == "sensor/battery_sensor3/":
        battery2 = msg.payload.decode("utf-8")
        print(msg.payload.decode("utf-8"))
    elif msg.topic == "sensor/battery_sensor5/":
        battery3 = msg.payload.decode("utf-8")
        print(msg.payload.decode("utf-8"))
    elif msg.topic == "sensor/env/":
        env = msg.payload.decode("utf-8")
        print(msg.payload.decode("utf-8"))


def init_mqtt():
    # Create an MQTT client and attach our routines to it.
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1", 1883, 60)
    client.loop_forever()
    

def thread_reload(root):
    while True:
    	#root.update_idletasks()
    	print("Run reconnect")
    	publish.single("sensor/topic", "connect/sensor1", hostname="127.0.0.1")
    	publish.single("sensor/topic", "connect/sensor2", hostname="127.0.0.1")
    	publish.single("sensor/topic", "connect/sensor3", hostname="127.0.0.1")
    	publish.single("sensor/topic", "connect/sensor4", hostname="127.0.0.1")
    	publish.single("sensor/topic", "connect/sensor5", hostname="127.0.0.1")
    	publish.single("sensor/topic", "connect/sensor6", hostname="127.0.0.1")
    	time.sleep(10)
    	

if __name__ == "__main__":
    root = Tk()
    threading.Thread(target=thread_reload, args=(root, )).start()
    View(root)
    root.mainloop()
