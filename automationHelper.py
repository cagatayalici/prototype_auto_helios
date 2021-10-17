# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 10:11:06 2021

@author: GE73VR 7RF
"""

import os 
from xml.dom import minidom
import codecs
import subprocess,shlex
import os


def combineXYZ (bridgeName,isSame,startIndex):
    
    print("\nCombining xyz files of" + bridgeName + "...\n")

    basefilePath = os.getcwd()
    completePath =  os.path.join(basefilePath, "output\\Survey Playback\\")
    textFile = bridgeName + "_combined.txt"
    outputFilePath = os.path.join(basefilePath, "output\\combined",textFile)
    os.chdir(completePath)
    
    components = ["abutments","deck","piers","railings","environment"]
    
    writeFile = open(outputFilePath, "w")
    
    for component in components:
        
        if(component == "environment" and isSame):
            fileName = "bridge" + str(startIndex) + "_" + component + "_survey"
        else:
            fileName = bridgeName + "_" + component + "_survey"
        targetPath =  os.path.join(completePath, fileName)
        os.chdir(targetPath)
        
        if(component == "abutments" ):
            label = 0
        elif(component == "piers" ):
            label = 1
        elif(component == "deck" ):
            label = 2
        elif(component == "railings"):
            label = 3
        elif(component == "environment"):
            label = 4
        
        
        for file in os.listdir():
            
            readPath =  os.path.join(targetPath,file,"points\\")
            os.chdir(readPath)
         
            for file in os.listdir():
                if file.endswith(".xyz"):
                    inputFile =  open(file)
                    
                    for line in inputFile:
                        coordinates =  line.split()[0:3]
                        L = [coordinates[0] + ' ' +  coordinates[1] + ' ' + coordinates[2] + ' '+ str(label) + "\n"]
                        writeFile.writelines(L)
                        
                    inputFile.close()
            
    writeFile.close()  
    os.chdir(basefilePath)

def autoRun (command, verbose = True):
    
    basefilePath = os.getcwd()
    os.chdir(basefilePath)
    
    if verbose == True:    
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, text=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print (output.strip())
                rc = process.poll()
    else:
        process = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, text= True)
        print(process.stdout)
        rc = 1

    return rc


def editXML (bridgeName, typeOfXML, component):
    
    basefilePath = os.getcwd()
    
    if typeOfXML == "scene":
    
        sceneFile = "data\\scenes\\projects\\dataset"
        completeFilePath = os.path.join(basefilePath, sceneFile)
        os.chdir(completeFilePath)
        
        file = minidom.parse('bridge_scene.xml')
        # filters = file.getElementsByTagName('filter')
        parameters = file.getElementsByTagName('param')
        
        bridgeNumber = bridgeName.replace("bridge","")
    
        parameters[0].attributes["value"].value = "data/sceneparts/projects/dataset/" + bridgeNumber + "/" + bridgeName + "_" + component +".obj"
        
        f = codecs.open('bridge_scene.xml', mode='w', encoding='UTF-8')
        file.writexml(f, encoding="UTF-8")
        f.close()
        
    elif typeOfXML == "survey":
        
        bridgeNumber = bridgeName.replace("bridge","")
        surveyFile = "data\\surveys\\projects\\dataset\\" + bridgeNumber
        completeFilePath = os.path.join(basefilePath, surveyFile)
        os.chdir(completeFilePath)
        
        if (component == "environment"):
            
             file = minidom.parse(bridgeName + "_environment_survey_airplane.xml")
             surveys = file.getElementsByTagName('survey')
             surveys[0].attributes["name"].value = bridgeName + "_environment_survey"
             f = codecs.open(bridgeName + "_environment_survey_airplane.xml", mode='w', encoding='UTF-8')
             file.writexml(f, encoding="UTF-8")
             f.close()
             
             file = minidom.parse(bridgeName + "_environment_survey_tripod.xml")
             surveys = file.getElementsByTagName('survey')
             surveys[0].attributes["name"].value = bridgeName + "_environment_survey"
             f = codecs.open(bridgeName + "_environment_survey_tripod.xml", mode='w', encoding='UTF-8')
             file.writexml(f, encoding="UTF-8")
             f.close()
             
        else:
            
            file = minidom.parse(bridgeName + "_bridgeComponents_survey.xml")
            surveys = file.getElementsByTagName('survey')
            surveys[0].attributes["name"].value = bridgeName + "_" + component + "_survey"
            f = codecs.open(bridgeName + "_bridgeComponents_survey.xml", mode='w', encoding='UTF-8')
            file.writexml(f, encoding="UTF-8")
            f.close()
                 
    os.chdir(basefilePath)
    
    
       
def runHelios(bridgeName,component, verbose = True):
    
    bridgeNumber = bridgeName.replace("bridge","")
    surveyNames = ["bridgeComponents_survey.xml","environment_survey_airplane.xml","environment_survey_tripod.xml"]
    
    if ( component == "abutments" or component == "deck" or component == "piers" or component == "railings"):
        command = "helios.exe data/surveys/projects/dataset/" + bridgeNumber + "/" + bridgeName + "_" + surveyNames[0]
        autoRun(command,verbose)
        
    elif (component == "environment"):
        command = "helios.exe data/surveys/projects/dataset/" + bridgeNumber + "/" + bridgeName + "_" + surveyNames[1]
        autoRun(command,verbose)
            
        command = "helios.exe data/surveys/projects/dataset/" + bridgeNumber + "/" + bridgeName + "_" + surveyNames[2]
        autoRun(command,verbose)
    


def automaticScan (bridgeName,isSame,startIndex,verbose = True):

    components = ["abutments","deck","piers","railings","environment"]
    
    for component in components:
        print("\nscaning " + component + "...")
        
        if( (component == "environment") and (bridgeName != "bridge" + str(startIndex))):
            if (not isSame):
                editXML(bridgeName,"scene",component)
                editXML(bridgeName,"survey",component)
                runHelios(bridgeName,component,verbose)
        else:
            editXML(bridgeName,"scene",component)
            editXML(bridgeName,"survey",component)
            runHelios(bridgeName,component,verbose)
            



            
            
        