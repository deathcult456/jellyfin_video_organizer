Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
pythonCmd = "pythonw.exe """ & strPath & "\tray_app.py"""
objShell.Run pythonCmd, 0, False
