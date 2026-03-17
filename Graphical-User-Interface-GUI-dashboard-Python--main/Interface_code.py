# %%
# -*- coding: utf-8 -*-

"""


@author: John Arimboor
"""

#***********************************************#
# Wafer testing Dashboard 

# The problem:- In an electronics lab, engineers have to constanlty move optical setups and its configurations resulitng in change of instrumnets and thus
# the development of messy funcitons. The test operators or a third perison would find it difficult to have multiple interfaces for interacting with muliple 
# instrumenst and thus there is a high kind need of covering all the functions under one unmberalla and develop the ability to share inforamtion across multilple 
# user defined fucntions. This viusal controL gui uses Object oriented programming(OOP) making it easy to share and project information

#How to achieve it :- This code creates a dashobaord using python tkinter's library. To make the code look presentable, scalable and stacked , it is built
# using OOP under a single 'wafertester' class

#GUI:- 
#1. The left frame takes the commands from the user to move the stage and print the status 
#2.The Middle frame houses buttons to trigger specific tests:- LIVs and Spectra Analysis 
# 3.Right frame runs a continuted background loop to display a live data of instrumnets connected - stages and photodector current 


import tkinter as tk
import random

class Wafertester:
    def __init__(self, root):
        self.root = root
        self.root.title("Wafertesting Dashboard")
        self.root.geometry("800x400")

        
        #Initalizing Left, Middle, and Right Frames
        
        self.left_frame = tk.Frame(self.root, bd=2, relief="groove")   # Grooves are providing the panels boundary and border wdith gives the 3D appearance 
        self.left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)#The fill and expand commands ensures the frame is equally divided isntead of squishing each other 

        self.middle_frame = tk.Frame(self.root, bd=2, relief="groove")
        self.middle_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5) # The slide is pushed to the left side of the frame which is middle now

        self.right_frame = tk.Frame(self.root, bd=2, relief="groove")
        self.right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        
        # Initliazing Subframes, Labels, Buttos
          
        # --- LEFT FRAME SUBFRAMES ---
        tk.Label(self.left_frame, text="Stage Alignment", font=("Arial", 12, "bold")).pack(pady=10) # Initalizng the header for the left frame
        
        # Subframe 1 (User Entry)
        self.left_sub1 = tk.Frame(self.left_frame) #Intializes the subframe left_sub1
        self.left_sub1.pack(pady=10, fill="x", padx=10)
        
        self.entry_label = tk.Label(self.left_sub1, text="Enter Stage value(0- 155):") # 0-155 is the stage values that help the movement of the holder 
        self.entry_label.grid(row=0, column=0, padx=5) # The user define entry label is intialized 
        
        self.user_entry = tk.Entry(self.left_sub1, width=15)
        self.user_entry.grid(row=0, column=1, padx=5) # A new entry called user_entery,adjancent to coloumn 0 is intialized for stage value 
        
        self.submit_btn = tk.Button(self.left_sub1, text="Move", command=self.Stage_move) # A command called handle user entry is intialized for movement of stages 
        self.submit_btn.grid(row=0, column=2, padx=5)

        # Subframe 2 (Status)
        self.left_sub2 = tk.Frame(self.left_frame) # Crates a subframe in left fram to put the following labels and buttons 
        self.left_sub2.pack(pady=10, fill="x", padx=10)
        
        self.status_label = tk.Label(self.left_sub2, text="System Status: Idle") # Initializes the status of the stage with idle at start and change when command received
        self.status_label.pack(side="left", padx=5)
        
        self.status_btn = tk.Button(self.left_sub2, text="Stop_Stage", command=self.terminate) # Button to terminate the test instrument operation
        self.status_btn.pack(side="right", padx=5)


        # --- MIDDLE FRAME SUBFRAMES ---
        tk.Label(self.middle_frame, text="Test Options", font=("Arial", 12, "bold")).pack(pady=10) # Initializes header for the middle for perfomring test operations 

        # Subframe 1
        self.mid_sub1 = tk.Frame(self.middle_frame) # Creates a subframe among the middle frame for intializing buttons 
        self.mid_sub1.pack(pady=10)
        
        self.mid_label1 = tk.Label(self.mid_sub1, text="LIV Analysis")
        self.mid_label1.pack(side="left", padx=5)
        
        self.mid_btn1 = tk.Button(self.mid_sub1, text="Sweep ON", command=self.LightCurrentVoltage) # When clicked the buttons, shares the text as sweep on 
        self.mid_btn1.pack(side="left", padx=5)

        # Subframe 2
        self.mid_sub2 = tk.Frame(self.middle_frame)
        self.mid_sub2.pack(pady=10)
        
        self.mid_label2 = tk.Label(self.mid_sub2, text="Spectral Analysis")
        self.mid_label2.pack(side="left", padx=5)
        
        self.mid_btn2 = tk.Button(self.mid_sub2, text="Trigger ON", command=self.Spectra) # When clicked the button, shares the text as trigger on 
        self.mid_btn2.pack(side="left", padx=5)


        # --- RIGHT FRAME SUBFRAMES (POINT 7: Changing Values) ---
        tk.Label(self.right_frame, text="Instrument Readings", font=("Arial", 12, "bold")).pack(pady=10) #Creates a header for showing live feed of instrument values as test progresses

        # Subframe 1
        self.right_sub1 = tk.Frame(self.right_frame)
        self.right_sub1.pack(pady=10)
        
        tk.Label(self.right_sub1, text="Stage Status:").pack(side="left", padx=5)
        self.temp_value_label = tk.Label(self.right_sub1, text="0.0 mm", bg="black", fg="red", font=("Courier", 12, "bold"), width=8)
        self.temp_value_label.pack(side="left", padx=5)

        # Subframe 2 
        self.right_sub2 = tk.Frame(self.right_frame)
        self.right_sub2.pack(pady=10)
        
        tk.Label(self.right_sub2, text="Photodetector:").pack(side="left", padx=5)
        self.pressure_value_label = tk.Label(self.right_sub2, text="0 mA", bg="black", fg="green", font=("Courier", 12, "bold"), width=8)
        self.pressure_value_label.pack(side="left", padx=5)

        # Start the continuous loop to update instrument values
        self.update_instruments()
    
    # Declaring Specific test functions 
        
    def terminate(self): # Define what happens when the Stop_Stage button is clicked.
        self.status_label.config(text="System Status: STOP") # Change the status text to read "STOP".
        self.status_btn.config(state="disabled") # Disable (grey out) the button so it can't be clicked again.

    def LightCurrentVoltage(self): # Define what happens when the LIV Sweep button is clicked.
        current_text = self.mid_btn1.cget("text")
        if current_text == "Sweep ON":
            self.mid_btn1.config(text="Sweep Done", fg="red")#Change it to say "Sweep Done" and turn the text red.
        else:
            self.mid_btn1.config(text="Sweep ON", fg="black")#Change it back to "Sweep ON" with black text.

    def Spectra(self):
        current_text = self.mid_btn2.cget("text") # Define what happens when the Spectral Trigger button is clicked.
        if current_text == "Trigger ON":
            self.mid_btn2.config(text="Trigger OFF", fg="red")
        else:
            self.mid_btn2.config(text="Trigger ON", fg="black")

    def update_instruments(self):
        # Generate random values to simulate reading from an instrument
        simulated_temp = round(random.uniform(20.0, 155.0), 1)
        simulated_pressure = random.randint(0,500)

        # Update the labels
        self.temp_value_label.config(text=f"{simulated_temp} mm")
        self.pressure_value_label.config(text=f"{simulated_pressure} mA")

        self.root.after(500, self.update_instruments)# Scheduled this function to run again in 500 milliseconds (0.5 seconds)

    def Stage_move(self):
      
        entered_text = self.user_entry.get()   # Grabs text from the entry box and updates the status label 
        if entered_text.strip():
            self.status_label.config(text=f"Command received: {entered_text}")
            self.user_entry.delete(0, tk.END) # Clear the entry box


if __name__ == "__main__":
    root = tk.Tk() # Fire up the hidden Tkinter engine and create the main window object.
    app = Wafertester(root) # Hand that blank window over to our Wafertester blueprint so it can build the dashboard.

    root.mainloop()
