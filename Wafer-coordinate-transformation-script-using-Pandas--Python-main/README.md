# Wafer-coordinate-transformation-script-using-Pandas--Python

Project Overview:-Compnaies usually handle large sets of data for automated semiconductor or quantum wafer testing processes.This code attempts to convert file containing the theoretical layout, the one sent from the design engineers consisting information of thousands of chips and transforming it into real-world physical motor coordinates for a testing stage.

Solution aimed at:-When a physical wafer is loaded onto a test machine, its physical position never perfectly matches the digital design file. If a wafer has thousands of chips (like a 40,000-qubit architecture), an engineer cannot manually align the machine to each one. This tool solves that by allowing the user to align the machine to just one reference chip. The script then instantly calculates the exact motor coordinates needed to find every other chip on the wafer.

Key Functions Used:
1. pd.read_csv() & to_csv(): Uses the Pandas library to instantly load and export massive datasets (like a 5000+ row Excel sheet) without slowing down the computer.
2. str.contains(): A search function used to quickly scan the massive dataframe and pinpoint the exact design coordinates of the user's chosen "Homechip."
3. random.uniform(): Used in this demonstration to simulate the physical X and Y coordinates read from the stage motors.
4. iterrows() & .loc[]: Iterates through the entire wafer map to apply the physical offset to every single chip and save the new values in dedicated columns.
