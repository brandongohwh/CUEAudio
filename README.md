# CUE! - See You Everyday Audio Puller

Pulls audio from CUE! and processes it into WAV/MP3 files. This code is also **extendible** to games that use HCA/ACB/AWB compression. Only thing to edit is the directory names in the ```startprocess.py``` and ```adbpull.bat``` files.

## Special Thanks

The code uses the following repositories:

- Deretore (/deretore/): [link](https://github.com/OpenCGSS/DereTore)

The code also uses the following programs:

- ADB (/platform-tools/): [link](https://developer.android.com/studio/releases/platform-tools#downloads)
- LAME MP3 Encoder (/lame/): [link](https://lame.sourceforge.io/)

All copyright from the use of the programs mentioned goes to the respective copyright holders.

## Requirements

- Python 3
- Wine (For Mac/Linux)
    - Debian/Linux instructions:
        - apt install wine-stable winetricks
        - winetricks dotnet45

## Use

```
usage: Startprocess.py [-h] [-o OUT] [-a ANAME] [-init] [-c] [-d] [-p P]

CUE! Audio Puller

optional arguments:
  -h, --help  show this help message and exit
  -o OUT      Specify output folder (Not tested yet, use at own risk!)
  -a ANAME    Android application name (Not tested yet, use at own risk!)
  -init       Emulate initial pull, extracts all current and previous files
              (Not yet implemented)
  -c          Converts extracted WAV to MP3
  -d          Deletes WAV
  -p P        Port number for ADB, applies to NoxPlayer (Not yet implemented)
  ```

### Examples:

  1. ```python startprocess.py -h``` → shows the above help
  2. ```python startprocess.py``` → starts program with default options (Extract to WAV only)
  3. ```python startprocess.py -c``` → extracts WAV and converts these to MP3 (Both WAV and MP3 will be present)
  4. ```python startprocess.py -c -d``` → extracts WAV, converts to MP3 and deletes the WAV files

## Notes

- This currently works on Windows only due to use of ```.bat``` files. Cross-compatibility is planned later.

- ~~To have the program convert extracted files to ```.mp3```, edit the following on line 17 of ```startprocess.py```: ```mp3=1``` → ```mp3=0```~~ (See *Use* for update to this)
- Options only apply to current execution, i.e. files pulled from the previous execution will not be subjected to the current options.


## Steps (New):

1. *Start init.bat* (Simple enough)
3. ~~Clean processing folder of stray .wav files~~ (Should not happen due to fixed typo)

## Current things to do:

1. Cut down on number of scripts to run
3. Creation of switches using getOpt or sys.argv *(Partially complete)*
<br/>a. Break each sector into functions and execute based on switches
5. Handle file extraction location
<br/>a. Save extraction locaton to file also -> Handle later due to fast push
6. Clean code by changing lots of constants to variables
7. Make cross-compatibility by delivering full Python script/C#
8. Due to a problem, if you had used the default options the first time and opted to convert the files to MP3 the second time, the program will convert **ALL** existing WAV to MP3