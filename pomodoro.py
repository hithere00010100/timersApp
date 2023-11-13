import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

# Set theme appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Set timer's variables
focusTime = 2 * 60
breakTime = 1 * 60
pomodoroCounter = 1

class timer:
    def __init__(self):
        # Import global variables to this local scope
        self.focusTime = focusTime
        self.pomodoroCounter = pomodoroCounter

        # Set initial conditions
        self.isTimerRunning = False
        self.isFocusTime = True
        self.isBreakTime = False
        self.isFirstTimePressed = True

        # Define window
        self.window = ctk.CTk()
        self.window.geometry("350x200")
        self.window.title("PomodoroApp")

        # Create timer triggerable label
        self.timerLabel = ctk.CTkButton(self.window, text = "Pomodoro", fg_color = "transparent", command = self.triggerTimer)
        self.timerLabel.pack()

        # Create pomodoro counter label
        self.pomodoroCounterLabel = ctk.CTkLabel(self.window, text = "#")
        self.pomodoroCounterLabel.pack()

        # Create timer buttons frame
        self.timerButtonsFrame = ctk.CTkFrame(self.window)
        self.timerButtonsFrame.pack()

        # Create timer reset button
        self.timerResetButton = ctk.CTkButton(self.timerButtonsFrame, text = "Reset timer", width = 100, command = self.resetTimer)
        self.timerResetButton.pack(side = "left", padx = 2.5)

        # Create timer skip button
        self.timerSkipButton = ctk.CTkButton(self.timerButtonsFrame, text = "Skip", width = 100, command = self.skipBlock)
        self.timerSkipButton.pack(side = "left", padx = 2.5)

        # Create pomodoro counter
        self.timerResetPomodoroCounterButton = ctk.CTkButton(self.timerButtonsFrame, text = "Reset pomodoros", width = 100, command = self.resetPomodoroCounter)
        self.timerResetPomodoroCounterButton.pack(side = "left", padx = 2.5)

        # Show alert if timer is not working
        self.bother()
        
        # Run window
        self.window.mainloop()

    def triggerTimer(self):
        if self.isTimerRunning == False:
            # Start timer when do not disturb is on and start button is pressed
            self.doNotDisturb = messagebox.showwarning(title = "Reminder",message = "Turn on do not disturb on the phone")

            if self.doNotDisturb == "ok":
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
        
        if self.isTimerRunning == True and self.isFocusTime == True:
            # Reduce focusTime and show updated timer if start button was pressed
            self.focusTime -= 20
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
                self.timesOver = messagebox.askquestion(title = "Question", message = "Do you want to start next block?")
                
                if(self.timesOver == "yes"):
                    # Set breakTime conditions to start automatically
                    self.isFocusTime = False
                    self.isBreakTime = True
                    self.isTimerRunning = True
                
                else:
                    # Set breakTime conditions to start manually
                    self.isFocusTime = False
                    self.isBreakTime = True
                    self.isTimerRunning = False

                # Set breakTime based on the actual pomodoro
                if self.pomodoroCounter % 4 == 0:
                    # If pomodoroCounter = (4, 8, 12, ...), breakTime is a long break
                    self.breakTime = breakTime * 2
                else:
                    self.breakTime = breakTime

        elif self.isTimerRunning == True and self.isBreakTime == True:
            # Reduce breakTime and show updated timer if start button was pressed
            self.breakTime -= 20
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
                self.timesOver = messagebox.askquestion(title = "Question", message = "Do you want to start next block?")

                if(self.timesOver == "yes"):
                    # Set focusTime conditions to start automatically
                    self.isFocusTime = True
                    self.isBreakTime = False
                    self.isTimerRunning = True
                
                else:
                    # Set focusTime conditions to start manually
                    self.isFocusTime = False
                    self.isBreakTime = True
                    self.isTimerRunning = False
        
        # Execute updateTimer every second
        self.window.after(1000, self.updateTimer)
        
    def bother(self):
        if self.isTimerRunning == False:
            # Set the window as "always on top" and annoy user when switching to other apps without starting the timer
            self.window.attributes("-topmost", True)
            self.window.bind("<FocusOut>", lambda event: messagebox.showerror(message = "Start a timer"))
        
        else:
            self.window.attributes("-topmost", False)
            self.window.unbind("<FocusOut>")

        # Execute bother every second
        self.window.after(1000, self.bother)

    def resetPomodoroCounter(self):
        self.pomodoroCounter = pomodoroCounter

timer()
