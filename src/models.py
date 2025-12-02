# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 14:06:07 2025

@author: Paola
"""


from datetime import datetime


class Trip:
    
    def __init__(self, name, country, city, start_date, end_date, budget, description="", trip_id=None):
      
        self.id = trip_id
        self.name = name
        self.country = country
        self.city = city
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.description = description
    
    def __str__(self):
        return f" {self.name} - {self.city}, {self.country} ({self.start_date} → {self.end_date})"
    
    def __repr__(self):
        return f"Trip(id={self.id}, name='{self.name}', country='{self.country}')"
    
    def get_duration_days(self):
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        return (end - start).days + 1
    
    def get_budget_per_day(self):
        duration = self.get_duration_days()
        return self.budget / duration if duration > 0 else 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'budget': self.budget,
            'description': self.description,
            'duration_days': self.get_duration_days(),
            'budget_per_day': self.get_budget_per_day()
        }


class Place:
    def __init__(self, name, category, trip_id, address="", notes="", rating=0, visited=0, place_id=None):
        self.id = place_id
        self.name = name
        self.category = category
        self.trip_id = trip_id
        self.address = address
        self.notes = notes
        self.rating = rating
        self.visited = visited
    
    def __str__(self):
        status = "Visited" if self.visited else "Not visited"
        stars = "Rated" * self.rating if self.rating > 0 else "No rated"
        return f"{status} {self.name} ({self.category}) - {stars}"
    
    def __repr__(self):
        return f"Place(id={self.id}, name='{self.name}', category='{self.category}')"
    
    def mark_as_visited(self):
        self.visited = 1
    
    def rate(self, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.rating = rating
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'trip_id': self.trip_id,
            'address': self.address,
            'notes': self.notes,
            'rating': self.rating,
            'visited': bool(self.visited)
        }
