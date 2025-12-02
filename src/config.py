"""
config.py - Application configuration management
"""
import configparser
import os


class Config:
    def __init__(self, config_file="config/settings.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
        if not os.path.exists(config_file):
            self._create_default_config()
        
        self.config.read(config_file)
    
    def _create_default_config(self):
        """Create default configuration file"""
        config = configparser.ConfigParser()
        config['DATABASE'] = {
            'path': 'data/travel_erasmus.db',
            'timeout': '5'
        }
        config['REPORTS'] = {
            'path': 'reports'
        }
        
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        with open(self.config_file, 'w') as f:
            config.write(f)
        
        print(f"✅ Configuration file created: {self.config_file}")
    
    def get_db_path(self):
        """Get database path from config"""
        return self.config.get('DATABASE', 'path', fallback='data/travel_erasmus.db')
    
    def get_reports_path(self):
        """Get reports path from config"""
        return self.config.get('REPORTS', 'path', fallback='reports')
