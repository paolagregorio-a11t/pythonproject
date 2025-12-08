# Travel Erasmus CLI

Command line application for managing Erasmus trips with SQLite database.

## Installation

1. Clone repository:
git clone https://github.com/paolagregorio-a11t/pythonproject.git
cd pythonproject

text

2. Create virtual environment:
python -m venv venv
venv\Scripts\activate # Windows

source venv/bin/activate # Linux/Mac
text

3. Setup configuration:
copy config\settings.example.ini config\settings.ini

text

4. Create sample database:
python create_sample_data.py

text

5. Run application:
python src/main.py

text

## Project Structure

├── src/ # Source code
│ ├── main.py # Main menu application
│ ├── database.py # SQLite connection and tables
│ ├── models.py # Trip and Place classes
│ └── config.py # Settings loader
├── config/
│ ├── settings.example.ini # Template
│ └── settings.ini # Local config (ignored)
├── data/ # Database (ignored)
│ └── travel_erasmus.db
├── reports/ # CSV exports (ignored)
├── create_sample_data.py
└── README.md

text

## Usage

Menu options:
1. Add trip
2. List trips
3. View trip details
4. Update trip budget
5. Delete trip
6. Manage places in trip
7. Export trips to CSV
8. Exit

## Database

**config/settings.ini**:
[DATABASE]
path = data/travel_erasmus.db

[REPORTS]
path = reports

text

## Sample Data

python create_sample_data.py

text

## Troubleshooting

Config missing: `copy config\settings.example.ini config\settings.ini`

No data: `python create_sample_data.py`

## Author

Paola Gregorio