
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 12:51:25 2026

@author: John Arimboor
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 16:15:00 2026

@author: John Arimboor
"""
#******************************************#
#Keithley 2520 Pulsed Sweep Automation Script using PyVISA library 
#The problem :- Wafers that consist of 5000+ chips are sensistive devices like laser diodes and qubits and requires precise thermal management 
#The task was to replace a test station that ran with a continous DC current through time which eventually led to overheat and degrade. This project 
#is aimed at developing an automated python script that replace DC with a ultra fast precise timed pulsed sweeps by reading the paramters for each device from 
# a user defined config file 
# 
#How this code achieves it :
# 1. Configuration: The script first reads a simple, external text file 
#    containing the safe test limits and pulse timings (Pdelay, Pwidth) for the DUT.
# 2. Initialization: It uses the PyVISA library to find the instrument on the lab 
# 3. Execution: It triggers the pulsed sweep, reading Voltage and two separate 
#    Current channels simultaneously.
# 4. Data Logging:It takes the raw, messy string of data,appends it with the 
#    exact time of the test, and exports it safely to an Excel file.

import pyvisa as py 
import pandas as pd
import csv
import numpy as np 
import matplotlib.pyplot as plt
import datetime # module required to generate timestamp for seperating the saved files 


# Function to extract test parameters set by the user in a config file 
def load_config(filename):
    config = {} # An empty dictionary is declared to store the new values
    with open(filename, encoding="utf-8-sig") as f:# Safely open the file. "utf-8-sig" automatically removes invisible characters (like the Byte Order Mark) that Windows sometimes hides at the start of text files.
        for line in f: 
            if "Configfile2520" in line.lower(): 
                header = [h.strip() for h in line.split("\t")] #split this line into pieces wherever there is a Tab space ("\t"),.strip() to clean off any accidental empty spaces around the words.
                break #'header' is a clean list of our column names (e.g., ['Parameters', 'Start_I', 'Stop_I']). Now we need the values
        else:
            print("Config header not found")

        reader = csv.DictReader(f, fieldnames=header, delimiter="\t") # The exisiting data is send over to a dict to collect the required values 
        for row in reader: # Loop through the remaining rows of actual numbers/data.
            if row["Parameters"]: # Checking to make sure there is text
                config[row["Parameters"].strip()] = row # enetering the entire row's of data into the folder of config

    return config


ConfigKE2520= load_config(r"C:\Users\John Arimboor\OneDrive\Desktop\John_Arimboor\Apply Jobs 2025\Sample jobs\Quantware Delft\Config_File.txt") #Upload the config file 
mode = ConfigKE2520["DUT_2"]["Mode"]
print(mode)


#Instrument check 
# # Creat a resource manager and checking for the instrument's address and print the values
rm = py.ResourceManager()
print("Available resources:")
resources = rm.list_resources()
print(resources)
GPIB_address = resources[0]   # choose instrument (change index if needed)
KE2520 = rm.open_resource(GPIB_address)
print("Instrument ID:")
print(KE2520.query("*IDN?"))


#Initialize the paramteres using SCPI commands for performing sweeps using a keithley 2520  laser diode test system (device used)
def Init_KE2520(KE2520,ConfigKE2520):
    KE2520.write(':FORM:ELEM VOLT1,CURR2,CURR3')  #Laser Diode voltage, detector current data - the output format 
    KE2520.write(f':SENS1:VOLT:RANG {ConfigKE2520["DUT_1"]["LD_V"]} ') # Laser diode voltage 
    KE2520.write(f':SOUR1:CURR:RANG {ConfigKE2520["DUT_1"]["LD_I"]}') # laser diode current
    
    KE2520.write(f':SOUR1:CURR:STAR {ConfigKE2520["DUT_1"]["Start_I"]}') # start current 
    KE2520.write(f':SOUR1:CURR:STOP {ConfigKE2520["DUT_1"]["Stop_I"]}') # stop current 
    KE2520.write(f':SOUR1:CURR:STEP {ConfigKE2520["DUT_1"]["Step_I"]}') # step current 
    
    KE2520.write(f':SOUR2:VOLT {ConfigKE2520["DUT_1"]["D1_V"]}') #Detector's 1 voltage range 
    KE2520.write(f':SOUR3:VOLT {ConfigKE2520["DUT_1"]["D2_V"]}') #Detector 2 voltage range 
    
    KE2520.write(f':SOUR1:FUNC {ConfigKE2520["DUT_1"]["Mode"]}') # DC or Pulsed mode for sweeps 
  
    
    KE2520.write(f'SOUR1:PULS:DEL {ConfigKE2520["DUT_1"]["Pdelay"]}') # Pulsed delay 
    KE2520.write('SOUR1:PULS:WIDT {ConfigKE2520["DUT_1"]["Pwidth"]}')# Pulsed width 
    
    KE2520.write(':SOUR1:CURR:MODE SWE') #Selecting staircase sweep mode
    KE2520.write(':SOUR1:SWE:SPAC LIN') # Selecting linear staircase sweep 
    
    return None

# Sweeping fucntion
def Sweep_KE2520(KE2520,ConfigKE2520):
    #Hardware Communication for tunring ON 
    KE2520.write(':OUTP1 ON')
    data=KE2520.query(':READ?')
    KE2520.write(':OUTP1 OFF')
    # Decalring the time stamps for data accuracy 
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Generating the current time for data accuracy, the timestamp is used for excel file name and no colons
    EXCEL_FILENAME = f'smu_measurements_{timestamp}.xlsx'
    #Converting string to numpy
    stringvalue=np.fromstring(data,sep=",")  # Converts the string results into array([V1, I1a, I1b, V2, I2a, I2b, ...])
    # Reshaping the array into rows of 3
    data_reshaped=stringvalue.reshape(-1,3) #Divides the code into arrays of three [[V1, I1a, I1b],
    # Converting into dictoinary 
    data_dict = {"Timestamp":timestamp,"Voltage": data_reshaped[:, 0], "Current1": data_reshaped[:, 1],"Current2": data_reshaped[:, 2]}  # data_reshaped is in the form data_reshaped[row,coloumn], now : take all rows , and ,0 means first just first coloumn and 1 means just second coloumn 
      
    df = pd.DataFrame(data_dict,columns=["Timestamp","Voltage", "Current1", "Current2"])
    df.to_excel(EXCEL_FILENAME, index=False)
    print(f"Sweep completed! Data saved to:{EXCEL_FILENAME}")
    
       

    

    
 


