cd %~dp0
if not exist %~dp0\ProcessingFolder mkdir ProcessingFolder
if not exist %~dp0\Sound mkdir Sound

python %~dp0\Startprocess.py