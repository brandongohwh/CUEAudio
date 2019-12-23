# -*- coding: utf-8 -*-

import os
import time
import subprocess
import shutil
from datetime import datetime
import sys
import filecmp

#For mp3
import platform
import struct

#Constants
#1 for MP3 conversion (will delete WAV), 0 for WAV
mp3=0

#For option selection
import argparse
parser = argparse.ArgumentParser(description='CUE! Audio Puller')
parser.add_argument('-o', help="Specify output folder", dest='Out')
parser.add_argument('-a', help='Android application name', dest='AName')
parser.add_argument('-init', action='store_true', dest='init', help="Emulate initial pull, extracts all current and previous files")
parser.add_argument('-c', action='store_true', dest='conv', help='Converts extracted WAV to MP3')
parser.add_argument('-d', action='store_true', dest='Del', help='Deletes WAV')
parser.add_argument('-p', type=int, help="Port number for ADB, applies to NoxPlayer")

args = parser.parse_args()


icon='''
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((/*,..                   .,*//(((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((/,.   .*//(((((((((((((((((((((((((/*.   .*(((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((/,.  ,*(((((((((((((((((((((((((((((((((((((((((/,.  */(((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((*  .,((((((((((((((((((((((((((((((((((((((((((((((((((((/,  *((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((*  ./((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((*. .(((((((((((((((((((((((((
(((((((((((((((((((((((((((((((((((. .*(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((/  *((((((((((((((((((((((
(((((((((((((((((((((((((((((((/. ./(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((, ,((((((((((((((((((((
(((((((((((((((((((((((((((((. ./((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((* ,((((((((((((((((((
(((((((((((((((((((((((((((((/(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((,,(((((((((((((((((
((((((((((((((((((((((((((/,.        ,*(((((((//////////(((((((((((((//////////(((((///////////////////////((((((//////////(((((((((
(((((((((((((((((((((/,                   *((/          /(((((((((((/          ((((/                       (((((*          (((((((((
(((((((((((((((((((.                       /(.         ,((((((((((((,         .((((.                      .(((((.         ,(((((((((
((((((((((((((((/                        /(((          /(((((((((((/          *((((                       *((((/          /(((((((((
((((((((((((((/                        *((((/          ((((((((((((*         .((((/                      .(((((,         .((((((((((
(((((((((((((.             ,*/(//*.  ,((((((,         .((((((((((((.         *((((,         .((((((((((((((((((          /((((((((((
((((((((((((.           *((((((((((((((((((/.         *((((((((((((          /(((/          *(((((((((((((((((/          (((((((((((
(((((((((((           *((((((((((((((((((((*         .((((((((((((/          ((((*         .((((((((((((((((((*         .(((((((((((
((((((((((*          ((((((((((((((((((((((.         *((((((((((((.         ,((((.                     /((((((.         *(((((((((((
(((((((((/          /((((((((((((((((((((((          /(((((((((((/          /((((                      ((((((*          /(((((((((((
(((((((((,         .((((((((((((((((((((((/          ((((((((((((,         .((((/                     .((((((.         ,((((((((((((
(((((((((,          /(((((((((((((((((((((,         ,((((((((((((          /((((,                     *((((((          /((((((((((((
(((((((((,          .(((((((((((((((((((((.         ,(((((((((((*          ((((/          /(((((((((((((((((((((((((((((((((((((((((
(((((((((/           ./(((((((((((((((((((.          /((((((((/           /((((,         .((((((((((((((((((((*.   .*(((((((((((((((
((((((((((*              ,*//*.   .(((((((,            .*//,.            /(((((          *(((((((((((/  ,((/          *(((((((((((((
((((((((*((.                       ,(((((((                            ./((((((                    /(.  /(*            (((((((((((((
(((((((/ /((*                        (((((((((/                       *(((((((*                    ((  ,(/             (((((((((((((
(((((((/ /(((/,                      ./((((  .(/                   ./(((((((((.                   ,(*  /(/            *(((((((((((((
(((((((/ /((((((/                  ,/((((((*  *(,               ./(((((((((((/                    //   (((*         .(((((((((((((((
(((((((/ *((((((((((/*,.    .,*/((((((((((((.  ((((*,.    .,*((((((((((((((((((((((((((((((((((((((,  ,(((((/.  .,/(((((((((((((((((
((((((((,.((((((((((((((((((((((((((((((/*,.      /((((((((((((((((((((((((((((((((((///**,,,*(((((   /((((((((((((. /((((((((((((((
((((((((/ *(((((((((((((((((((((((((*  .,//((  .((((((((((((((((((((((((/*,..      ..,,*/////(((((*  *(((((((((((* ,((((((((((((((((
(((((((((. ((((((((((((((((((((((((((/(((((((.  *,.    ,((((((((((*     .,*/((((((((((((((((((((((.  ((((((((((/ ./(((((((((((((((((
(((((((((/ *(((((((((((((((((((((((((((/*.      ./(((((((*,,*(((((///((((((((((((((((((((((((((((/   ((((((((* ./(((((((((((((((((((
((((((((((/ ,((((((((((((((((((((/,    ,*/((((.  (((((/  */.  /((((((((((((((((((((((((((((((((((///(((((((. ,((((((((((((((((((((((
(((((((((((* *((((((((((((((/,   ,/(((((((((((/  *(((((//((   ///,,*(((((((((((((((((((((((((((.  .  /((*  /((((((((((((((((((((((((
((((((((((((( .((((((((((,   *(((((((((((((((((.  /((((((*.   .*/((((((((((((((((((((((((((((/  .(.  ((**(((((((((((((((((((((((((((
((((((((((((((, /((((((.  /((((((((((((((((((((/   ((/.  ,/((((((((((((((((((((((((((((((((((,      /(((((((((((((((((((((((((((((((
(((((((((((((((* ,(((((((((((((((((((((((((((((((//((///((((((((((((((((((((((((((((((((((((((* .(((((((((((((((((((((((((((((((((((
(((((((((((((((((, ,(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((/,  /((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((* ./((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((*.  */(((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((/. ,((((((((((((((((((((((((((((((((((((((((((((((((((((((((((/*/((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((/  ,/(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((((((((/,  */(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((((((((((((/,  .*/((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((/*.   .,*/(((((((((((((((((((((/*,.    ,((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((//*,.  ,/(((((((((*.  .*/(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((((((((((((((((((((((((((((((((/ ,(((((. ./(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((/ *(/  /((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((( ,  (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((/  /((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((((((((((((((((((((((((((((((((/ .((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((/(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
'''

warning='''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@%########(((((((((((########%&@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%####(/****************************//(####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@%###(/*****************************,,,,,,,,,,*/###%@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##(/***************************,,,,,,,,,,,,,,,,,,,,*(##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%##(/**************************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*/##%@%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%@##(/**************************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*(##%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%@##(**************************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,/##&%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%##**************************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,(##%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%@##**************************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,(#%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%##/*************************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*##%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%@##/************************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*##%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%##************************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,(#%%%%%%%%%%%%%%
%%%%%%%%%%%%##/***********************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,##@%%%%%%%%%%%
%%%%%%%%%%%##/***********************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,##&%%%%%%%%%%
%%%%%%%%%@##/**********************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,(#%%%%%%%%%%
%%%%%%%%(**********************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,(#%%%%%%%%%
%%%%%%%%##**********************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,##%%%%%%%%
%%%%%%%##/********************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*##%%%%%%%
%%%%%%%#/********************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*#%%%%%%%
%%%%%%##*******************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,(#%%%%%%
%%%%%##/******************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*##%%%%%
%%%%%##*****************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,##%%%%%
%%%%%#(****************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,(%#%%%%
%%%%%#%#(/************,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*/#%#%%%%
%%%%###%%%%%%#(/*****,,,,,,,,,,,,,,,,,,,,,,,/(,,,,,,,,*(/,,,,,/(***(/**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,**/((#%%%%%%%%#@%%%
%%##*****/(#%%%%%%%##(/*,,,,,,,,,,,,,,,,#%###(((%#*,/#%((%#*,/#(#(/#/#(,,,,,,,,,,,,,,,,,,,**/((##%%%%%%%%%##(/*,,,/##@%
##**************//(##%%%%%%%%%%##(((//*,///%#////**#%##%%###/,/((#%##%/,/((((####(*#%%%%%%%%%%##((/*,,,,,,,,,,,,,,,,*##
#(***************,,,,,,,**/((###%%%%%%#*((%#//%%//,,(##%%#(,,,#%(#%#((/,*/***,,,**,/((/***,,,,,,,,,,,,,,,,,,,,,,,,,,,/#
%##(*************,,,,,,,,,,,,,,,,,,,,,,,,,(%%%%(*,,,**/%#****,(#%%%/*(%*,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*(#%
%%%%###(/*******,,,,,,,,,,,,,,,,,,,,,,,,,,,**,,,*,,/********,,**,*/*,*,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*(###%%%
%%%%%%%##%%#(/,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*/#%%##%%%%%%
%%%%%@##,(%#%(*/(##(/*,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,*/(###/**%##%//##%%%%%
%%%%@##,,/%###,,,,,,,*/(###((/**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,**/((###(/*,,,,,,,/%###*,/##%%%%
%%%%#/,,,/%##%*,,,,,,,,,,,,,*#,**/((##%##((///****,,,,,,,,,,,,,,,,,,,****///((#####(/*,...#/,,,,,,,,,,,,,#%#%#/,,,(#%%%
%%##((#%//%##%#*,,,,,,,,,,,,*#((///(#%%(*,,(#,    ./(/..............      .,/##(/***//*,  #/,,,,,,,,,,,,*%##%%//##(###%
%%%%%%##,,%%##%(,,,,,,,,,,,,,#,,,,/#,,#,(#/                                               #*,,,,,,,,,,,,#%##%#*,/##%%%%
%%%%%%#/,,(%##%#,,,,,,,,,,,,,(#((,. .(#*.                                                .(,,,,,,,,,,,,(%##%%/,,,(#%%%%
%%%%%##,,,*%%##%(,,,,,,*,,,,,*(.                                                         (*,,,,,*,,,,,*%###%#,,,,,#%%%%
%%%%%#/,,,,(%###%*,,,,,#(#(//*#/                                                        ,%**/(#(#*,,,,#%##%%*,,,,,(#&%%
%%%%#(*,,,,,/%##%#***,,#*,(*...                                                          ....(/*#*,**/%###%/,,,,,,*##%%
%%%%#*,,,,,,,#%##%%#*(##*,(*                                                                .#/*##/,/%###%*,,,,,,,,(#%%
%%%##,,,,,,,,*%%##%#,,,,,,((.                                                               /%/,,,,,*###%(,,,,,,,,,/#%%
%%%#(,,,,,,,,,*###%(,,,,,,/%(.*((.                                                    *(/, .##*,,,,,*##%#,,,,,,,,,,*(#%
%%%#/,,,,,,,,,,*%#%(,,,,,,*%%&&&&&*,.       ,*#,                      ((*.       .*(%&&&&&%%((,,,,,,*#%#/,,,,,,,,,,,(#%
%%%#/,,,,,,,,,,,/%%#,,,,,,,##(#&&&&&&&&&%%%%&&&%,                      #&&&%%%%&&&&&&&&&%/*(//,,,,,,*##/*,,,,,,,,,,,(#%
%%%#/,,,,,,,,,,,,/##,,,,,,,(##. ./#%&&&&&&&&%(.                          *#%&&&&&&&&%#*.  #/(,,,,,,,/#/*,,,,,,,,,,,,(#%
%%%#(,,,,,,,,,,,,*/#,,,,,,,*#(*     .,%(,....                               ...*#/........(/(,,,,,,,/#/,,,,,,,,,,,,*##%
%%%%#,,,,,,,,,,,,,*#*,,,,,,,*%(.   ..........                                ............/%%*,,,,,,,(#*,,,,,,,,,,,,(#%%
%%%%#(,,,,,,,,,,,,,(/,,,,,,,,(%(    .........                                  ........ .%#/,,,,,,,,#/,,,,,,,,,,,,*##%%
%%%%%#(,,,,,*/,,,,,*#,,,,,,,,,#%,     .....                                       ..   ./%/,,,,,,,,*#*,,,,*(,,,,,,##%%%
%%%%%%##,,,,,##(,,,,#*,,,,,,,,,(%.                                                    .#%/,,,,,,,,,#*,,,,#%(,,,,/##%%%%
%%%%%%%##(,,,*###/,,*#*,,,,,,,,,#%(.                    ... ....                     ,#%(,,,,,,,,,*#,,*###(*,,,(#%%%%%%
%%%%%%%%%##(*,*####(,/#,,,,,,,,,,(%%(,              .**..       .*/.              ./%%%*,,,,,,,,,,#,/####(,,*##%%%%%%%%
%%%%%%%%%%%%###(###%####*,,,,,,,,,,/%%%%(*.                                  .,/#%#%#/,,,,,,,,,,(###%%##((###%%%%%%%%%%
%%%%%%%%%%%%%%%####%%%%##(,,,,,,,,,,,*#%%%%%%#/*.                      .,/#%%%#%%%(,,,,,,,,,,,,##%%%%%###%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%##/,,,,,,,,,,,,,*(%%#%%%%%%##(////////*/((#%%%%%##%%#/,,,,,,,,,,,,,,(#%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%###(*,,*%#####(%%###%%%%%%%#%%&@&&@&&%#%%%%%%%####%%%####%%,,,*###%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###((###%%##%##########%#(#%%%%#((#%##########%%##%##((####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''
print("%s\nWelcome to CUE! Audio puller!"%icon)
#print(sys.argv)

#Must change running directory or else there'll be an error
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#Get existing folders
ori=os.getcwd()

def PreProcessing(val):
    folders= []
    for r, d, f in os.walk(os.path.join(os.getcwd(),'ProcessingFolder')):
        for folder in d:
            folders.append(os.path.join(r, folder))
    
            
    for f in folders:
        for fi in os.listdir(f):
            if os.path.splitext(fi)[1].lower() == '.wav':
                if val==0:
                    print("%s\nThere are still .wav files in ProcessingFolder folder, program will terminate!"%warning)
                    print("To make this error disappear, remove all .wav files from the ProcessingFolder folder\n")
                elif val==1:
                    print("%s\nThe program is unable to copy all the .wav files into the destination folders.")
                    print("Please remove all .wav files from the ProcessingFolder folder before next execution\n")

                sys.exit(0)
    
    subprocess.call([os.path.realpath(os.path.join(os.getcwd(),'CleanFolder.bat'))])

def ADBexec(init=0):   
    folders = []
    
    for r, d, f in os.walk(os.path.join(os.getcwd(),'Sound')):
        for folder in d:
            if os.listdir(os.path.join(r,folder)):
                folders.append(os.path.join(r, folder))
            
    # !Make sure working directory reset since Python messes up things
    os.chdir(ori)
        
    # Update latest files by pulling from phone/emulator
    # I am not going to make sure it calls adb connect 5555 / 62001 (Nox) first
    # Edit the adbpull.bat if necessary
    print("Starting ADB in ")
    for i in range(5,0,-1):
        print(i)
        time.sleep(1)
    subprocess.call([os.path.realpath(os.path.join(os.getcwd(),'adbpull.bat'))])
        
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    g=open(os.path.join(ori,'updatedfolder.log'),'a+')
    
    g.write("Update time: "+dt_string)
    g.write("\n-------------------------------------------------------------------------------------------------------------------------\n")
    g.write("Changed Folders:\n")

    if init:
        folderpost= []
        for r, d, f in os.walk(os.path.join(os.getcwd(),'Sound')):
            for folder in d:
                if os.listdir(os.path.join(r,folder)):
                    folderpost.append(os.path.join(r, folder))
        if len(folderpost):
            for s in folderpost:
                g.write(s)
                g.write("\n")
                print(s)
        else:
            g.write("<NIL>\n")
        g.write("-----------------------------------------------\n")
                
    else:
        # Gets updated folders only
        folderpost= []
        for r, d, f in os.walk(os.path.join(os.getcwd(),'Sound')):
            for folder in d:
                if os.listdir(os.path.join(r,folder)) and os.path.join(r,folder) not in folders:
                    folderpost.append(os.path.join(r, folder))
        
        if len(folderpost):
            for s in folderpost:
                g.write(s)
                g.write("\n")
                print(s)
        else:
            g.write("<NIL>\n")
        g.write("-----------------------------------------------\n")
    
    g.write("Files added:\n")
    # For new folders, locate awb/acb and place them in the same folder
    
    if len(folderpost):
        for f in folderpost:
            for fi in os.listdir(f):
                if os.path.splitext(fi)[1].lower() in ['.awb','.acb']:
                    print(os.path.join(f,fi))
                    g.write(os.path.join(f,fi))
                    g.write("\n")
                    if not os.path.isdir(os.path.join(ori,'Processingfolder',os.path.basename(os.path.join(f,os.path.splitext(fi)[0])),'')):
                        os.mkdir(os.path.join(ori,'Processingfolder',os.path.basename(os.path.join(f,os.path.splitext(fi)[0])),''))
                    shutil.copy(os.path.join(f,fi),os.path.join(ori,'Processingfolder',os.path.basename(os.path.join(f,os.path.splitext(fi)[0])),''))
    else:
        g.write("<NIL>\n")
    
    #End init block 
    os.chdir(ori)
    g.write("-------------------------------------------------------------------------------------------------------------------------\n")
    g.flush()
    g.close()

def ACB2WAV():
    subprocess.call([os.path.realpath(os.path.join(os.getcwd(),'ACB2WAVlong.bat'))])
    
    print("Extracted WAV files now in %s"%os.path.join(ori,'CopiedWAV',''))


def copyF(fol):
    for f in os.listdir(os.path.join(ori,'ProcessingFolder')):
        for r,d,f2 in os.walk(fol):
            if f in d:
                for r2,d2,f3 in os.walk(os.path.join(ori,'ProcessingFolder',f)):
                    for f4 in f3:
                        if os.path.splitext(f4)[1].lower() in ['.wav']: 
                            x=1
                            if os.path.exists(os.path.join(r,f,f4)):
                                if filecmp.cmp(os.path.join(r,f,f4),os.path.join(r2,f4)):
                                    os.remove(os.path.join(r2,f4))
                                else:
                                    while True:
                                        if not os.path.exists(os.path.join(r,f,os.path.splitext(f4)[0])+'('+str(x)+')'+os.path.splitext(f4)[1]):
                                            shutil.move(os.path.join(r2,f4),os.path.join(r,f,os.path.splitext(f4)[0])+'('+str(x)+')'+os.path.splitext(f4)[1])
                                            break
                                        x+=1
                            else:
                                shutil.move(os.path.join(r2,f4),os.path.join(r,f,f4))

def updateFolder(src,dst):
    for i in os.listdir(src):
        if os.path.isdir(os.path.join(src,i)) and len(i)<40:
            if not os.path.exists(os.path.join(dst,i)):
                os.makedirs(os.path.join(dst,i))
                print(os.path.join(dst,i))
            updateFolder(os.path.join(src,i),os.path.join(dst,i))

def extractfolder(fol,fpath=False):
    if fpath==False:
        if not os.path.exists(os.path.join(ori,fol)):
            os.mkdir(os.path.join(ori,fol))
    else:
        os.makedirs(fol)

PreProcessing(0)
os.chdir(ori)
ADBexec()
ACB2WAV()
fol='Extracted'
extractfolder(fol)

#extractFolder -> Create root extraction folder
#updateFolder -> Create sub-directory extraction folder
if args.Out==False:
    extractfolder(fol)
    updateFolder(os.path.join(ori,'Sound'),os.path.join(ori,fol))
    copyF(os.path.join(ori,fol))
else:
    if platform.system()=="Windows":
        if ":" in args.Out:
            extractfolder(args.Out,True)
            updateFolder(args.Out,os.path.join(ori,fol))
            copyF(args.Out)
        else:
            extractfolder(args.Out) 
            updateFolder(os.path.join(ori,args.Out),os.path.join(ori,fol))
            copyF(os.path.join(ori,args.Out))
PreProcessing(1)

if (args.conv):
    if platform.system()=="Windows":
        if (struct.calcsize("P") * 8)==64: #32 for 32-bit & 64 for 64-bit
            subprocess.call([os.path.realpath(os.path.join(os.getcwd(),'MP3Conv64.bat'))])
        elif (struct.calcsize("P") * 8)==32:
            subprocess.call([os.path.realpath(os.path.join(os.getcwd(),'MP3Conv.bat'))])
        if (args.Del):
            subprocess.call([os.path.realpath(os.path.join(os.getcwd(),'delWAV.bat'))])
    elif platform.system()=="Darwin":
        #Install lame on Mac
        pass #For mac
    elif platform.system()=="Linux":
        #Install lame on linux
        pass #For Linux