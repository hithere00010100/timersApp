import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

# Put dark mode and green color accent
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Assign pomodoro timer times
focusTime = 35 * 60
breakTime = 10 * 60
pomodoroTimerCounter = 1

# Assign eating timer times
lunchTime = 15 * 60
dinnerTime = 10 * 60

class timer:
    def __init__(self):
        # Initialize some pomodoro timer values
        self.focusTime = focusTime
        self.pomodoroTimerCounter = pomodoroTimerCounter

        # Set initial conditions for pomodoro timer
        self.isPomodoroTimerRunning = False
        self.isPomodoroTimerFirstTime = True
        self.isFocusTime = True
        self.isBreakTime = False
        self.skipPomodoroTimer = False

        # Set initial conditions for eating timer
        self.isEatingTimerRunning = False
        self.isEatingTimerFirstTime = True

        # Create and set up window
        self.window = ctk.CTk()
        self.window.geometry("350x250")
        self.window.title("TimersApp")

        # Create and set up pomodoro timer label
        self.pomodoroTimerLabel = ctk.CTkButton(self.window, text = "Start/stop", fg_color = "transparent", command = self.triggerPomodoroTimer)
        self.pomodoroTimerLabel.pack(pady = 5)

        # Create and set up pomodoro timer counter label
        self.pomodoroTimerCounterLabel = ctk.CTkLabel(self.window, text = "Turn on DND")
        self.pomodoroTimerCounterLabel.pack()

        # Create and set up pomodoro timer buttons frame (container)
        self.pomodoroTimerButtonsFrame = ctk.CTkFrame(self.window)
        self.pomodoroTimerButtonsFrame.pack()

        # Create and set up pomodoro timer reset button
        self.pomodoroTimerResetButton = ctk.CTkButton(self.pomodoroTimerButtonsFrame, text = "Reset", width = 100, command = self.resetPomodoroTimer)
        self.pomodoroTimerResetButton.pack(side = "left", padx = 2.5)

        # Create and set up pomodoro timer skip button
        self.pomodoroTimerSkipButton = ctk.CTkButton(self.pomodoroTimerButtonsFrame, text = "Skip", width = 100, command = self.skipPomodoroTimerBlock)
        self.pomodoroTimerSkipButton.pack(side = "left", padx = 2.5)

        # Create and set up pomodoro timer reset counter button
        self.pomodoroTimerResetCounterButton = ctk.CTkButton(self.pomodoroTimerButtonsFrame, text = "Reset", width = 100, command = self.resetPomodoroTimerCounter)
        self.pomodoroTimerResetCounterButton.pack(side = "left", padx = 2.5)

        # Create and set up eating timer label
        self.eatingTimerLabel = ctk.CTkButton(self.window, text = "Start/stop", fg_color = "transparent", command = self.triggerEatingTimer)
        self.eatingTimerLabel.pack(pady = 20)

        # Create and set up eating timer switch 
        self.eatingTimerSwitchState = tk.BooleanVar()

        self.eatingTimerChangeModeSwitch = ctk.CTkSwitch(self.window,
                                                    text = "Breakfast/dinner",
                                                    variable = self.eatingTimerSwitchState,
                                                    onvalue = True,
                                                    offvalue = False,
                                                    command = self.resetEatingTimer)
        self.eatingTimerChangeModeSwitch.pack(pady = 5)
        
        # Initialize eating timer times according to switch state
        self.resetEatingTimer()
        
        # Create and set up eating timer reset button
        self.eatingTimerResetButton = ctk.CTkButton(self.window, text = "Reset", command = self.resetEatingTimer)
        self.eatingTimerResetButton.pack()

        # Show alert every minute if no timer is running 
        self.bother()
        
        self.window.mainloop()

    def triggerPomodoroTimer(self):
        # Run pomodoro timer when start/stop button is pressed or stop it if it's already running
        if self.isPomodoroTimerRunning == False:
            self.isPomodoroTimerRunning = True
            
            # Make sure to avoid double counting
            if self.isPomodoroTimerFirstTime == True:
                self.updatePomodoroTimer()
        
        else:
            self.isPomodoroTimerRunning = False
            # Show DND reminder if timer is stopped
            self.pomodoroTimerCounterLabel.configure(text = "Turn on DND")
    
    def resetPomodoroTimer(self):
        # Reinitialize pomodoro timer times
        self.focusTime = focusTime
        self.breakTime = breakTime

        # Show updated timer when resetted according to pomodoro timer block
        if self.isFocusTime == True:
            self.pomodoroTimerMinutes, self.pomodoroTimerSeconds = divmod(self.focusTime, 60)
            self.pomodoroTimerLabel.configure(text = "{:02d}:{:02d}".format(self.pomodoroTimerMinutes, self.pomodoroTimerSeconds))
        else:
            # Assign break time according to pomodoro timer counter
            if self.pomodoroTimerCounter % 4 == 0:
                self.breakTime = breakTime * 2
            else:
                self.breakTime = breakTime
            
            self.pomodoroTimerMinutes, self.pomodoroTimerSeconds = divmod(self.breakTime, 60)
            self.pomodoroTimerLabel.configure(text = "{:02d}:{:02d}".format(self.pomodoroTimerMinutes, self.pomodoroTimerSeconds))

    def skipPomodoroTimerBlock(self):
        # Show a flag when skip button is pressed
        self.skipPomodoroTimer = True

    def updatePomodoroTimer(self):
        # Change pomodoro timer state to avoid double counting
        self.isPomodoroTimerFirstTime = False
        
        # Start pomodoro timer if eating timer is not running
        if self.isEatingTimerRunning == False:
            # Update focus timer on the screen
            if self.isPomodoroTimerRunning == True and self.isFocusTime == True:
                # Update pomodoro counter every focus block only when timer is running
                self.pomodoroTimerCounterLabel.configure(text = self.pomodoroTimerCounter)
                
                self.focusTime -= 1
                self.pomodoroTimerMinutes, self.pomodoroTimerSeconds = divmod(self.focusTime, 60)
                self.pomodoroTimerLabel.configure(text = "{:02d}:{:02d}".format(self.pomodoroTimerMinutes, self.pomodoroTimerSeconds))
                
                # Reset this focus timer for later use when time's over or skip button is pressed
                if self.focusTime == 0 or self.skipPomodoroTimer == True:
                    self.isPomodoroTimerRunning = False
                    self.focusTime = focusTime
                    self.skipPomodoroTimer = False

                    # Show finish alert on the screen and set conditions for break timer
                    self.window.state(newstate = "normal")
                    self.window.attributes("-topmost", True)
                    self.alertReturn = messagebox.showerror(message = "Get up, check phone, read and exercise", type = "ok")
                    self.window.attributes("-topmost", False)
                    
                    if(self.alertReturn == "ok"):
                        self.isFocusTime = False
                        self.isBreakTime = True
                        self.isPomodoroTimerRunning = True

                    # Assign break time according to pomodoro timer counter
                    if self.pomodoroTimerCounter % 4 == 0:
                        self.breakTime = breakTime * 2
                    else:
                        self.breakTime = breakTime

            # Update break timer on the screen
            elif self.isPomodoroTimerRunning == True and self.isBreakTime == True:
                self.breakTime -= 1
                self.pomodoroTimerMinutes, self.pomodoroTimerSeconds = divmod(self.breakTime, 60)
                self.pomodoroTimerLabel.configure(text = "{:02d}:{:02d}".format(self.pomodoroTimerMinutes, self.pomodoroTimerSeconds))

                # Reset this break timer for later use when time's over or skip button is pressed
                if self.breakTime == 0 or self.skipPomodoroTimer == True:
                    self.isPomodoroTimerRunning = False
                    self.breakTime = breakTime
                    self.skipPomodoroTimer = False

                    # Increase pomodoro counter
                    self.pomodoroTimerCounter += 1

                    # Show finish alert on the screen and set conditions for focus timer
                    self.window.state(newstate = "normal")
                    self.window.attributes("-topmost", True)
                    self.alertReturn = messagebox.showerror(message = "Let's focus", type = "ok")
                    self.window.attributes("-topmost", False)

                    if(self.alertReturn == "ok"):
                        self.isFocusTime = True
                        self.isBreakTime = False
                        self.isPomodoroTimerRunning = True
        
        # Refresh every second
        self.window.after(1000, self.updatePomodoroTimer)
        
    def bother(self):
        # Show alert every minute if no timer is running
        if self.isPomodoroTimerRunning == False and self.isEatingTimerRunning == False:
            self.window.state(newstate = "normal")
            self.window.attributes("-topmost", True)
            messagebox.showerror(message = "Start a timer")
            self.window.attributes("-topmost", False)

        self.window.after(60000, self.bother)

    def resetPomodoroTimerCounter(self):
        # Reinitialize pomodoro timer counter
        self.pomodoroTimerCounter = pomodoroTimerCounter

    def triggerEatingTimer(self):
        # Stop pomodoro timer when the button is pressed
        self.isPomodoroTimerRunning = False

        # Run eating timer when start/stop button is pressed or stop it if it's already running
        if self.isEatingTimerRunning == False:
            self.isEatingTimerRunning = True

            # Make sure to avoid double counting
            if self.isEatingTimerFirstTime == True:
                self.updateEatingTimer()
        else:
            self.isEatingTimerRunning = False

    def updateEatingTimer(self):
        # Update eating timer on the screen
        if self.isEatingTimerRunning == True:
            self.isEatingTimerFirstTime = False
            
            self.eatingTime -= 1

            # Reset this eating timer for later use when time's over
            if self.eatingTime == 0:
                self.isEatingTimerRunning = False

                # Show finish alert on the screen
                self.window.state(newstate = "normal")
                self.window.attributes("-topmost", True)
                self.alertReturn = messagebox.showerror(message = "Stop what you're doing RIGHT NOW!")
                self.window.attributes("-topmost", False)

                if self.alertReturn == "ok":
                    self.resetEatingTimer()

            self.eatingTimerMinutes, self.eatingTimerSeconds = divmod(self.eatingTime, 60)
            self.eatingTimerLabel.configure(text = "{:02d}:{:02d}".format(self.eatingTimerMinutes, self.eatingTimerSeconds))
        
        # Refresh every second
        self.window.after(1000, self.updateEatingTimer)

    def resetEatingTimer(self):
        # Reinitialize eating timer times according to switch state
        if self.eatingTimerSwitchState.get() == True:
            self.eatingTime = dinnerTime
        else:
            self.eatingTime = lunchTime

        # Show updated timer when resetted
        self.eatingTimerMinutes, self.eatingTimerSeconds = divmod(self.eatingTime, 60)
        self.eatingTimerLabel.configure(text = "{:02d}:{:02d}".format(self.eatingTimerMinutes, self.eatingTimerSeconds))
        
            
timer()
