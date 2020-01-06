# CUE! - See You Everyday Audio Puller

Pulls audio from CUE! and processes it into WAV/MP3 files. This code is also **extendible** to games that use HCA/ACB/AWB compression. Only thing to edit is the directory names in the ```Startprocess.py``` files.

## Acknowledgements

The code incorporates code from the following repositories:

- Deretore (/deretore/): [link](https://github.com/OpenCGSS/DereTore)

The code also uses the following programs:

- ADB (/platform-tools/): [link](https://developer.android.com/studio/releases/platform-tools#downloads)
- LAME MP3 Encoder (/lame/): [link](https://lame.sourceforge.io/)

All copyright from the use of the programs mentioned goes to the respective copyright holders.

## Requirements

- Python 3
- .NET Framework 4.5
- Wine (For Linux/Mac)
- XQuartz >2.7.7 (Mac)

> *Except for **Python3**, checks are in place to make sure that all required programs are installed and configured, so there is NO need to manually install the software*

## Supported OSes

- Windows
- Ubuntu
- Debian 10 (& bullseye)
- Mac OS X (Partially up to Mojave)

> *Note to Mac users: File hashes on extracted WAV and MP3 will be **different** as compared to the Windows/Linux versions. This is due to Apple removing support for 32-bit software and wine not working properly as of writing. There is no guarantee that the extracted audio will have a similar quality to its Windows & Linux counterpart.
>
> Workarounds include using Bootcamp with Windows/Linux to run this software. All mentioned OSes above except for Mac have passed all tests.

## Use

```python3
usage: Startprocess.py [-h] [-o OUT] [-a ANAME] [-init] [-c] [-d] [-p P]

CUE! Audio Puller

optional arguments:
  -h, --help  show this help message and exit
  -o OUT      Specify output folder (Not tested yet, use at own risk!)
  -a ANAME    Android application name (Not implemented yet)
  -init       Emulate initial pull, extracts all current and previous files
  -c          Converts extracted WAV to MP3
  -d          Deletes WAV
  -p P        Port number for ADB, applies to Bluestacks/NoxPlayer (Not yet
              implemented)
  ```

### Examples:

  1. ```python3 Startprocess.py -h``` → shows the above help
  2. ```python3 Startprocess.py``` → starts program with default options (Extract to WAV only)
  3. ```python3 Startprocess.py -c``` → extracts WAV and converts these to MP3 (Both WAV and MP3 will be present)
  4. ```python3 Startprocess.py -c -d``` → extracts WAV, converts to MP3 and deletes the WAV files

>*Note: ```python3``` applies to Linux and Mac while Windows users must replace ```python3``` with ```python``` (and ensuring that the script is run with Python 3).

## Notes

- More support for other OSes are ongoing.
- Options only apply to current execution, i.e. files pulled from the previous execution will not be subjected to the current options.
- Each execution is **additive** (i.e. new files are constantly added and renamed if older files are present)
- Native app support is removed to maintain hash consistency across platforms. 

>*Important*: File hashes on Mac will be different due to Wine having errors due to removal of 32-bit support from Mac OS X.

## Steps (New):

*Start init.bat* (Simple enough for Windows) **OR** use either of the commands provided above in the **USE** section.

## Current things to do:

1. Creation of switches using getOpt or sys.argv *(Partially complete)*
   - Break each sector into functions and execute based on switches
5. Handle file extraction location
   - Save extraction locaton to file also -> Handle later due to fast push
6. Clean code by changing lots of constants to variables
8. Due to a problem, if you had used the default options the first time and opted to convert the files to MP3 the second time, the program will convert **ALL** existing WAV to MP3
9. Formatting of printing statements due to current flooding of CLI