import time
import tkinter
from tkinter import *
from PIL import ImageTk, Image
from datetime import datetime


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
        self.root.rowconfigure(1, weight=3)
        self.root.rowconfigure(2, weight=3)

        # frame_row_top
        self.frame_row_top = Frame(self.root, bg="#f0f0f0")
        self.frame_row_top.grid(column=0, row=0, stick=(N + S + E + W), padx=20, pady=5)
        self.frame_row_top.columnconfigure(0, weight=1)
        self.frame_row_top.columnconfigure(1, weight=2)
        self.frame_row_top.rowconfigure(0, weight=1)

        # frame_image
        self.frame_image = Frame(self.frame_row_top, bg="#f0f0f0")
        self.frame_image.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_image.columnconfigure(0, weight=1)
        self.frame_image.rowconfigure(0, weight=1)

        # image_logo
        self.img_logo = ImageTk.PhotoImage(Image.open("logo1.PNG"))
        self.l_img_sensor_2 = Label(self.frame_image, image=self.img_logo, bg="#f0f0f0")
        self.l_img_sensor_2.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)

        # frame_time
        self.frame_time = Frame(self.frame_row_top, bg="white", highlightthickness=2, highlightbackground='#e6e6e6')
        self.frame_time.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_time.columnconfigure(0, weight=1)
        self.frame_time.columnconfigure(1, weight=2)
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
        self.lbl_time_value.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 50), 'bold'))
        self.lbl_time_value.place(relx=0.5, rely=0.6, anchor='center')

        # frame_second_row
        self.frame_second_row = Frame(root, bg="#f0f0f0")
        self.frame_second_row.grid(column=0, row=1, stick=(N + S + E + W), padx=20, pady=5)
        self.frame_second_row.columnconfigure(0, weight=1)
        self.frame_second_row.columnconfigure(1, weight=1)
        self.frame_second_row.rowconfigure(0, weight=1)

         # frame_temperature
        self.frame_temperature = Frame(self.frame_second_row, bg="white", highlightthickness=2,
                                       highlightbackground='#e6e6e6')
        self.frame_temperature.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_temperature.columnconfigure(0, weight=1)
        self.frame_temperature.columnconfigure(1,weight=2)
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
        self.frame_humidity = Frame(self.frame_second_row, bg="white", highlightthickness=2, highlightbackground='#e6e6e6')
        self.frame_humidity.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_humidity.columnconfigure(0, weight=1)
        self.frame_humidity.columnconfigure(1, weight=2)
        self.frame_humidity.rowconfigure(0, weight=1)

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


        # frame_third_row
        self.frame_third_row = Frame(self.root, bg="#f0f0f0")
        self.frame_third_row.grid(column=0, row=2, stick=(N + S + E + W), padx=20, pady=5)
        self.frame_third_row.columnconfigure(0, weight=1)
        self.frame_third_row.columnconfigure(1, weight=1)
        self.frame_third_row.rowconfigure(0, weight=1)

        # frame_co
        self.frame_co = Frame(self.frame_third_row, bg="white", highlightthickness=2,
                                       highlightbackground='#e6e6e6')
        self.frame_co.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_co.columnconfigure(0, weight=1)
        self.frame_co.columnconfigure(1, weight=2)
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
        self.lbl_co_value.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 50), 'bold'))
        self.lbl_co_value.place(relx=0.5, rely=0.6, anchor='center')

        # frame_light
        self.frame_light = Frame(self.frame_third_row, bg="white", highlightthickness=2,
                                       highlightbackground='#e6e6e6')
        self.frame_light.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_light.columnconfigure(0, weight=1)
        self.frame_light.columnconfigure(1, weight=2)
        self.frame_light.rowconfigure(0, weight=1)

        # frame_light_image
        self.frame_light_image = Frame(self.frame_light, bg='white')
        self.frame_light_image.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.image_light = Image.open("light.png")
        self.image_light_resize = self.image_light.resize((int(self.root.winfo_screenwidth()/14), int(self.root.winfo_screenwidth()/14)),Image.ANTIALIAS)
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
        self.lbl_light_value.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 50), 'bold'))
        self.lbl_light_value.place(relx=0.5, rely=0.6, anchor='center')

    


        
        """
        self.frame_sensor1 = Frame(self.frame_row_bottom, bg="white", highlightthickness=2,
                                   highlightbackground='#e6e6e6')
        self.frame_sensor1.grid(column=0, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_sensor1.rowconfigure(0, weight=1)
        self.frame_sensor1.rowconfigure(1, weight=1)
        self.frame_sensor1.rowconfigure(2, weight=2)
        self.frame_sensor1.rowconfigure(3, weight=1)
        self.frame_sensor1.columnconfigure(0, weight=1)
        
        

        # label_info_1
        self.label_info_1 = Label(self.frame_sensor1, text=str("Conjunto 1"), bg="white", fg='#6e6e6e')
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
        self.label_status_1 = Label(self.frame_sensor1, text=str("Status desconhecido"), bg="white", fg='#474747')
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
        self.frame_sensor2.grid(column=1, row=0, stick=(N + S + E + W), padx=5, pady=5)
        self.frame_sensor2.rowconfigure(0, weight=1)
        self.frame_sensor2.rowconfigure(1, weight=1)
        self.frame_sensor2.rowconfigure(2, weight=2)
        self.frame_sensor2.rowconfigure(3, weight=1)
        self.frame_sensor2.columnconfigure(0, weight=1)

        # label_info_2
        self.label_info_2 = Label(self.frame_sensor2, text=str("Conjunto 2"), bg="white", fg='#6e6e6e')
        self.label_info_2.config(font=('Monoton', int(self.root.winfo_screenwidth() / 90)))
        self.label_info_2.grid(column=0, row=0, stick=NE, padx=25, pady=10)

        # image_sensor2
        self.image_sensor_2 = Image.open("unknown.png")
        self.image_sensor_2_resize = self.image_sensor_2.resize((int(self.root.winfo_screenwidth()/6), int(self.root.winfo_screenwidth()/6)),Image.ANTIALIAS)
        self.sensor_2_img = ImageTk.PhotoImage(self.image_sensor_2_resize)
        #self.l_img_sensor_2 = Label(self.frame_sensor2, image=self.sensor_1_img, bg="white")
        self.l_img_sensor_2.grid(column=0, row=1, stick=(N + S + E + W), padx=5, pady=5)

        # label_status_2
        self.label_status_2 = Label(self.frame_sensor2, text=str("Status desconhecido"), bg="white", fg='#474747')
        self.label_status_2.config(font=('Tahoma', int(self.root.winfo_screenwidth() / 60)))
        self.label_status_2.grid(column=0, row=2, stick=(N + S + E + W), padx=5, pady=5)
        self.label_status_2.place(relx=0.5, rely=0.8, anchor='center')

        # frame_sensor2_battery
        self.frame_sensor2_battery = Frame(self.frame_sensor2, bg='white')
        self.frame_sensor2_battery.grid(column=0, row=3, stick=(N + S + E + W))
        self.lbl_s2_batt = Label(self.frame_sensor2_battery, text='-', bg='white', fg='#6e6e6e')
        self.lbl_s2_batt.config(font=('Monoton', int(self.root.winfo_screenwidth() / 120)))
        self.lbl_s2_batt.place(relx=0.5, rely=0.5, anchor='center')
        
        """       
        """
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        
        

        self.thread_battery_1 = threading.Thread(target=thread_battery_1,
                                                 args=(self.lbl_s1_batt,))
        self.thread_battery_1.daemon = True
        self.thread_battery_1.start()

        self.thread_battery_2 = threading.Thread(target=thread_battery_2,
                                                 args=(self.lbl_s2_batt,))
        self.thread_battery_2.daemon = True
        self.thread_battery_2.start()
        
        """
        




    #width = int(root.winfo_screenwidth()/6)
    #print(width)
    	

if __name__ == "__main__":
    root = Tk()
    View(root)
    root.mainloop()
