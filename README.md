# Video File Organizer for Jellyfin

🇫🇷 **Organiseur automatique de séries pour Jellyfin**

Organise automatiquement vos fichiers vidéo pour une compatibilité parfaite avec Jellyfin. Place chaque épisode dans son propre dossier pour assurer une détection correcte par Jellyfin. Fonctionne silencieusement dans la barre des tâches Windows et surveille vos dossiers de séries. Support français et anglais.

*Mots-clés : Jellyfin, organiseur de séries, automatisation Windows, gestionnaire de fichiers, détection automatique, media server*

🇬🇧 **Automatic TV Shows Organizer for Jellyfin**

Automatically organize your video files for perfect Jellyfin compatibility. Places each episode in its own folder to ensure proper detection by Jellyfin. Runs silently in the Windows system tray and monitors your TV shows folders. French and English support.

*Keywords: Jellyfin, TV shows organizer, Windows automation, file manager, auto-detection, media server*

---

# Video File Organizer

[English version below](#video-file-organizer-1)

Un script Python qui surveille automatiquement un dossier pour organiser les fichiers vidéo dans leurs propres sous-dossiers.

## Fonctionnalités

- Surveillance en temps réel d'un dossier maître
- Détection automatique des nouveaux fichiers vidéo
- Création automatique de sous-dossiers nommés d'après les fichiers
- Interface système minimaliste dans la barre des tâches
- Gestion intelligente des fichiers en cours de téléchargement
- Configuration facile via un fichier config.ini
- Support multilingue (Français et Anglais)

## Installation

1. Installer Python si ce n'est pas déjà fait
2. Installer les dépendances :
   ```
   pip install -r requirements.txt
   ```

## Configuration

Le fichier `config.ini` contient tous les paramètres de l'application :

```ini
[Paths]
; Dossier à surveiller pour les fichiers vidéo
watch_directory = D:\flight\serie_dossier

[Settings]
; Extensions vidéo supportées
video_extensions = .mp4, .avi, .mkv, .mov, .wmv
; Temps maximum d'attente pour le téléchargement (en secondes)
max_download_wait = 500
; Temps maximum d'attente pour le déverrouillage (en secondes)
max_unlock_wait = 300

[Language]
; Langue de l'application (fr pour français, en pour anglais)
language = fr
```

Pour modifier la configuration :
1. Ouvrir `config.ini` dans un éditeur de texte
2. Modifier les paramètres selon vos besoins
3. Sauvegarder le fichier
4. Redémarrer l'application si elle est en cours d'exécution

## Utilisation

1. Double-cliquer sur `start_video_organizer.vbs` pour démarrer l'application
2. Une icône apparaît dans la barre des tâches
3. Clic droit sur l'icône pour :
   - Voir le statut de l'application
   - Ouvrir le dossier surveillé
   - Ouvrir le fichier de configuration
   - Quitter l'application

## Fonctionnement

1. L'application surveille le dossier spécifié dans `config.ini`
2. Quand un nouveau fichier vidéo est détecté :
   - Attend que le téléchargement soit complet (taille stable)
   - Attend que le fichier soit déverrouillé
   - Crée un dossier avec le nom du fichier
   - Déplace le fichier dans ce dossier

## Logs

Les logs sont enregistrés dans `video_organizer.log` dans le même dossier que l'application.
Ils contiennent des informations détaillées sur :
- Les fichiers détectés
- L'état des téléchargements
- Les opérations de déplacement
- Les erreurs éventuelles

## Démarrage automatique

Pour lancer l'application au démarrage de Windows :
1. Double-cliquer sur `create_startup_shortcut.ps1`
2. Une fenêtre PowerShell s'ouvre et crée le raccourci
3. Le script affiche les chemins configurés
4. Appuyer sur une touche pour fermer la fenêtre

Pour désactiver le démarrage automatique, supprimer le raccourci "VideoOrganizer" du dossier :
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

---

# Video File Organizer

A Python script that automatically monitors a folder to organize video files into their own subfolders.

## Features

- Real-time monitoring of a master folder
- Automatic detection of new video files
- Automatic creation of subfolders named after files
- Minimalist system tray interface
- Smart handling of downloading files
- Easy configuration via config.ini file
- Multilingual support (French and English)

## Installation

1. Install Python if not already done
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

The `config.ini` file contains all application settings:

```ini
[Paths]
; Folder to watch for video files
watch_directory = D:\flight\serie_dossier

[Settings]
; Supported video extensions
video_extensions = .mp4, .avi, .mkv, .mov, .wmv
; Maximum wait time for download (in seconds)
max_download_wait = 500
; Maximum wait time for file unlock (in seconds)
max_unlock_wait = 300

[Language]
; Application language (fr for French, en for English)
language = en
```

To modify the configuration:
1. Open `config.ini` in a text editor
2. Modify settings as needed
3. Save the file
4. Restart the application if it's running

## Usage

1. Double-click `start_video_organizer.vbs` to start the application
2. An icon appears in the system tray
3. Right-click the icon to:
   - View application status
   - Open the watched folder
   - Open configuration file
   - Quit application

## How it works

1. The application monitors the folder specified in `config.ini`
2. When a new video file is detected:
   - Waits for download to complete (stable size)
   - Waits for file to unlock
   - Creates a folder with the file name
   - Moves the file into that folder

## Logs

Logs are saved in `video_organizer.log` in the same folder as the application.
They contain detailed information about:
- Detected files
- Download status
- Move operations
- Any errors

## Automatic Startup

To launch the application at Windows startup:
1. Double-click `create_startup_shortcut.ps1`
2. A PowerShell window opens and creates the shortcut
3. The script displays the configured paths
4. Press any key to close the window

To disable automatic startup, delete the "VideoOrganizer" shortcut from:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
