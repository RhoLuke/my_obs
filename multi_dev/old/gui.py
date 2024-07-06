import customtkinter as ctk
import time
from threading import Thread
import _thread as th
import sys
import logging
from os import kill, getpid
from signal import SIGKILL

import app
import log
import switchdevice
import weatherdevice
import ror_device
import watcher

class Footer(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        
        self.grid(row=3, padx=8, pady=5, sticky='sw')
        self.grid_columnconfigure(0, weight=1)
        self.label = ctk.CTkLabel(self, text='footer')
        self.label.grid(row=0, padx=10, pady=10)
        self.configure(fg_color="transparent")
        
    def update_time(self):
        self.label.configure(text=time.strftime('%d-%m-%YT%H:%M:%S', time.localtime()))
        self.master.after(1000, self.update_time)

class SwitchFrame(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        self.swt = switchdevice.SwitchDevice(self.master.logger)
        self.swt.connected = True
        
        self.grid(row=0,
                  padx=10,
                  pady=10,
                  sticky="n")
        self.grid_columnconfigure(0, weight=1)
        
        self.label = ctk.CTkLabel(self,
            text='RELAY BOARD',
            font=('roboto', 22))
        self.label.grid(row=0,
                        sticky='n',
                        padx=5,
                        pady=8)
        
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=1, sticky='n')
        self.buttons_frame.configure(fg_color='transparent')
        self.connected_color_button = '#1cd122'
        self.disconnected_color_button = '#e86343'

    def generate_buttons(self):
        self.buttons = dict()
        for idx in range(self.swt.__class__._maxswitch):
            name = self.swt.get_switchname(idx)
            self.buttons[name] = [idx, False, ctk.CTkButton(self.buttons_frame, text=name)]
            self.buttons[name][2].configure(command=lambda x = self.buttons[name][2].cget("text"):self.callback(x))
            self.buttons[name][2].configure(
                width=90,
                height=40,
                fg_color=self.disconnected_color_button,
                font=('roboto', 20))
            self.buttons[name][2].grid(row=1,
                              column=idx,
                              padx=5,
                              pady=5,
                              sticky='e')
    
    def callback(self, name):    
        if self.buttons[name][1]:
            self.buttons[name][1] = False
            self.buttons[name][2].configure(fg_color=self.disconnected_color_button)
        else:
            self.buttons[name][1] = True
            self.buttons[name][2].configure(fg_color=self.connected_color_button)
        
        for key, val in self.swt.__class__._switch.items():
            if name in val['Name']:
                self.swt.set_switch(key, self.buttons[name][1])
    
    def update_buttons(self):
        for key, val in self.swt.__class__._switch.items():
            if self.buttons[val['Name']] == val['State']:
                continue
            elif val['State']:
                self.buttons[val['Name']][2].configure(fg_color=self.connected_color_button)
            else:
                self.buttons[val['Name']][2].configure(fg_color=self.disconnected_color_button)
                
        self.master.after(100, self.update_buttons)

class WeatherFrame(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        
        self.grid(row=0,
                  padx=3,
                  pady=5,
                  sticky="w")
        
        self.label = ctk.CTkLabel(self,
            text='WEATHER CONDITIONS',
            font=('roboto', 20))
        self.label.grid(row=0,
                        sticky='n',
                        padx=5,
                        pady=8)
        
        self.wth = weatherdevice.WeatherDevice(self.master.logger)
        self.wth.start()
        
        self.sensor_labels = dict()
        self.sensor_values = dict()
        
        self.is_safe_color = '#1cd122'
        self.is_not_safe_color = '#e86343'
        
        self.safety_monitor = ctk.CTkLabel(self, text='Safe',font=('roboto', 18), padx=3, pady=3, fg_color=self.is_safe_color)
        self.safety_monitor.grid(row=0, column=1, padx=3, pady=8, sticky='n')
        
    def generate_labels(self):
        for idx, sensor in enumerate(self.wth.__class__._sensors.keys()):
            self.sensor_labels[sensor] = ctk.CTkLabel(self, text=f'{sensor}: ', font=('roboto', 18))
            self.sensor_labels[sensor].grid(row=idx+1, column=0, sticky='nw', padx=3, pady=3)
            
            self.sensor_values[sensor] = ctk.CTkLabel(self, text=str(0.0), font=('roboto', 18))
            self.sensor_values[sensor].grid(row=idx+1, column=1, sticky='nw', padx=3, pady=3)
            
    def update_values(self):
        for sensor in self.wth.__class__._sensors.keys():
            self.sensor_values[sensor].configure(text=f"{self.wth.__class__._sensors[sensor]['Value']:.2f}")
            
            if sensor == 'RainRate':
                if self.wth.__class__._sensors[sensor]['Value']:
                    self.safety_monitor.configure(text='Not Safe', fg_color=self.is_not_safe_color)
                else:
                    self.safety_monitor.configure(text='Safe', fg_color=self.is_safe_color)
                
                
        self.master.after(int(self.wth.__class__._avperiod*1e+3), self.update_values)

class Watcher(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        
        self.wat = watcher.Watcher(self.master.logger)
        self.grid(row=0,
                  padx=3,
                  pady=5,
                  sticky="n")
        self.text_button = "Watcher Inactive"
        self.button = ctk.CTkButton(self, text=self.text_button, command=lambda: Thread().start())
        self.label = ctk.CTkLabel()
        #da finire qua
        
    
class RoRFrame(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        
        self.ror = ror_device.ROOF(self.master.logger, master=True)
        self.ror.check_sensor()
        
        for sensor in ['close1', 'close2', 'open1', 'open2']:
            state = self.ror.read_sensor(sensor)
            if state == 'active':
                if sensor == 'close1':
                    self.init_state = 'CLOSE'
                elif sensor == 'open1':
                    self.init_state = 'OPEN'
                elif sensor == 'close2':
                    self.init_state = 'CLOSING'
                elif sensor == 'open2':
                    self.init_state = 'OPENING'
                break
            else:
                self.init_state = 'UNKNOWN'
                
                    
        self.grid(row=0,
                  padx=3,
                  pady=5,
                  sticky="e")
        
        self.label = ctk.CTkLabel(self,
            text='ROR PANEL',
            font=('roboto', 20))
        self.label.grid(row=0,
                        sticky='ne',
                        padx=5,
                        pady=8)
    
        
        self.state_label = ctk.CTkLabel(self,
            text=f'State: {self.init_state}',
            font=('roboto', 18))
        self.state_label.grid(row=1, column=0,
                        sticky='w',
                        padx=5,
                        pady=8)
        
        self.buttons = {
            'OPEN': ctk.CTkButton(self, text='OPEN', command=lambda: Thread(target=self.ror.move_roof, name='open_roof', kwargs={"direction": True}).start()),
            'CLOSE': ctk.CTkButton(self, text='CLOSE', command=lambda: Thread(target=self.ror.move_roof, name='close_roof', kwargs={"direction": False}).start()),
            'ABORT': ctk.CTkButton(self, text='ABORT', command=lambda: Thread(target=self.ror.abort, name='abort_movement').start())
            }
        
#         self.buttons = {
#             'OPEN': ctk.CTkButton(self, text='OPEN', command=lambda: self.ror.move_roof(True)),
#             'CLOSE': ctk.CTkButton(self, text='CLOSE', command=lambda: self.ror.move_roof(False)),
#             'ABORT': ctk.CTkButton(self, text='ABORT', command=lambda: self.ror.abort())
#             }
        
    def generate_buttons(self):
        for idx, val in enumerate(self.buttons.values()):
            val.grid(row=2, column=idx, sticky='w', padx=5, pady=3)
            
    def update_state(self):
        state = self.ror.__class__._state
        if state == 0:
            self.state_label.configure(text=f'State: OPEN')
        elif state == 1:
            self.state_label.configure(text=f'State: CLOSED')
        elif state == 2:
            self.state_label.configure(text=f'State: OPENING')
        elif state == 3:
            self.state_label.configure(text=f'State: CLOSING')
        
        self.master.after(500, self.update_state)

class LogFrame(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        
        self.grid(row=2, sticky='we')
        
        self.label = ctk.CTkLabel(self, text='LOG:', font=('roboto', 20))
        self.label.grid(row=0, sticky='nw', padx=5, pady=3)
        
        self.text_log = ctk.CTkTextbox(self, border_width=3.0, width=800, activate_scrollbars=True)
        self.text_log.grid(row=1, padx=5, pady=5, sticky='we')
        self.text_log.grid_columnconfigure(0, weight=1)
    
    def write(self, text):
        self.text_log.insert('end', text)
        
    
class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.logger = log.init_logging()
        log.logger = self.logger
        stream_log = logging.StreamHandler(stream=LogFrame(self))
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(message)s', '%Y-%m-%dT%H:%M:%S')
        formatter.converter = time.gmtime           # UTC time
        stream_log.setFormatter(formatter)
        
        self.logger.addHandler(stream_log)
        self.version = 0.1
        self.title(f"MyObs GUI v.{self.version}")
        self.geometry("900x800")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.footer = Footer(self)
        self.footer.update_time()
        
        self.swt_frame = SwitchFrame(self)
        self.swt_frame.generate_buttons()
        self.swt_frame.update_buttons()
        
        self.wth_frame = WeatherFrame(self)
        self.wth_frame.generate_labels()
        self.wth_frame.update_values()
        
        self.ror_frame = RoRFrame(self)
        self.ror_frame.generate_buttons()
        self.ror_frame.update_state()
        
pid = getpid()    
gui = GUI()
app.start(gui.logger)
gui.mainloop() #Il problema del movimento del mototre può essere qua. Magari il main loop no va bene (thread di thread di thread)
kill(pid, SIGKILL)