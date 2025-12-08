# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 15:59:30 2025

@author: Paola
"""
import sys
import os

sys.path.insert(0, "src")

from database import DatabaseManager

def main():
    os.makedirs("data", exist_ok=True)
    db = DatabaseManager("data/travel_erasmus.db")
    db.connect()
    db.create_tables()
    cursor = db.cursor

    cursor.execute("DELETE FROM places")
    cursor.execute("DELETE FROM trips")
    db.commit()

    trips = [
        ("Barcelona Erasmus", "Spain", "Barcelona", "2025-03-01", "2025-03-10", 800, "Visit to Bcn during Erasmus"),
        ("Brussels Weekend", "Belgium", "Brussels", "2025-04-05", "2025-04-07", 300, "Weekend in Brussels"),
    ]

    trip_ids = []
    for t in trips:
        cursor.execute("""
            INSERT INTO trips (name, country, city, start_date, end_date, budget, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, t)
        trip_ids.append(cursor.lastrowid)

    places = [
        (trip_ids[0], "Sagrada Familia", "monument"),
        (trip_ids[0], "Parc Güell", "park"),
        (trip_ids[1], "Grand Place", "square"),
    ]

    cursor.executemany("""
        INSERT INTO places (trip_id, name, category)
        VALUES (?, ?, ?)
    """, places)

    db.commit()
    db.disconnect()
    print("Sample data inserted into data/travel_erasmus.db")

if __name__ == "__main__":
    main()
