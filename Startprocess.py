# -*- coding: utf-8 -*-

# Package section
import os
import time
import subprocess
import shutil
from datetime import datetime
import sys
import filecmp
import platform
import struct
import argparse
import shutil
import pyfile.strfile as st

# Initialisation section (IMPORTANT: DO NOT MOVE)
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Dir variables
# Fixed dir
ori = os.getcwd()
procLoc = os.path.join(ori, 'ProcessingFolder')
extLoc = os.path.join(ori, 'Extracted')
pullLoc = os.path.join(ori, 'Sound')
adbPre = os.path.join(ori, 'platform-tools')
mp3Pre = os.path.join(ori, 'lame')
dere = os.path.join(ori, 'deretore', 'Release')
AndroidLoc = "/sdcard/Android/data/jp.co.liberent.cue/files/UnityCache/Shared/Sound/."
dotNET45x86 = os.path.join(
    'C:/', 'Windows', 'Microsoft.NET', 'Framework', 'v4.0.30319')
dotNET45x64 = os.path.join(
    'C:/', 'Windows', 'Microsoft.NET', 'Framework64', 'v4.0.30319')
# Relative dir
fol = 'Extracted'

# General variables
sudoAPT = ['sudo', 'apt', 'install']
sudoNoPrompt = ['-y']
wineUbuntu = 'wine-stable'
wineDevUbuntu = 'wine-development'
wineAdd = 'winetricks'
mp3 = 'lame'

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


def PreProcessing(val):
    folders = []

    if os.path.exists(procLoc):
        for r, d, f in os.walk(procLoc):
            for folder in d:
                folders.append(os.path.join(r, folder))

    for f in folders:
        for fi in os.listdir(f):
            if os.path.splitext(fi)[1].lower() == '.wav':
                if val == 0:
                    print(st.warningpre1 % st.warning)
                    print(st.warningpre2)
                elif val == 1:
                    print(st.warningpost1 % st.warning)
                    print(st.warningpost2)
                sys.exit(0)

    if os.path.exists(procLoc):
        shutil.rmtree(procLoc)
    os.makedirs(procLoc)


def ADBexec(init=0):
    folders = []
    if not init:
        for r, d, f in os.walk(pullLoc):
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
    print(0, end='\n\n')

    if platform.system() == 'Windows':
        x = subprocess.call(
            [os.path.join(adbPre, 'win', 'adb.exe'), 'pull', AndroidLoc, pullLoc])
        if x:
            t = 3
            for i in range(t):
                print(
                    "(Attempt %d of %d) You may need to authorise ADB to access your Android device! Waiting for 5 seconds." % (i+1, t))
                time.sleep(5)
                x = subprocess.call(
                    [os.path.join(adbPre, 'win', 'adb.exe'), 'pull', AndroidLoc, pullLoc])
                if not x:
                    break

    elif platform.system() == 'Darwin':
        x = subprocess.call(
            [os.path.join(adbPre, 'mac', 'adb'), 'pull', AndroidLoc, pullLoc])
    elif platform.system() == 'Linux':
        subprocess.call(
            ['chmod', '+x', os.path.join(adbPre, 'linux', 'adb')])
        x = subprocess.call(
            [os.path.join(adbPre, 'linux', 'adb'), 'pull', AndroidLoc, pullLoc])
        if x:
            t = 3
            for i in range(t):
                print(
                    "(Attempt %d of %d) You may need to authorise ADB to access your Android device! Waiting for 5 seconds." % (i+1, t))
                time.sleep(5)
                x = subprocess.call(
                    [os.path.join(adbPre, 'linux', 'adb'), 'pull', AndroidLoc, pullLoc])
                if not x:
                    break
    if x:
        print("There is an error with ADB, program terminating!")
        sys.exit(0)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    g = open(os.path.join(ori, 'updatedfolder.log'), 'a+')

    g.write("Update time: "+dt_string)
    g.write(st.Tbr)
    g.write("Changed Folders:\n")

    if init:
        folderpost = []
        for r, d, f in os.walk(pullLoc):
            for folder in d:
                if os.listdir(os.path.join(r, folder)):
                    folderpost.append(os.path.join(r, folder))
        if len(folderpost):
            for s in folderpost:
                g.write(s)
                g.write("\n")
        else:
            g.write("<NIL>\n")
        g.write(st.br)

    else:
        # Gets updated folders only
        folderpost = []
        for r, d, f in os.walk(pullLoc):
            for folder in d:
                if os.listdir(os.path.join(r, folder)) and os.path.join(r, folder) not in folders:
                    folderpost.append(os.path.join(r, folder))

        if len(folderpost):
            for s in folderpost:
                g.write(s)
                g.write("\n")
        else:
            g.write("<NIL>\n")
        g.write(st.br)

    g.write("Files added:\n")
    # For new folders, locate awb/acb and place them in the same folder

    if len(folderpost):
        for f in folderpost:
            for fi in os.listdir(f):
                if os.path.splitext(fi)[1].lower() in ['.awb', '.acb']:
                    print(os.path.join(f, fi))
                    g.write(os.path.join(f, fi))
                    g.write("\n")
                    if not os.path.isdir(os.path.join(procLoc, os.path.basename(os.path.join(f, os.path.splitext(fi)[0])), '')):
                        os.mkdir(os.path.join(procLoc, os.path.basename(
                            os.path.join(f, os.path.splitext(fi)[0])), ''))
                    shutil.copy(os.path.join(f, fi), os.path.join(
                        procLoc, os.path.basename(os.path.join(f, os.path.splitext(fi)[0])), ''))
    else:
        g.write("<NIL>\n")
        print("No new files added!")
        sys.exit(0)

    g.write(st.Fbr)
    g.flush()
    g.close()


def ACB2WAV():
    for r, d, f in os.walk(procLoc):
        for l in d:
            for s in os.listdir(os.path.join(r, l)):
                if os.path.splitext(s)[1].lower() in ['.acb']:
                    if platform.system() == 'Windows':
                        subprocess.call(
                            [os.path.join(dere, 'acbUnzip.exe'), os.path.join(r, l, s)])
                    elif platform.system() == 'Linux':
                        subprocess.call(['wine', os.path.join(
                            dere, 'acbUnzip.exe'), os.path.join(r, l, s)])

    for r, d, f in os.walk(procLoc):
        for l in d:
            for s in os.listdir(os.path.join(r, l)):
                if os.path.splitext(s)[1].lower() in ['.hca']:
                    print("Processing %s" % os.path.join(r, l, s))
                    if platform.system() == 'Windows':
                        subprocess.call(
                            [os.path.join(dere, 'hca2wav.exe'), os.path.join(r, l, s)])
                    elif platform.system() == 'Linux':
                        subprocess.call(['wine', os.path.join(
                            dere, 'hca2wav.exe'), os.path.join(r, l, s)])


def copyF(fol):
    for f in os.listdir(procLoc):
        for r, d, f2 in os.walk(fol):
            if f in d:
                for r2, d2, f3 in os.walk(os.path.join(procLoc, f)):
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


def preCheck():
    # Pre-req check
    # https://askubuntu.com/questions/578257/how-to-get-the-package-description-using-python-apt
    if 'ubuntu' in platform.platform().lower():
        import apt
        cache = apt.Cache()
        pkg1 = cache[wineUbuntu]
        pkg2 = cache[wineDevUbuntu]
        pkg3 = cache[wineAdd]
        x = 0
        if not pkg1.is_installed and not pkg2.is_installed:
            x += 1
            print(st.p1NI)
            # Checking repo -> Need to provide print statement
            time.sleep(10)
            subprocess.call(['sudo', 'apt', 'update', '-y'])
            subprocess.call(sudoAPT+[wineUbuntu]+sudoNoPrompt)
        else:
            print(st.p1AI, end="")
        if not pkg3.is_installed:
            if not x:
                print()
                time.sleep(10)
            else:
                print(st.p2NI)
                time.sleep(5)
            subprocess.call(sudoAPT+[wineAdd]+sudoNoPrompt)
        else:
            print(st.p2AI, end="")
        f = subprocess.Popen([wineAdd]+['list-installed'],
                             stdout=subprocess.PIPE)
        a = f.communicate()
        if not ('dotnet45' in str(a)):
            print(st.p3NI)
            time.sleep(5)
            subprocess.call([wineAdd] + ['--force','dotnet45'])
        else:
            print(st.p3AI, end="")
        if args.nat == True:
            pkg4 = cache[mp3]
            if not pkg4.is_installed:
                print(st.p4NI)
                time.sleep(10)
                subprocess.call(sudoAPT+[mp3] + sudoNoPrompt)
            else:
                print(st.p4AI, end="")
        print(st.pOK)
    elif 'debian' in platform.platform().lower():
        if 'debian-10' in platform.platform().lower():
            import apt
            cache = apt.Cache()
            pkg1 = cache['wine']
            if not pkg1.is_installed:
                print(st.p1NI)
                time.sleep(10)
                x = subprocess.call(['sudo', 'add-apt-repository', 'contrib'])
                if x:
                    print(st.sudoProbDeb10)
                    os._exit(0)
                subprocess.call(['sudo', 'add-apt-repository', 'non-free'])
                subprocess.call(['sudo','dpkg','--add-architecture','i386'])
                subprocess.call(['sudo', 'apt', 'update', '-y'])
                #askubuntu.com/questions/1090094/wine-missing-ntlm-auth-3-0-25
                #Prompt to tell user to click next only
                subprocess.call(['sudo', 'apt', 'install', 'wine', 'winbind','-y'])
            else:
                print(st.p1AI, end="")
            cache = apt.Cache()
            pkg2 = cache['wine32:i386']
            if not pkg2.is_installed:
                subprocess.call(['sudo', 'apt', 'install', 'wine32','-y'])
            pkg3=cache[wineAdd]
            if not pkg3.is_installed:
                if not x:
                    print(st.p2NI)
                    time.sleep(10)
                else:
                    print(st.p2NI)
                    time.sleep(5)
                subprocess.call(sudoAPT+[wineAdd]+sudoNoPrompt)
            else:
                print(st.p2AI, end="")
            os.environ['WINEARCH']= "win32"
            os.environ['WINEPREFIX']=os.path.expanduser("~")+os.path.sep+".winedotnet"
            #subprocess.call(['wineboot','-u'])
            f = subprocess.Popen([wineAdd]+['list-installed'],
                             stdout=subprocess.PIPE)
            a = f.communicate()
            if not ('dotnet45' in str(a)):
                print(st.p3NI)
                time.sleep(5)
                subprocess.call([wineAdd] + ['dotnet45'])
            else:
                print(st.p3AI, end="")
            if args.nat == True:
                pkg4 = cache[mp3]
                if not pkg4.is_installed:
                    print(st.p4NI)
                    time.sleep(10)
                    subprocess.call(sudoAPT+[mp3] + sudoNoPrompt)
                else:
                    print(st.p4AI, end="")
            print(st.pOK)
    elif platform.system() == 'Windows':
        if not (os.path.exists(dotNET45x86) or os.path.exists(dotNET45x64)):
            print(st.windotNET45)
            time.sleep(10)
            subprocess.call(
                [os.path.join(ori, 'installer', 'dotNetFx45_Full_setup.exe')], shell=True)
    elif 'centos' in platform.platform().lower():
        # Due to sickening documentation for Fedora/CentOS/RHEL and lack of packages from default repo, going to use brute-force method
        # https://stackoverflow.com/questions/567542/running-a-command-as-a-super-user-from-a-python-script
        x = subprocess.call(['sudo', 'dnf', 'install', 'epel-release'])
        if x:
            print(st.sudoProb)
        # Edited visudo with <user> ALL=(ALL) ALL
        sys.exit(0)
    else:
        print(st.noSup)
        sys.exit(0)


def folFile():
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
                updateFolder(os.path.join(ori, args.Out),
                             os.path.join(ori, fol))
                copyF(os.path.join(ori, args.Out))


def convFile():
    if args.Out == None or args.Out == False:
        for r, d, f in os.walk(extLoc):
            for l in d:
                for s in os.listdir(os.path.join(r, l)):
                    if os.path.splitext(s)[1].lower() in ['.wav']:
                        if not (os.path.splitext(s)[0]+'.mp3') in os.listdir(os.path.join(r, l)):
                            if platform.system() == "Windows":
                                if (struct.calcsize("P") * 8) == 64:  # 32 for 32-bit & 64 for 64-bit
                                    subprocess.call([os.path.join(mp3Pre, 'win64', 'lame.exe'), os.path.join(
                                        r, l, s), os.path.splitext(os.path.join(r, l, s))[0]+'.mp3', '-b', '320'])
                                elif (struct.calcsize("P") * 8) == 32:
                                    subprocess.call([os.path.join(mp3Pre, 'win32', 'lame.exe'), os.path.join(
                                        r, l, s), os.path.splitext(os.path.join(r, l, s))[0]+'.mp3', '-b', '320'])
                            elif platform.system() == "Darwin":
                                # Install lame on Mac
                                pass  # For mac
                            elif platform.system() == "Linux":
                                if args.nat:
                                    subprocess.call(['lame', os.path.join(r, l, s), os.path.splitext(
                                        os.path.join(r, l, s))[0]+'.mp3', '-b', '320'])
                                else:
                                    subprocess.call(['wine', os.path.join(mp3Pre, 'win32', 'lame.exe'), os.path.join(
                                        r, l, s), os.path.splitext(os.path.join(r, l, s))[0]+'.mp3', '-b', '320'])


def delWAV():
    for r, d, f in os.walk(extLoc):
        for src in d:
            for l in os.listdir(os.path.join(r, src)):
                if os.path.splitext(l)[1].lower() in ['.wav']:
                    os.remove(os.path.join(r, src, l))


preCheck()
print(st.welcome % st.icon)

PreProcessing(0)
if args.init == False or args.init == None:
    ADBexec()
else:
    ADBexec(1)
ACB2WAV()
folFile()

PreProcessing(1)

if (args.conv):
    convFile()

if (args.Del):
    delWAV()

print("Complete! Log file is in %s" % ori)
