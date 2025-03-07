# Obtenir le chemin du dossier du script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Créer le raccourci
$WScript = New-Object -ComObject WScript.Shell
$Shortcut = $WScript.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\VideoOrganizer.lnk")
$Shortcut.TargetPath = Join-Path $scriptPath "start_video_organizer.vbs"
$Shortcut.WorkingDirectory = $scriptPath
$Shortcut.Save()

Write-Host "Raccourci créé avec succès dans le dossier de démarrage !"
Write-Host "Chemin du raccourci : $($Shortcut.TargetPath)"
Write-Host "Dossier de travail : $($Shortcut.WorkingDirectory)"

# Attendre que l'utilisateur appuie sur une touche
Write-Host "`nAppuyez sur une touche pour fermer..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
