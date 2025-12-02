# -*- coding: utf-8 -*-
"""
main.py - Travel Erasmus CLI
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database import DatabaseManager
from config import Config
from models import Trip


class TravelApp:
    """Main application"""
    
    def __init__(self):
        print("\n" + "="*50)
        print("TRAVEL ERASMUS")
        print("="*50)
        
        # Load configuration
        print("\nLoading configuration...")
        self.config = Config("config/settings.ini")
        print("Configuration loaded")
        
        # Connect to database
        print("\n🗄️  Initializing database...")
        db_path = self.config.get_db_path()
        print(f"Database: {db_path}")
        self.db = DatabaseManager(db_path)
        self.db.connect()
        self.db.create_tables()
        print("Database ready\n")
    
    def show_menu(self):
        """Show main menu"""
        print("="*50)
        print("1. Add trip")
        print("2. List trips")
        print("3. Exit")
        print("="*50)
    
    def add_trip(self):
        """Add a trip to database"""
        print("\n➕ Add Trip")
        print("-"*50)
        
        name = input("Trip name: ").strip()
        country = input("Country: ").strip()
        city = input("City: ").strip()
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        end_date = input("End date (YYYY-MM-DD): ").strip()
        budget = float(input("Budget (EUROS): ").strip())
        
        # Create Trip object
        trip = Trip(
            name=name,
            country=country,
            city=city,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            description=""
        )
        
        # Insert into database
        try:
            self.db.cursor.execute('''
                INSERT INTO trips (name, country, city, start_date, end_date, budget, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (trip.name, trip.country, trip.city, trip.start_date, 
                  trip.end_date, trip.budget, trip.description))
            self.db.commit()
            print(f"Trip '{name}' added successfully!\n")
        except Exception as e:
            print(f"Error: {e}\n")
    
    def list_trips(self):
        """List all trips from database"""
        print("\n📋 All Trips")
        print("-"*50)
        
        try:
            self.db.cursor.execute('SELECT * FROM trips')
            rows = self.db.cursor.fetchall()
            
            if not rows:
                print("📭 No trips yet\n")
                return
            
            for row in rows:
                trip_id = row['id']
                name = row['name']
                country = row['country']
                city = row['city']
                budget = row['budget']
                print(f"[ID: {trip_id}] {name} - {city}, {country} (€{budget})")
            print()
        except Exception as e:
            print(f"Error: {e}\n")
    
    def run(self):
        """Run the application"""
        while True:
            self.show_menu()
            choice = input("Select: ").strip()
            
            if choice == '1':
                self.add_trip()
            elif choice == '2':
                self.list_trips()
            elif choice == '3':
                print("\nGoodbye!\n")
                break
            else:
                print("Invalid option\n")
    
    def close(self):
        """Close database"""
        self.db.disconnect()


def main():
    try:
        app = TravelApp()
        app.run()
        app.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
