"""
Module de traduction pour l'application Video Organizer
Translation module for Video Organizer application
"""

TRANSLATIONS = {
    'fr': {
        # Messages de log
        'watching_folder': 'Surveillance du dossier: {}',
        'press_ctrl_c': 'Appuyez sur Ctrl+C pour arrêter...',
        'stopping_watch': 'Arrêt de la surveillance...',
        'unexpected_error': 'Erreur inattendue: {}',
        'config_error': 'Erreur lors du chargement de la configuration: {}',
        'file_not_found': 'Le fichier {} n\'existe pas',
        'new_file_detected': 'Nouveau fichier détecté: {}',
        'download_progress': 'Téléchargement en cours... Taille actuelle: {} bytes',
        'download_complete': 'Fichier {} complètement téléchargé ({} bytes)',
        'file_locked': 'Fichier {} toujours verrouillé, attente...',
        'lock_error': 'Erreur lors de la vérification du verrouillage: {}',
        'lock_timeout': 'Timeout atteint en attendant le déverrouillage de {}',
        'move_success': 'Déplacé {} vers {}',
        'move_error': 'Erreur lors du déplacement de {}: {}',
        'process_error': 'Erreur inattendue lors du traitement de {}: {}',
        'config_not_found': 'Le fichier de configuration \'{}\' n\'existe pas!',
        
        # Interface système
        'app_name': 'Video Organizer',
        'running_status': 'En cours d\'exécution',
        'open_folder': 'Ouvrir le dossier surveillé',
        'open_config': 'Ouvrir la configuration',
        'quit': 'Quitter',
        'already_running': 'Une instance est déjà en cours d\'exécution!',
        'tray_error': 'La barre des tâches n\'est pas disponible!',
        'startup_error': 'Erreur lors du démarrage:\n{}',
        'critical_error': 'Une erreur critique est survenue:\n{}',
        'tooltip': 'Video Organizer - En cours d\'exécution',
        'watching_notification': 'Surveillance du dossier:\n{}'
    },
    'en': {
        # Log messages
        'watching_folder': 'Watching folder: {}',
        'press_ctrl_c': 'Press Ctrl+C to stop...',
        'stopping_watch': 'Stopping watch...',
        'unexpected_error': 'Unexpected error: {}',
        'config_error': 'Error loading configuration: {}',
        'file_not_found': 'File {} does not exist',
        'new_file_detected': 'New file detected: {}',
        'download_progress': 'Download in progress... Current size: {} bytes',
        'download_complete': 'File {} completely downloaded ({} bytes)',
        'file_locked': 'File {} still locked, waiting...',
        'lock_error': 'Error checking file lock: {}',
        'lock_timeout': 'Timeout reached waiting for {} to unlock',
        'move_success': 'Moved {} to {}',
        'move_error': 'Error moving {}: {}',
        'process_error': 'Unexpected error processing {}: {}',
        'config_not_found': 'Configuration file \'{}\' does not exist!',
        
        # System interface
        'app_name': 'Video Organizer',
        'running_status': 'Running',
        'open_folder': 'Open watched folder',
        'open_config': 'Open configuration',
        'quit': 'Quit',
        'already_running': 'An instance is already running!',
        'tray_error': 'System tray is not available!',
        'startup_error': 'Error during startup:\n{}',
        'critical_error': 'A critical error occurred:\n{}',
        'tooltip': 'Video Organizer - Running',
        'watching_notification': 'Watching folder:\n{}'
    }
}
