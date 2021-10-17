# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 14:58:58 2021

@author: GE73VR 7RF
"""

# from automaticScan import *
# from combineXYZ import *

from automationHelper import *

# INPUT: 

startIndex = int(input("\nStart index: "))

bridgeNumber = int(input("Number of bridges: "))

isSame = input("Do the bridges have the same environment[y/n]: ")
isSame == "y" 

verbose = input("Verbose[y/n]: ")
verbose == "y"


# # MANUALLY:

# startIndex = 1
# bridgeNumber =  2
# isSame = True
# verbose = True



for i in range (startIndex,startIndex+bridgeNumber):
    bridgeName = "bridge" + str(i)
    print("\nProccessing bridge"+str(i)+"...\n")
    automaticScan (bridgeName,isSame,startIndex,verbose)
    print("\nScaning of bridge"+str(i)+" is complete!\n")
    combineXYZ(bridgeName,isSame,startIndex)
    print("\nCombining of xyz files of bridge"+str(i)+" is complete!\n")