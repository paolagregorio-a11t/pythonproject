"""
config.py - Configuration management
"""
import configparser
import os


class Config:
    """Load configuration from settings file"""
    
    def __init__(self, config_file="config/settings.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
        if not os.path.exists(config_file):
            print(f"Config file not found: {config_file}")
            print("Create it from: config/settings.example.ini")
            raise FileNotFoundError(f"Missing {config_file}")
        
        self.config.read(config_file)
    
    def get_db_path(self):
        """Get database path from config"""
        return self.config.get('DATABASE', 'path')
