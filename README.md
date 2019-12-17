# CUEOriginal

## Steps (Old):
1. Run CUE.bat to create directory structure -> !Ensure that the depth for new folders is correct!
2. Search for all AWB/ACB and dump into VGMToolbox
3. Get all ~~BIN~~ HCA files
4. Run HCADecode batch script
5. Throw all the WAV into respective folders
6. Use empty folder to see if anything was copied wrongly (mostly not)
7. Get all .bin .hca and .wav files (.wav are duplicates)
8. Run cleanup file

## Steps (New):
1. *Start init.bat* -> Run python file -> Does ADB pull -> Gets all new ACB, AWB and dump into root/processingfolder folder -> Extract HCA from ACB -> Extract WAV from HCA
2. ~~Copy WAV to respective folder~~
3. Automatically clean processing folder for next update -> This is performed everytime the script starts (Also checks for stray .WAV files)

## Current things to do:
1. ~~Automate extraction, copying and populate folders automatically into CUEPush repo~~
2. Cut down on number of scripts to run