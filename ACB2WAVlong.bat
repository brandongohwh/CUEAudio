dir /s/b %~dp0\ProcessingFolder\*.acb > acb.log

for /F "tokens=*" %%a in (acb.log) do (
	%~dp0\deretore\Release\acbUnzip.exe %%a
	)

del acb.log

dir /s/b %~dp0\ProcessingFolder\*.hca > hca.log

for /F "tokens=*" %%a in (hca.log) do (
	%~dp0\deretore\Release\hca2wav.exe %%a
	)

del hca.log