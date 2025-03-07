import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import logging
from pathlib import Path
import win32file
import win32con
import pywintypes
import configparser
import sys
from translations import TRANSLATIONS

def load_config():
    """Charge la configuration depuis config.ini"""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(t('config_not_found').format(config_path))
    
    config.read(config_path, encoding='utf-8')
    
    # Charger les extensions vidéo
    video_extensions = tuple(ext.strip() for ext in config.get('Settings', 'video_extensions').split(','))
    
    return {
        'watch_directory': config.get('Paths', 'watch_directory'),
        'video_extensions': video_extensions,
        'max_download_wait': config.getint('Settings', 'max_download_wait'),
        'max_unlock_wait': config.getint('Settings', 'max_unlock_wait'),
        'language': config.get('Language', 'language', fallback='en')
    }

# Configuration globale
config = load_config()
LANG = config['language']

def t(key):
    """Fonction de traduction"""
    return TRANSLATIONS[LANG][key]

# Configuration du logging dans un fichier
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video_organizer.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class VideoHandler(FileSystemEventHandler):
    def __init__(self, config):
        super().__init__()
        self.video_extensions = config['video_extensions']
        self.max_download_wait = config['max_download_wait']
        self.max_unlock_wait = config['max_unlock_wait']
    
    def wait_for_file_completion(self, file_path):
        """Attend que le fichier soit complètement téléchargé en surveillant sa taille"""
        previous_size = -1
        stable_count = 0
        check_interval = 10  # secondes entre chaque vérification
        max_checks = self.max_download_wait // check_interval
        
        for _ in range(max_checks):
            try:
                current_size = os.path.getsize(file_path)
                if current_size == previous_size:
                    stable_count += 1
                    if stable_count >= 3:  # La taille est stable pendant 3 vérifications
                        logging.info(t('download_complete').format(Path(file_path).name, current_size))
                        return True
                else:
                    stable_count = 0
                    logging.info(t('download_progress').format(current_size))
                
                previous_size = current_size
                time.sleep(check_interval)
                
            except FileNotFoundError:
                logging.error(t('file_not_found').format(file_path))
                return False
            except Exception as e:
                logging.error(t('unexpected_error').format(str(e)))
                return False
        
        logging.warning(t('lock_timeout').format(Path(file_path).name))
        return False

    def wait_for_file_unlock(self, file_path):
        """Attend que le fichier soit déverrouillé"""
        start_time = time.time()
        while time.time() - start_time < self.max_unlock_wait:
            try:
                # Essaie d'ouvrir le fichier en mode écriture exclusive
                handle = win32file.CreateFile(
                    str(file_path),
                    win32con.GENERIC_WRITE,
                    0,  # Pas de partage
                    None,
                    win32con.OPEN_EXISTING,
                    win32con.FILE_ATTRIBUTE_NORMAL,
                    None
                )
                win32file.CloseHandle(handle)
                return True
            except pywintypes.error as e:
                if e.winerror == 32:  # Fichier utilisé par un autre processus
                    logging.info(t('file_locked').format(Path(file_path).name))
                    time.sleep(5)  # Attendre 5 secondes avant de réessayer
                else:
                    logging.error(t('lock_error').format(str(e)))
                    return False
        
        logging.warning(t('lock_timeout').format(Path(file_path).name))
        return False
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = event.src_path
        if file_path.lower().endswith(self.video_extensions):
            logging.info(t('new_file_detected').format(Path(file_path).name))
            if self.wait_for_file_completion(file_path):
                if self.wait_for_file_unlock(file_path):
                    self.organize_video(file_path)
                else:
                    logging.warning(t('lock_timeout').format(Path(file_path).name))
            else:
                logging.warning(t('process_error').format(Path(file_path).name, 'incomplete download'))
    
    def organize_video(self, file_path):
        try:
            file_path = Path(file_path)
            name_without_ext = file_path.stem
            
            # Create directory path using the file name
            new_dir = file_path.parent / name_without_ext
            new_file_path = new_dir / file_path.name
            
            # Si le fichier est déjà dans son propre dossier, on ignore
            if file_path.parent == new_dir:
                return
            
            # Create directory if it doesn't exist
            new_dir.mkdir(exist_ok=True)
            
            try:
                shutil.move(str(file_path), str(new_file_path))
                logging.info(t('move_success').format(file_path.name, new_dir))
            except Exception as e:
                logging.error(t('move_error').format(file_path.name, str(e)))
                    
        except Exception as e:
            logging.error(t('process_error').format(file_path, str(e)))

def watch_directory(path):
    if not os.path.exists(path):
        logging.error(t('file_not_found').format(path))
        return
    
    config = load_config()
    event_handler = VideoHandler(config)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    try:
        observer.start()
        logging.info(t('watching_folder').format(path))
        logging.info(t('press_ctrl_c'))
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info(t('stopping_watch'))
    except Exception as e:
        logging.error(t('unexpected_error').format(str(e)))
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    try:
        config = load_config()
        watch_directory(config['watch_directory'])
    except Exception as e:
        logging.error(t('config_error').format(str(e)))
        sys.exit(1)
