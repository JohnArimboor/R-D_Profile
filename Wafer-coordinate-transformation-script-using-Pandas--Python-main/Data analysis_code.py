# -*- coding: utf-8 -*-
"""
@author: John Arimboor
"""


#**********************************************#
# Wafer coordiante transformation script using Pandas- Python
# The Problem:= Design and Process engineer deal with massive excel sheet with various informatin of the chips which almost accounts to 5000+ in number in a single wafer. 
# This details consist of spatial coordiantes of the chip , Positive and Negative contacts of the wafer and fabrication confinement layers 
# In this test recipe, the engineering team needs a way to dyanammically translate the digital map of the wafer into physical map for the stages to move by assumuing a user
#define homechip 
# 
# How to achieve  it:- 
# 1. The script loads the massive design CSV into a Pandas DataFrame.
# 2. It asks the user to pick one specific chip as a reference point (the "Homechip").
# 3. It reads the physical stage motors to see exactly where that Homechip is in real life.
# 4. It compares the real-life position to the design position to find the offset.
# 5. It applies that exact offset to every single chip in the massive DataFrame and 
#    generates a brand new CSV file with the updated, real-world stage coordinates.

import pandas as pd 
import random 

Map=pd.read_csv(r"C:\Users\John Arimboor\OneDrive\Desktop\Chip_List_One.csv")
print(type(Map))

def Homechip(ChipID,Map):
    print("The user entry is:",ChipID)

    #Ask the stages to geenerate me any random numver between 0 and 155 for x and y valyes 
    GetPosX= round(random.uniform(0.0, 155.0), 1)
    GetPosY=  round(random.uniform(0.0, 155.0), 1)
    print(GetPosX)
    print(GetPosY)
    #Update new coloumns withing the dataframe 
    Map['Pix_upd']=0
    Map['Piy_upd']=0
    
    # Try to find the user's home chip amnong the list and find the correspoinding x and y values 
    homechip=(Map[Map['Chip_ID'].str.contains(ChipID)])
    print(homechip)
    HomeX=float(homechip["Wafer_X_Loc_mm"])
    print(HomeX)
    HomeY=float(homechip["Wafer_Y_Loc_mm"])
    print(HomeY)
    
    # Chaning the values of all x and y values of all the chips according to the homechip inbto a new coloumns
    for index,row in Map.iterrows():
        Map.loc[index,"Pix_upd"]=float(GetPosX + ((Map.loc[index,"Wafer_X_Loc_mm"])-HomeX)) 
        Map.loc[index,"Piy_upd"]=float(GetPosY + ((Map.loc[index,"Wafer_Y_Loc_mm"])-HomeY))
    #print the updated dataframe with new Pix and Piy values 
    print("Updated Dataframe",Map)
    print("Home chip updated in datafram and stage valaues generated ")
    #Converting the data back to csv 
    Map.to_csv("mapnew1.csv", index=False) #Generating a new physical world for stage movement map 
    
    
Home_ChipID=str(input("Enter the ChipID to be assigned as Homechip:"))
# print(ChipID)   
Homechip(Home_ChipID,Map) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

#Function that asks user to assign the homechip and updates the entire dataframe with new set of stage values 
# Function that asks for the chip ID from the user, updates the values in the dataframe and share the map as an object within the tkinter 
# def homechip(self,ChipID):
#     print("The entry is:",ChipID)
#     ChipX=SC.GetPos(Config,"X0")[0]
#     ChipY=SC.GetPos(Config,"Y0")[0]
#     Map1=self.Map
#     Map1['Pix_upd']=0
#     Map1['Piy_upd']=0
    
#     homechip=(Map1[Map1['ChipID'].str,contains(ChipID)])
#     HomeX=float(homechip["x(um)"])
#     HomeY=float(homechip["y(um)"])
    
    
#     for index,row in Map1.iterrows():
#         Map1.loc[index,"Pix_upd"]=float(ChipX + (0-((Map1.loc[index,"x(um)"])-(HomeX))/1000)) # WOnt be requiring to show zero here
#         Map1.loc[index,"Piy_upd"]=float(ChipY + (((Map1.loc[index,"y(um)"])-(HomeY))/1000))
    
#     print("Updated Dataframe",Map1)
#     print("Home chip updated in datafram and stage valaues generated ")
#     self.Mapnew=Map1
#     M=self.Mapnew
#     Map1.to_csv("map1.csv", index=False)
    
#     return self.Mapnew    
    
