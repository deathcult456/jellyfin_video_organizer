import sys
import os
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, Qt
from video_organizer import watch_directory, load_config
from translations import TRANSLATIONS
import logging
import tempfile

class WatcherThread(QThread):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        try:
            watch_directory(self.path)
        except Exception as e:
            logging.error(t('unexpected_error').format(str(e)))

def resource_path(relative_path):
    """Obtenir le chemin absolu vers la ressource"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class VideoOrganizerTray:
    def __init__(self):
        try:
            # Charger la configuration
            self.config = load_config()
            self.watch_dir = self.config['watch_directory']
            
            # Définir la langue
            global LANG
            LANG = self.config['language']
            
            # Vérifier que le dossier existe
            if not os.path.exists(self.watch_dir):
                raise FileNotFoundError(t('file_not_found').format(self.watch_dir))
            
            # S'assurer qu'une seule instance est en cours d'exécution
            self.tmp_dir = tempfile.gettempdir()
            self.lock_file = os.path.join(self.tmp_dir, 'video_organizer.lock')
            
            if os.path.exists(self.lock_file):
                QMessageBox.warning(None, t('app_name'), t('already_running'))
                sys.exit(1)
                
            with open(self.lock_file, 'w') as f:
                f.write(str(os.getpid()))

            # Initialiser l'application
            self.app = QApplication(sys.argv)
            self.app.setQuitOnLastWindowClosed(False)
            
            # Créer une icône pour la barre des tâches
            self.tray = QSystemTrayIcon()
            self.create_tray_icon()
            
            if not self.tray.isSystemTrayAvailable():
                QMessageBox.critical(None, t('app_name'), t('tray_error'))
                sys.exit(1)
            
            # Créer le menu contextuel
            self.menu = QMenu()
            self.status_action = self.menu.addAction(t('running_status'))
            self.status_action.setEnabled(False)
            self.menu.addSeparator()
            
            # Ajouter l'option pour ouvrir le dossier surveillé
            open_action = self.menu.addAction(t('open_folder'))
            open_action.triggered.connect(self.open_watched_folder)
            
            # Ajouter l'option pour ouvrir le fichier de configuration
            config_action = self.menu.addAction(t('open_config'))
            config_action.triggered.connect(self.open_config)
            
            self.menu.addSeparator()
            quit_action = self.menu.addAction(t('quit'))
            quit_action.triggered.connect(self.quit)
            
            # Attacher le menu à l'icône
            self.tray.setContextMenu(self.menu)
            
            # Démarrer le watcher dans un thread séparé
            self.watcher = WatcherThread(self.watch_dir)
            self.watcher.start()
            
            # Afficher l'icône
            self.tray.show()
            
            # Message de démarrage
            self.tray.showMessage(
                t('app_name'),
                t('watching_notification').format(self.watch_dir),
                QIcon(),
                3000
            )
            
        except Exception as e:
            QMessageBox.critical(None, t('app_name'), t('startup_error').format(str(e)))
            sys.exit(1)
    
    def create_tray_icon(self):
        """Créer une icône plus visible pour la barre des tâches"""
        from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(0, 0, 0, 0))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dessiner un cercle bleu avec contour
        painter.setBrush(QColor(0, 120, 212))
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawEllipse(4, 4, 56, 56)
        
        # Dessiner un "V" blanc
        painter.setPen(QPen(QColor(255, 255, 255), 4))
        painter.drawLine(20, 25, 32, 45)
        painter.drawLine(32, 45, 44, 25)
        
        painter.end()
        
        self.tray.setIcon(QIcon(pixmap))
        self.tray.setToolTip(t('tooltip'))
    
    def open_watched_folder(self):
        """Ouvrir le dossier surveillé dans l'explorateur Windows"""
        os.startfile(self.watch_dir)
    
    def open_config(self):
        """Ouvrir le fichier de configuration dans l'éditeur par défaut"""
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        os.startfile(config_path)
    
    def quit(self):
        """Arrêter proprement l'application"""
        try:
            # Arrêter le thread de surveillance
            self.watcher.terminate()
            self.watcher.wait()
            
            # Supprimer le fichier de verrouillage
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
            
            # Quitter l'application
            self.app.quit()
        except Exception as e:
            logging.error(t('unexpected_error').format(str(e)))
            sys.exit(1)
    
    def run(self):
        """Démarrer l'application"""
        try:
            sys.exit(self.app.exec())
        except Exception as e:
            logging.error(t('unexpected_error').format(str(e)))
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
            sys.exit(1)

def t(key):
    """Fonction de traduction"""
    return TRANSLATIONS[LANG][key]

LANG = 'fr'  # Langue par défaut, sera mise à jour par la configuration

if __name__ == "__main__":
    try:
        app = VideoOrganizerTray()
        app.run()
    except Exception as e:
        logging.error(t('critical_error').format(str(e)))
        QMessageBox.critical(None, t('app_name'), t('critical_error').format(str(e)))
        sys.exit(1)
