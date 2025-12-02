# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 14:06:13 2025

@author: Paola
"""
import sqlite3
import os


class DatabaseManager:
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
        # Ensure directory exists
        db_dir = os.path.dirname(db_path) if os.path.dirname(db_path) else '.'
        os.makedirs(db_dir, exist_ok=True)
    
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            # This allows us to access columns by name
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            
            # Enable foreign key constraints
            self.cursor.execute("PRAGMA foreign_keys = ON")
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from database")
    
    def create_tables(self):
        try:
            # Create trips table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS trips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    country TEXT NOT NULL,
                    city TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    budget REAL NOT NULL,
                    description TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create places table with foreign key to trips
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS places (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trip_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    address TEXT,
                    notes TEXT,
                    rating INTEGER DEFAULT 0,
                    visited INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
                )
            ''')
            
            self.connection.commit()
            print("Database tables created successfully")
            
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise
    
    def commit(self):
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        if self.connection:
            self.connection.rollback()
    
    def close(self):
        self.disconnect()
