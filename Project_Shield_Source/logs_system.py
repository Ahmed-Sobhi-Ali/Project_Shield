import logging
from pathlib import Path

class Logger:
    log_file_path = Path(__file__).resolve().parent / 'project_shield.log'
    username = 'Unknown'  # Default username if not set

    @staticmethod
    def setup_logging():
        """Set up the logging configuration."""
        logging.basicConfig(
            filename=Logger.log_file_path,
            level=logging.INFO,
            format='%(asctime)s - %(username)s - %(levelname)s - %(message)s'
        )

    @staticmethod
    def set_username(user):
        """Set the username for logging."""
        Logger.username = user

    @staticmethod
    def log_action(action):
        """Log an action to the log file with the username."""
        logging.info(action, extra={'username': Logger.username})
