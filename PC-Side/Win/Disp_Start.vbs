Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c AUTOSTART.bat"
oShell.Run strArgs, 0, false
