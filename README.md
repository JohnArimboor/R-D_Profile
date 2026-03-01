# Pulsed-Sweep-Automation-using-PyVISA-library-Python


Project Overview:- This project is aimed to fully automate the interaction with an SMU for performing pulsed sweeps. It uses SCPI commands over a GPIB/USB connection to fully initialize the instrument, perform highly controlled pulsed current sweeps and securely log the data

Purpose:-The manual process of running measurements via the instrument's front panel is slow and prone to human error.By pulling safety limits from an external text file (Config_File.txt), this code could engineer a fully automated test station that performs pulsed sweeps accroding to the user's customzied paramters for each devie.

Key Functions Used:
1. pyvisa: The library used for a connection with the SMU test instrument. 

2.Init_KE2520(): Sends the configuration data into SCPI commands to set the instrument's voltage ranges, pulse widths, pulse delays, and sweep modes safely.

3.Sweep_KE2520(): Triggers the physical measurement and exports data to a dynamically named Excel file.
