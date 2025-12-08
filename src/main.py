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
import csv
from datetime import datetime

class TravelApp:
    
    def __init__(self):
        print("\n" + "="*50)
        print("TRAVEL ERASMUS")
        print("="*50)
        
        # Load configuration
        print("\n Loading configuration...")
        self.config = Config("config/settings.ini")
        print("Configuration loaded")
        
        # Connect to database
        print("\n Initializing database...")
        db_path = self.config.get_db_path()
        print(f"Database: {db_path}")
        self.db = DatabaseManager(db_path)
        self.db.connect()
        self.db.create_tables()
        print("Database ready\n")
    
    def show_menu(self):
        print("="*50)
        print("1. Add trip")
        print("2. List trips")
        print("3. View trip details")
        print("4. Update trip budget")
        print("5. Delete trip")
        print("6. Manage places in trip")
        print("7. Export trips to CSV")
        print("8. Exit")

        print("="*60)
    
    def add_trip(self):
        print("\n Add Trip")
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
        print("\n All Trips")
        print("-"*50)
        
        try:
            self.db.cursor.execute('SELECT * FROM trips')
            rows = self.db.cursor.fetchall()
            
            if not rows:
                print("No trips yet\n")
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
            
    def add_place(self, trip_id):
        print("\nADD PLACE")
        print("-"*30)
        
        name = input("Place name: ").strip()
        category = input("Category (museum/restaurant/monument): ").strip()
        
        try:
            self.db.cursor.execute('''
                INSERT INTO places (trip_id, name, category)
                VALUES (?, ?, ?)
            ''', (trip_id, name, category))
            self.db.commit()
            print("Place added!")
        except Exception as e:
            print(f"Error: {e}")
            
            
    def list_places(self, trip_id):
        self.db.cursor.execute('SELECT * FROM places WHERE trip_id = ? ORDER BY name', (trip_id,))
        places = self.db.cursor.fetchall()
        
        if not places:
            print("No places yet")
        else:
            print("\n Places:")
            for place in places:
                status = "Visited" if place['visited'] else "Not visited"
                print(f"  [ID: {place['id']}] {status} {place['name']} ({place['category']})")

    
    def run(self):
        while True:
            self.show_menu()
            choice = input("Select option (1-7): ").strip()
            
            if choice == '1':
                self.add_trip()
            elif choice == '2':
                self.list_trips()
            elif choice == '3':
                self.view_trip_details()
            elif choice == '4':
                self.update_trip_budget()
            elif choice == '5':
                self.delete_trip()
            elif choice == '6':
                self.manage_places()
            elif choice == '7':
                self.export_trips_csv()
            elif choice == '8':
                print("\nGoodbye!")
                break
            else:
                print("Invalid option. Try 1-7")
    
    def close(self):
        self.db.disconnect()
        
    def view_trip_details(self):
        print("\n TRIP DETAILS")
        print("-"*40)
        
        try:
            trip_id = int(input("Enter trip ID: "))
            
            self.db.cursor.execute('SELECT * FROM trips WHERE id = ?', (trip_id,))
            row = self.db.cursor.fetchone()
            
            if not row:
                print("Trip not found")
                return
            
            print(f"\n ID: {row['id']}")
            print(f"Name: {row['name']}")
            print(f"Country: {row['country']}")
            print(f"City: {row['city']}")
            print(f"Dates: {row['start_date']} → {row['end_date']}")
            print(f"Budget: €{row['budget']:.2f}")
            print(f"Created: {row['created_at']}")
            
            if row['description']:
                print(f"Description: {row['description']}")
                
        except ValueError:
            print("Invalid ID")
        except Exception as e:
            print(f"Error: {e}")
    
    def update_trip_budget(self):
        """Update budget of a trip"""
        print("\n UPDATE BUDGET")
        print("-"*40)
        
        try:
            trip_id = int(input("Enter trip ID: "))
            new_budget = float(input("New budget (€): "))
            
            self.db.cursor.execute('SELECT name FROM trips WHERE id = ?', (trip_id,))
            row = self.db.cursor.fetchone()
            
            if not row:
                print("Trip not found")
                return
            
            confirm = input(f"Update '{row['name']}' budget to €{new_budget:.2f}? (y/n): ")
            
            if confirm.lower() == 'y':
                self.db.cursor.execute(
                    'UPDATE trips SET budget = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    (new_budget, trip_id)
                )
                self.db.commit()
                print("Budget updated!")
            else:
                print("Cancelled")
                
        except ValueError:
            print("Invalid input")
        except Exception as e:
            print(f"Error: {e}")
    
    def delete_trip(self):
        print("\n DELETE TRIP")
        print("-"*40)
        
        try:
            trip_id = int(input("Enter trip ID to delete: "))
            
            self.db.cursor.execute('SELECT name FROM trips WHERE id = ?', (trip_id,))
            row = self.db.cursor.fetchone()
            
            if not row:
                print(" Trip not found")
                return
            
            print(f"\n Delete: {row['name']} (ID: {trip_id})")
            confirm = input("Are you sure? (y/n): ")
            
            if confirm.lower() == 'y':
                self.db.cursor.execute('DELETE FROM trips WHERE id = ?', (trip_id,))
                self.db.commit()
                print("Trip deleted!")
            else:
                print(" Cancelled")
                
        except ValueError:
            print("Invalid input")
        except Exception as e:
            print(f"Error: {e}")
            
    def export_trips_csv(self):
        """Export all trips to a CSV file"""
        print("\n EXPORT TRIPS TO CSV")
        print("-"*40)
        
        try:
            self.db.cursor.execute('SELECT * FROM trips')
            rows = self.db.cursor.fetchall()
            
            if not rows:
                print("No trips to export\n")
                return
            
            # Asegurar carpeta reports
            os.makedirs("reports", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/trips_{timestamp}.csv"
            
            with open(filename, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                # Cabecera
                writer.writerow([
                    "id", "name", "country", "city",
                    "start_date", "end_date", "budget", "description"
                ])
                # Filas
                for row in rows:
                    writer.writerow([
                        row["id"],
                        row["name"],
                        row["country"],
                        row["city"],
                        row["start_date"],
                        row["end_date"],
                        row["budget"],
                        row["description"] if row["description"] else ""
                    ])
            
            print(f"Trips exported to: {filename}\n")
        except Exception as e:
            print(f"Error exporting CSV: {e}\n")
    
    def manage_places(self):
        print("\nMANAGE PLACES")
        print("-"*40)
        
        try:
            trip_id = int(input("Enter trip ID: "))
            
            self.db.cursor.execute('SELECT name FROM trips WHERE id = ?', (trip_id,))
            row = self.db.cursor.fetchone()
            
            if not row:
                print("Trip not found")
                return
            
            print(f"\n'{row['name']}' (ID: {trip_id})")
            print("a) Add place")
            print("l) List places")
            print("v) Mark place as visited")
            print("b) Back")
            action = input("Choose (a/l/v/b): ").strip().lower()
            
            if action == 'a':
                self.add_place(trip_id)
            elif action == 'l':
                self.list_places(trip_id)
            elif action == 'v':
                self.mark_place_visited(trip_id)
            elif action == 'b':
                return
            else:
                print("Invalid option")
                
        except ValueError:
            print("Invalid input")
        except Exception as e:
            print(f"Error: {e}")
    
    def mark_place_visited(self, trip_id):
        print("\nMARK PLACE AS VISITED")
        print("-"*40)
        
        self.list_places(trip_id)
        
        try:
            place_id = int(input("Enter place ID: "))
            
            self.db.cursor.execute('UPDATE places SET visited = 1 WHERE id = ?', (place_id,))
            if self.db.cursor.rowcount > 0:
                self.db.commit()
                print("Place marked as visited!")
            else:
                print("Place not found")
                
        except ValueError:
            print("Invalid ID")
        except Exception as e:
            print(f"Error: {e}")




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
