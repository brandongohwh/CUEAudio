for /F "tokens=*" %%a in (wav.log) do (
	del %%a
	)

del wav.log