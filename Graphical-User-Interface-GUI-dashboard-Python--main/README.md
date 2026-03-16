# Graphical-User-Interface-GUI-dashboard-Python-tkinter

Project Overview:- In an R&D lab, physicists and hardware engineers need reliable tools to run tests without having to dig into messy backend code and have mutliple GUIs for hardware interaction.This project uses tkinter library of python programming language to build a Graphical User Interface (GUI) dashboard capable of accomodating mutiple user defined test operations.It acts as a digital control panel for automated wafer testing, designed to simulate the alignment of a motorized stage and the execution of optoelectronic sweeps.

Key Functions Used:
1. Object Oriented Architecture (class Wafertester): The entire GUI is wrapped in a single class. This is crucial for scalability, allowing other engineers to easily add new instruments or frames later without breaking the code.

2. update_instruments(): Utilizes a recursive .after() loop to simulate real-time, continuous data streaming (simulating a stage position in mm and a photodetector reading in mA) without freezing the user interface.

3. handle_user_entry(): Captures and executes custom user inputs for stage alignment coordinates.

4. Test Functions: manage the active/idle states of specific test routines (like LIV and Spectral Analysis).

Result:- tool proves the ability to translate complex hardware testing requirements into a scalable,accessible, production-ready GUI for testing team 
