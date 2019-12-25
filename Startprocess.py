# -*- coding: utf-8 -*-

#Package section
import os
import time
import subprocess
from subprocess import PIPE
import shutil
from datetime import datetime
import sys
import filecmp
import platform
import struct
import argparse
import shutil

# String section
# postfix:
# AI: Already implemented
# NI: Not implemented
p1NI="""====================================================================================
Phase 1:
Wine has not been detected on the system, preparing to install.
Provide sudo password if prompted!
Commencing installation in 10s.
====================================================================================
"""
p1AI="""====================================================================================
Phase 1: Wine already installed on system!
"""
p2NI="""====================================================================================
Phase 2:
Winetricks has not been detected on the system, preparing to install.
Provide sudo password if prompted!
Commencing installation in 10s.
====================================================================================
"""
p2AI="""Phase 2: Winetricks already installed on system!
"""
p3NI="""====================================================================================
Phase 3:
Initiating installation of .NET Framework 4.5, follow instructions on screen.
====================================================================================
"""
p3AI="""Phase 3: .NET Framework 4.5 already installed on system!\n"""
p4NI="""====================================================================================
Phase 4:
Lame has not been detected on the system, preparing to install.
Provide sudo password if prompted!\nCommencing installation in 10s.
====================================================================================
"""
p4AI="""Phase 4: Lame already installed on system!
===================================================================================="""
pOK="""
Pre-requisite check complete!
===================================================================================="""
sudoProb="""
====================================================================================
You may need to add your username to the sudoers file!

Run the following command:
su
visudo

On the last line, add '<username> ALL=(ALL) ALL'

Save and quit by pressing ESC, then typing in ':wq' and hit ENTER.

Restart your system to have the changes take effect.
===================================================================================="""
noSup="""

====================================================================================
Support for Linux/Mac is not available yet!
===================================================================================="""
welcome="%s\nWelcome to CUE! Audio puller!\n"
warningpre1="%s\nThere are still .wav files in ProcessingFolder folder, program will terminate!"
warningpre2="To make this error disappear, remove all .wav files from the ProcessingFolder folder\n"
warningpost1="%s\nThe program is unable to copy all the .wav files into the destination folders."
warningpost2="Please remove all .wav files from the ProcessingFolder folder before next execution\n"
icon = '''
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

warning = '''
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

# Initialisation section (IMPORTANT: DO NOT MOVE)
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

## Root dir
ori = os.getcwd()

# Variables section
sudoAPT=['sudo', 'apt', 'install']
sudoNoPrompt=['-y']

# Program argument section
parser = argparse.ArgumentParser(description='CUE! Audio Puller')
parser.add_argument(
    '-o', help="Specify output folder (Not tested yet, use at own risk!)", dest='Out')
parser.add_argument(
    '-a', help='Android application name (Not implemented yet)', dest='AName')
parser.add_argument('-init', action='store_true', dest='init',
                    help="Emulate initial pull, extracts all current and previous files")
parser.add_argument('-c', action='store_true', dest='conv',
                    help='Converts extracted WAV to MP3')
parser.add_argument('-d', action='store_true', dest='Del', help='Deletes WAV')
parser.add_argument(
    '-p', type=int, help="Port number for ADB, applies to Bluestacks/NoxPlayer (Not yet implemented)")
parser.add_argument('-n', action='store_true', dest='nat',
                    help='Use Native apps where available (Only Ubuntu)')

args = parser.parse_args()

# Function section
def PreProcessing(val):
    folders = []

    if os.path.exists(os.path.join(ori, 'ProcessingFolder')):
        for r, d, f in os.walk(os.path.join(os.getcwd(), 'ProcessingFolder')):
            for folder in d:
                folders.append(os.path.join(r, folder))

    for f in folders:
        for fi in os.listdir(f):
            if os.path.splitext(fi)[1].lower() == '.wav':
                if val == 0:
                    print(warningpre1 % warning)
                    print(warningpre2)
                elif val == 1:
                    print(warningpost1 % warning)
                    print(warningpost2)
                sys.exit(0)

    if os.path.exists(os.path.join(ori, 'ProcessingFolder')):
        shutil.rmtree(os.path.join(ori, 'ProcessingFolder'))
    os.makedirs(os.path.join(ori, 'ProcessingFolder'))

def ADBexec(init=0):
    folders = []

    if not init:
        for r, d, f in os.walk(os.path.join(os.getcwd(), 'Sound')):
            for folder in d:
                if os.listdir(os.path.join(r, folder)):
                    folders.append(os.path.join(r, folder))

    # !Make sure working directory reset since Python messes up things
    os.chdir(ori)

    # Update latest files by pulling from phone/emulator
    # I am not going to make sure it calls adb connect 5555 / 62001 (Nox) first

    print("Starting ADB in: ")
    for i in range(5, 0, -1):
        print(i, end='\r')
        time.sleep(1)
    print(0,end='\n\n')

    if platform.system() == 'Windows':
        x = subprocess.call([os.path.join(os.getcwd(), 'platform-tools', 'win', 'adb.exe'), 'pull',
                             "/sdcard/Android/data/jp.co.liberent.cue/files/UnityCache/Shared/Sound/.", os.path.realpath(os.path.join(os.getcwd(), 'Sound'))])
        if x:
            t = 3
            for i in range(t):
                print(
                    "(Attempt %d of %d) You may need to authorise ADB to access your Android device! Waiting for 5 seconds." % (i+1, t))
                time.sleep(5)
                x = subprocess.call([os.path.join(os.getcwd(), 'platform-tools', 'win', 'adb.exe'), 'pull',
                                     "/sdcard/Android/data/jp.co.liberent.cue/files/UnityCache/Shared/Sound/.", os.path.realpath(os.path.join(os.getcwd(), 'Sound'))])
                if not x:
                    break

    elif platform.system() == 'Darwin':
        x = subprocess.call([os.path.join(os.getcwd(), 'platform-tools', 'mac', 'adb'), 'pull',
                             "/sdcard/Android/data/jp.co.liberent.cue/files/UnityCache/Shared/Sound/.", os.path.realpath(os.path.join(os.getcwd(), 'Sound'))])
    elif platform.system() == 'Linux':
        subprocess.call(
            ['chmod', '+x', os.path.join(os.getcwd(), 'platform-tools', 'linux', 'adb')])
        x = subprocess.call([os.path.join(os.getcwd(), 'platform-tools', 'linux', 'adb'), 'pull',
                             "/sdcard/Android/data/jp.co.liberent.cue/files/UnityCache/Shared/Sound/.", os.path.realpath(os.path.join(os.getcwd(), 'Sound'))])
        if x:
            t = 3
            for i in range(t):
                print(
                    "(Attempt %d of %d) You may need to authorise ADB to access your Android device! Waiting for 5 seconds." % (i+1, t))
                time.sleep(5)
                x = subprocess.call([os.path.join(os.getcwd(), 'platform-tools', 'linux', 'adb'), 'pull',
                                     "/sdcard/Android/data/jp.co.liberent.cue/files/UnityCache/Shared/Sound/.", os.path.realpath(os.path.join(os.getcwd(), 'Sound'))])
                if not x:
                    break

    if x:
        print("There is an error with ADB, program terminating!")
        sys.exit(0)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    g = open(os.path.join(ori, 'updatedfolder.log'), 'a+')

    g.write("Update time: "+dt_string)
    g.write("\n-------------------------------------------------------------------------------------------------------------------------\n")
    g.write("Changed Folders:\n")

    if init:
        folderpost = []
        for r, d, f in os.walk(os.path.join(os.getcwd(), 'Sound')):
            for folder in d:
                if os.listdir(os.path.join(r, folder)):
                    folderpost.append(os.path.join(r, folder))
        if len(folderpost):
            for s in folderpost:
                g.write(s)
                g.write("\n")
        else:
            g.write("<NIL>\n")
        g.write("-----------------------------------------------\n")

    else:
        # Gets updated folders only
        folderpost = []
        for r, d, f in os.walk(os.path.join(os.getcwd(), 'Sound')):
            for folder in d:
                if os.listdir(os.path.join(r, folder)) and os.path.join(r, folder) not in folders:
                    folderpost.append(os.path.join(r, folder))

        if len(folderpost):
            for s in folderpost:
                g.write(s)
                g.write("\n")
        else:
            g.write("<NIL>\n")
        g.write("-----------------------------------------------\n")

    g.write("Files added:\n")
    # For new folders, locate awb/acb and place them in the same folder

    if len(folderpost):
        for f in folderpost:
            for fi in os.listdir(f):
                if os.path.splitext(fi)[1].lower() in ['.awb', '.acb']:
                    print(os.path.join(f, fi))
                    g.write(os.path.join(f, fi))
                    g.write("\n")
                    if not os.path.isdir(os.path.join(ori, 'ProcessingFolder', os.path.basename(os.path.join(f, os.path.splitext(fi)[0])), '')):
                        os.mkdir(os.path.join(ori, 'ProcessingFolder', os.path.basename(
                            os.path.join(f, os.path.splitext(fi)[0])), ''))
                    shutil.copy(os.path.join(f, fi), os.path.join(
                        ori, 'ProcessingFolder', os.path.basename(os.path.join(f, os.path.splitext(fi)[0])), ''))
    else:
        g.write("<NIL>\n")
        print("No new files added!")
        sys.exit(0)

    # End init block
    os.chdir(ori)
    g.write("-------------------------------------------------------------------------------------------------------------------------\n")
    g.flush()
    g.close()

def ACB2WAV():
    for r, d, f in os.walk(os.path.join(ori, 'ProcessingFolder')):
        for l in d:
            for s in os.listdir(os.path.join(r, l)):
                if os.path.splitext(s)[1].lower() in ['.acb']:
                    if platform.system() == 'Windows':
                        subprocess.call(
                            [os.path.join(ori, 'deretore', 'Release', 'acbUnzip.exe'), os.path.join(r, l, s)])
                    elif platform.system() == 'Linux':
                        subprocess.call(['wine', os.path.join(
                            ori, 'deretore', 'Release', 'acbUnzip.exe'), os.path.join(r, l, s)])

    for r, d, f in os.walk(os.path.join(ori, 'ProcessingFolder')):
        for l in d:
            for s in os.listdir(os.path.join(r, l)):
                if os.path.splitext(s)[1].lower() in ['.hca']:
                    if platform.system() == 'Windows':
                        subprocess.call(
                            [os.path.join(ori, 'deretore', 'Release', 'hca2wav.exe'), os.path.join(r, l, s)])
                    elif platform.system() == 'Linux':
                        subprocess.call(['wine', os.path.join(
                            ori, 'deretore', 'Release', 'hca2wav.exe'), os.path.join(r, l, s)])

def copyF(fol):
    for f in os.listdir(os.path.join(ori, 'ProcessingFolder')):
        for r, d, f2 in os.walk(fol):
            if f in d:
                for r2, d2, f3 in os.walk(os.path.join(ori, 'ProcessingFolder', f)):
                    for f4 in f3:
                        if os.path.splitext(f4)[1].lower() in ['.wav']:
                            x = 1
                            if os.path.exists(os.path.join(r, f, f4)):
                                if filecmp.cmp(os.path.join(r, f, f4), os.path.join(r2, f4)):
                                    os.remove(os.path.join(r2, f4))
                                else:
                                    while True:
                                        if not os.path.exists(os.path.join(r, f, os.path.splitext(f4)[0])+'('+str(x)+')'+os.path.splitext(f4)[1]):
                                            shutil.move(os.path.join(r2, f4), os.path.join(
                                                r, f, os.path.splitext(f4)[0])+'('+str(x)+')'+os.path.splitext(f4)[1])
                                            break
                                        x += 1
                            else:
                                shutil.move(os.path.join(r2, f4),
                                            os.path.join(r, f, f4))

def updateFolder(src, dst):
    for i in os.listdir(src):
        if os.path.isdir(os.path.join(src, i)) and len(i) < 40:
            if not os.path.exists(os.path.join(dst, i)):
                os.makedirs(os.path.join(dst, i))
                print(os.path.join(dst, i))
            updateFolder(os.path.join(src, i), os.path.join(dst, i))

def extractfolder(fol, fpath=False):
    if fpath == False:
        if not os.path.exists(os.path.join(ori, fol)):
            os.mkdir(os.path.join(ori, fol))
    else:
        os.makedirs(fol)

print(subprocess.call(['sudo', 'apt', 'install', 'wine-stable','-y']))
sys.exit(0)

# Pre-req check
# https://askubuntu.com/questions/578257/how-to-get-the-package-description-using-python-apt
if 'ubuntu' in platform.platform().lower():
    import apt
    cache = apt.Cache()
    pkg1 = cache['wine-stable']
    pkg2 = cache['wine-development']
    pkg3 = cache['winetricks']
    x = 0
    if not pkg1.is_installed and not pkg2.is_installed:
        x += 1
        print(p1NI)
        time.sleep(10)
        subprocess.call(['sudo', 'apt', 'install', 'wine-stable','-y'])
    else:
        print(p1AI,end="")
    if not pkg3.is_installed:
        if not x:
            print()
            time.sleep(10)
        else:
            print(p2NI)
            time.sleep(5)
        subprocess.call(['sudo', 'apt', 'install', 'winetricks','-y'])
    else:
        print(p2AI,end="")
    f = subprocess.Popen(['winetricks', 'list-installed'], stdout=PIPE)
    a = f.communicate()
    if not ('dotnet45' in str(a)):
        print()
        time.sleep(5)
        subprocess.call(['winetricks', 'dotnet45'])
    else:
        print(p3AI,end="")
    if args.nat == True:
        pkg4 = cache['lame']
        if not pkg4.is_installed:
            print(p4NI)
            time.sleep(10)
            subprocess.call(['sudo', 'apt', 'install', 'lame','-y'])
        else:
            print(p4AI,end="")
    print(pOK)
elif platform.system() == 'Windows':
    pass
elif 'centos' in platform.platform().lower():
    #Due to sickening documentation for Fedora/CentOS/RHEL and lack of packages from default repo, going to use brute-force method
    #https://stackoverflow.com/questions/567542/running-a-command-as-a-super-user-from-a-python-script
    x=subprocess.call(['sudo','dnf','install','epel-release'])
    if x:
        print(sudoProb)
    #Edited visudo with <user> ALL=(ALL) ALL
    sys.exit(0)
else:
    print(noSup)
    sys.exit(0)

print(welcome % icon)

PreProcessing(0)
os.chdir(ori)
if args.init == False or args.init == None:
    ADBexec()
else:
    ADBexec(1)
ACB2WAV()
fol = 'Extracted'

# extractFolder -> Create root extraction folder
# updateFolder -> Create sub-directory extraction folder
if args.Out == None or args.Out == False:
    extractfolder(fol)
    updateFolder(os.path.join(ori, 'Sound'), os.path.join(ori, fol))
    copyF(os.path.join(ori, fol))
else:
    if platform.system() == "Windows":
        if ":" in args.Out:
            extractfolder(args.Out, True)
            updateFolder(args.Out, os.path.join(ori, fol))
            copyF(args.Out)
        else:
            extractfolder(args.Out)
            updateFolder(os.path.join(ori, args.Out), os.path.join(ori, fol))
            copyF(os.path.join(ori, args.Out))
PreProcessing(1)

if (args.conv):
    if args.Out == None or args.Out == False:
        for r, d, f in os.walk(os.path.join(ori, 'Extracted')):
            for l in d:
                for s in os.listdir(os.path.join(r, l)):
                    if os.path.splitext(s)[1].lower() in ['.wav']:
                        if not (os.path.splitext(s)[0]+'.mp3') in os.listdir(os.path.join(r, l)):
                            if platform.system() == "Windows":
                                if (struct.calcsize("P") * 8) == 64:  # 32 for 32-bit & 64 for 64-bit
                                    subprocess.call([os.path.join(ori, 'lame', 'win64', 'lame.exe'), os.path.join(
                                        r, l, s), os.path.splitext(os.path.join(r, l, s))[0]+'.mp3', '-b', '320'])
                                elif (struct.calcsize("P") * 8) == 32:
                                    subprocess.call([os.path.join(ori, 'lame', 'win32', 'lame.exe'), os.path.join(
                                        r, l, s), os.path.splitext(os.path.join(r, l, s))[0]+'.mp3', '-b', '320'])
                            elif platform.system() == "Darwin":
                                # Install lame on Mac
                                pass  # For mac
                            elif platform.system() == "Linux":
                                if args.nat:
                                    subprocess.call(['lame', os.path.join(r, l, s), os.path.splitext(os.path.join(r, l, s))[0]+'.mp3', '-b', '320'])
                                else:
                                    subprocess.call(['wine', os.path.join(ori, 'lame', 'win32', 'lame.exe'), os.path.join(r, l, s), os.path.splitext(os.path.join(r, l, s))[0]+'.mp3', '-b', '320'])

if (args.Del):
    for r, d, f in os.walk(os.path.join(ori, 'Extracted')):
        for src in d:
            for l in os.listdir(os.path.join(r,src)):
                if os.path.splitext(l)[1].lower() in ['.wav']:
                    os.remove(os.path.join(r,src,l))

print("Complete! Log file is in the root directory.")