dir /s/b %~dp0\Extracted\*.wav > wav.log

for /F "tokens=*" %%a in (wav.log) do (
	%~dp0\lame\win64\lame.exe %%a "%%~pa%%~na.mp3" -b 320
	)