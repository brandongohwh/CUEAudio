# CUEOriginal

Pulls audio from CUE and processes it into WAV files. This code is also **extendible** to games that use Unity audio compression. Only thing to edit is the directory names in the ```startprocess.py``` and ```adbpull.bat``` files.

## Special Thanks
The code uses the following repositories:

- Deretore: [link](https://github.com/OpenCGSS/DereTore)

All copyright goes to the respective copyright holders
## Notes
- This currently works on Windows only due to use of ```.bat``` files. Cross-compatibility is planned later.
## Steps (New):
1. *Start init.bat* (Simple enough)
3. Clean processing folder of stray .wav files

## Current things to do:
1. Cut down on number of scripts to run
3. Creation of switches using getOpt or sys.argv
<br/>a. Break each sector into functions and execute based on switches
4. ~~Handle file modifications -> Don't have to since its a hash based system for awb/acb~~
5. Handle file extraction location
<br/>a. Save extraction locaton to file also -> Handle later due to fast push
6. Clean code by changing lots of constants to variables
7. Make cross-compatibility by delivering full Python script/C#

Use of this software is governed by the MIT license and the authors do not expressly provide consent to use the software to facilitate illegal piracy of audio files. Additionally, please respect the (software/app) developers and their wishes if they so express.
