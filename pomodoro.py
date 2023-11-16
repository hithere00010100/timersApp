import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

focusTime = 35 * 60
breakTime = 10 * 60
pomodoroTimerCounter = 1

lunchTime = 15 * 60
dinnerTime = 10 * 60

class timer:
    def __init__(self):
        self.focusTime = focusTime
        self.pomodoroTimerCounter = pomodoroTimerCounter

        self.isPomodoroTimerRunning = False
        self.isFocusTime = True
        self.isBreakTime = False
        self.isPomodoroTimerFirstTime = True
        self.skipPomodoroTimer = False

        self.isEatingTimerRunning = False
        self.isEatingTimerFirstTime = True

        self.window = ctk.CTk()
        self.window.geometry("350x250")
        self.window.title("TimersApp")

        self.pomodoroTimerLabel = ctk.CTkButton(self.window, text = "Start/stop", fg_color = "transparent", command = self.triggerPomodoroTimer)
        self.pomodoroTimerLabel.pack(pady = 5)

        self.pomodoroTimerCounterLabel = ctk.CTkLabel(self.window, text = "#")
        self.pomodoroTimerCounterLabel.pack()

        self.pomodoroTimerButtonsFrame = ctk.CTkFrame(self.window)
        self.pomodoroTimerButtonsFrame.pack()

        self.pomodoroTimerResetButton = ctk.CTkButton(self.pomodoroTimerButtonsFrame, text = "Reset", width = 100, command = self.resetPomodoroTimer)
        self.pomodoroTimerResetButton.pack(side = "left", padx = 2.5)

        self.pomodoroTimerSkipButton = ctk.CTkButton(self.pomodoroTimerButtonsFrame, text = "Skip", width = 100, command = self.skipPomodoroTimerBlock)
        self.pomodoroTimerSkipButton.pack(side = "left", padx = 2.5)

        self.pomodoroTimerResetCounterButton = ctk.CTkButton(self.pomodoroTimerButtonsFrame, text = "Reset", width = 100, command = self.resetPomodoroTimerCounter)
        self.pomodoroTimerResetCounterButton.pack(side = "left", padx = 2.5)

        self.eatingTimerLabel = ctk.CTkButton(self.window, text = "Start/stop", fg_color = "transparent", command = self.triggerEatingTimer)
        self.eatingTimerLabel.pack(pady = 20)

        self.eatingTimerSwitchState = tk.BooleanVar()

        self.eatingTimerChangeModeSwitch = ctk.CTkSwitch(self.window,
                                                    text = "Breakfast/dinner",
                                                    variable = self.eatingTimerSwitchState,
                                                    onvalue = True,
                                                    offvalue = False,
                                                    command = self.resetEatingTimer)
        self.eatingTimerChangeModeSwitch.pack(pady = 5)
        
        self.resetEatingTimer()
        
        self.eatingTimerResetButton = ctk.CTkButton(self.window, text = "Reset", command = self.resetEatingTimer)
        self.eatingTimerResetButton.pack()

        self.bother()
        
        self.window.mainloop()

    def triggerPomodoroTimer(self):
        if self.isPomodoroTimerRunning == False:
            self.isPomodoroTimerRunning = True
            
            if self.isPomodoroTimerFirstTime == True:
                self.updatePomodoroTimer()
        
        else:
            self.isPomodoroTimerRunning = False
    
    def resetPomodoroTimer(self):
        self.focusTime = focusTime
        self.breakTime = breakTime

    def skipPomodoroTimerBlock(self):
        self.skipPomodoroTimer = True

    def updatePomodoroTimer(self):
        self.isPomodoroTimerFirstTime = False
        self.pomodoroTimerCounterLabel.configure(text = self.pomodoroTimerCounter)
        
        if self.isEatingTimerRunning == False:
            if self.isPomodoroTimerRunning == True and self.isFocusTime == True:
                self.focusTime -= 1
                self.pomodoroTimerMinutes, self.pomodoroTimerSeconds = divmod(self.focusTime, 60)
                self.pomodoroTimerLabel.configure(text = "{:02d}:{:02d}".format(self.pomodoroTimerMinutes, self.pomodoroTimerSeconds))
                
                if self.focusTime == 0 or self.skipPomodoroTimer == True:
                    self.isPomodoroTimerRunning = False
                    self.focusTime = focusTime
                    self.skipPomodoroTimer = False

                    self.window.state(newstate = "normal")
                    self.window.attributes("-topmost", True)
                    self.alertReturn = messagebox.showerror(message = "Check phone, exercise, read or get ahead on due stuff", type = "ok")
                    
                    if(self.alertReturn == "ok"):
                        self.isFocusTime = False
                        self.isBreakTime = True
                        self.isPomodoroTimerRunning = True

                    if self.pomodoroTimerCounter % 4 == 0:
                        self.breakTime = breakTime * 2

                    else:
                        self.breakTime = breakTime

            elif self.isPomodoroTimerRunning == True and self.isBreakTime == True:
                self.breakTime -= 1
                self.pomodoroTimerMinutes, self.pomodoroTimerSeconds = divmod(self.breakTime, 60)
                self.pomodoroTimerLabel.configure(text = "{:02d}:{:02d}".format(self.pomodoroTimerMinutes, self.pomodoroTimerSeconds))

                if self.breakTime == 0 or self.skipPomodoroTimer == True:
                    self.isPomodoroTimerRunning = False
                    self.breakTime = breakTime
                    self.skipPomodoroTimer = False

                    self.pomodoroTimerCounter += 1

                    self.window.state(newstate = "normal")
                    self.window.attributes("-topmost", True)
                    self.alertReturn = messagebox.showerror(message = "Let's focus", type = "ok")

                    if(self.alertReturn == "ok"):
                        self.isFocusTime = True
                        self.isBreakTime = False
                        self.isPomodoroTimerRunning = True
        
        self.window.after(1000, self.updatePomodoroTimer)
        
    def bother(self):
        if self.isPomodoroTimerRunning == False and self.isEatingTimerRunning == False:
            self.window.state(newstate = "normal")
            self.window.attributes("-topmost", True)
            messagebox.showerror(message = "Turn on DND and start a timer")
            self.window.attributes("-topmost", False)

        self.window.after(60000, self.bother)

    def resetPomodoroTimerCounter(self):
        self.pomodoroTimerCounter = pomodoroTimerCounter

    def triggerEatingTimer(self):
        if self.isEatingTimerRunning == False:
            self.isEatingTimerRunning = True

            if self.isEatingTimerFirstTime == True:
                self.updateEatingTimer()
        else:
            self.isEatingTimerRunning = False

    def updateEatingTimer(self):
        if self.isEatingTimerRunning == True:
            self.isEatingTimerFirstTime = False
            
            self.eatingTime -= 1

            if self.eatingTime == 0:
                self.isEatingTimerRunning = False

                self.window.state(newstate = "normal")
                self.window.attributes("-topmost", True)
                self.alertReturn = messagebox.showerror(message = "Stop what you're doing RIGHT NOW!")

                if self.alertReturn == "ok":
                    self.resetEatingTimer()

            self.eatingTimerMinutes, self.eatingTimerSeconds = divmod(self.eatingTime, 60)
            self.eatingTimerLabel.configure(text = "{:02d}:{:02d}".format(self.eatingTimerMinutes, self.eatingTimerSeconds))
        
        self.window.after(1000, self.updateEatingTimer)

    def resetEatingTimer(self):
        if self.eatingTimerSwitchState.get() == True:
            self.eatingTime = dinnerTime
        else:
            self.eatingTime = lunchTime
            
timer()
