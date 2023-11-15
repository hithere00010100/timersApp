import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

# Set theme appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Set timer's variables
focusTime = 35 * 60
breakTime = 10 * 60
pomodoroCounter = 1

lunchTime = 15 * 60

class timer:
    def __init__(self):
        # Import global variables to this local scope
        self.focusTime = focusTime
        self.pomodoroCounter = pomodoroCounter

        self.lunchTime = lunchTime

        # Set initial conditions for pomodoro timer
        self.isTimerRunning = False
        self.isFocusTime = True
        self.isBreakTime = False
        self.isFirstTimePressed = True

        # Set initial conditions for lunch timer
        self.isLunchTimerRunning = False
        self.isFirstTimePressedLunch = True

        # Define window
        self.window = ctk.CTk()
        self.window.geometry("350x200")
        self.window.title("TimersApp")

        # Create timer triggerable label
        self.timerLabel = ctk.CTkButton(self.window, text = "Start/stop", fg_color = "transparent", command = self.triggerTimer)
        self.timerLabel.pack(pady = 5)

        # Create pomodoro counter label
        self.pomodoroCounterLabel = ctk.CTkLabel(self.window, text = "#")
        self.pomodoroCounterLabel.pack()

        # Create timer buttons frame
        self.timerButtonsFrame = ctk.CTkFrame(self.window)
        self.timerButtonsFrame.pack()

        # Create timer reset button
        self.timerResetButton = ctk.CTkButton(self.timerButtonsFrame, text = "Reset", width = 100, command = self.resetTimer)
        self.timerResetButton.pack(side = "left", padx = 2.5)

        # Create timer skip button
        self.timerSkipButton = ctk.CTkButton(self.timerButtonsFrame, text = "Skip", width = 100, command = self.skipBlock)
        self.timerSkipButton.pack(side = "left", padx = 2.5)

        # Create pomodoro counter
        self.timerResetPomodoroCounterButton = ctk.CTkButton(self.timerButtonsFrame, text = "Reset", width = 100, command = self.resetPomodoroCounter)
        self.timerResetPomodoroCounterButton.pack(side = "left", padx = 2.5)

        # Create lunch timer label
        self.lunchTimerLabel = ctk.CTkButton(self.window, text = "Start/stop", fg_color = "transparent", command = self.triggerLunchTimer)
        self.lunchTimerLabel.pack(pady = 20)

        # Create reset lunch timer button
        self.resetLunchTimerButton = ctk.CTkButton(self.window, text = "Reset", command = self.resetLunchTimer)
        self.resetLunchTimerButton.pack()

        # Show alert if timer is not working
        self.bother()
        
        # Run window
        self.window.mainloop()

    def triggerTimer(self):
        # Start timer when start button is pressed
        if self.isTimerRunning == False:
            self.isTimerRunning = True
            
            # Make sure updateTimer is only executed once
            if self.isFirstTimePressed == True:
                self.updateTimer()
        
        else:
            # Stop timer when stop button is pressed
            self.isTimerRunning = False
    
    def resetTimer(self):
        # Reset timer's variables
        self.focusTime = focusTime
        self.breakTime = breakTime

    def skipBlock(self):
        # Go to the next timer
        self.skipBlock = True

    def updateTimer(self):
        # Update isFirstTimePressed to avoid double updateTimer executions
        self.isFirstTimePressed = False
        # Show actual pomodoro
        self.pomodoroCounterLabel.configure(text = self.pomodoroCounter)
        
        # Deactive pomodoro timer while lunch timer is on
        if self.isLunchTimerRunning == False:
            if self.isTimerRunning == True and self.isFocusTime == True:
                # Reduce focusTime and show updated timer if start button was pressed
                self.focusTime -= 1
                self.timerMinutes, self.timerSeconds = divmod(self.focusTime, 60)
                self.timerLabel.configure(text = "{:02d}:{:02d}".format(self.timerMinutes, self.timerSeconds))
                
                if self.focusTime == 0 or self.skipBlock == True:
                    # Stop counting, reset focusTime and skipBlock variable when time is over or skip button was pressed
                    self.isTimerRunning = False
                    self.focusTime = focusTime
                    self.skipBlock = False

                    # Show window and the alert
                    self.window.state(newstate = "normal")
                    self.window.attributes("-topmost", True)
                    self.timesOver = messagebox.showerror(message = "Check phone, exercise, read or get ahead on due stuff", type = "ok")
                    
                    if(self.timesOver == "ok"):
                        # Set breakTime conditions to start automatically
                        self.isFocusTime = False
                        self.isBreakTime = True
                        self.isTimerRunning = True

                    # Set breakTime based on the actual pomodoro
                    if self.pomodoroCounter % 4 == 0:
                        # If pomodoroCounter = (4, 8, 12, ...), breakTime is a long break
                        self.breakTime = breakTime * 2
                        
                    else:
                        self.breakTime = breakTime

            elif self.isTimerRunning == True and self.isBreakTime == True:
                # Reduce breakTime and show updated timer if start button was pressed
                self.breakTime -= 1
                self.timerMinutes, self.timerSeconds = divmod(self.breakTime, 60)
                self.timerLabel.configure(text = "{:02d}:{:02d}".format(self.timerMinutes, self.timerSeconds))

                if self.breakTime == 0 or self.skipBlock == True:
                    # Stop counting, reset focusTime and skipBlock variable when time is over or skip button was pressed
                    self.isTimerRunning = False
                    self.breakTime = breakTime
                    self.skipBlock = False

                    # Increment pomodoroCounter
                    self.pomodoroCounter += 1

                    # Show window and the alert
                    self.window.state(newstate = "normal")
                    self.window.attributes("-topmost", True)
                    self.timesOver = messagebox.showerror(message = "Let's focus", type = "ok")

                    if(self.timesOver == "ok"):
                        # Set focusTime conditions to start automatically
                        self.isFocusTime = True
                        self.isBreakTime = False
                        self.isTimerRunning = True
        
        # Execute updateTimer every second
        self.window.after(1000, self.updateTimer)
        
    def bother(self):
        # If no timer is running, show reminder every minute
        if self.isTimerRunning == False and self.isLunchTimerRunning == False:
            # Show window and put it always on top
            self.window.state(newstate = "normal")
            self.window.attributes("-topmost", True)
            messagebox.showerror(message = "Turn on DND and start a timer")

        # If at least one timer is running, hide window and put it on the background
        else:
            self.window.state(newstate = "iconic")
            self.window.attributes("-topmost", False)

        self.window.after(60000, self.bother)

    def resetPomodoroCounter(self):
        self.pomodoroCounter = pomodoroCounter

    def triggerLunchTimer(self):
        # Same logic as triggerTimer function
        if self.isLunchTimerRunning == False:
            self.isLunchTimerRunning = True

            if self.isFirstTimePressedLunch == True:
                self.updateLunchTimer()
        else:
            self.isLunchTimerRunning = False

    def updateLunchTimer(self):
        # Same logic as updateTimer function
        if self.isLunchTimerRunning == True:
            self.isFirstTimePressedLunch = False
            
            self.lunchTime -= 1
            self.lunchMinutes, self.lunchSeconds = divmod(self.lunchTime, 60)
            self.lunchTimerLabel.configure(text = "{:02d}:{:02d}".format(self.lunchMinutes, self.lunchSeconds))

            if self.lunchTime == 0:
                self.isLunchTimerRunning = False
                # Stop pretending that pomodoro timer is working (revert simulation made in bother function)
                self.isTimerRunning = False

                self.window.state(newstate = "normal")
                self.window.attributes("-topmost", True)
                messagebox.showerror(message = "Stop what you're doing RIGHT NOW!")

        self.window.after(1000, self.updateLunchTimer)

    def resetLunchTimer(self):
        self.lunchTime = lunchTime
        
timer()
