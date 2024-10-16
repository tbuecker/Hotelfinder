import requests
from bs4 import BeautifulSoup
import sqlite3
import csv
import re
import time
import random
import concurrent.futures
import os  # Importiere os zum Löschen der DB
from threading import Lock

# Charakter für die Fortschrittsanzeige
BAR = chr(9608)

# Fortschrittsbalken-Funktion
def getProgressBar(progress, total, barWidth=40):
    """Erstellt einen Fortschrittsbalken-String."""
    progressBar = '['
    if progress > total:
        progress = total
    if progress < 0:
        progress = 0

    numberOfBars = int((progress / total) * barWidth)
    progressBar += BAR * numberOfBars  # Fortschrittsbalken hinzufügen
    progressBar += ' ' * (barWidth - numberOfBars)  # Leeren Raum hinzufügen
    progressBar += ']'  # Ende des Balkens

    percentComplete = round(progress / total * 100, 1)
    progressBar += f' {percentComplete}% {progress}/{total}'  # Prozentsatz und Zahlen hinzufügen

    return progressBar  # Fortschrittsbalken-String zurückgeben

# Funktion zum Scrapen der Hoteldaten
def scrape_hotel_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)  # Timeout auf 5 Sekunden
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Name des Hotels scrapen
        name_tag = soup.find('h2', {'class': re.compile(r'pp-header__title')})
        name = name_tag.get_text(strip=True) if name_tag else "Name nicht verfügbar"

        # Preis scrapen
        price_tag = soup.find('span', {'class': re.compile(r'prco-valign-middle-helper')})
        price = price_tag.get_text(strip=True) if price_tag else "Preis nicht verfügbar"
        new_price = price.lstrip('€').strip()

        # Adresse scrapen
        address_tag = soup.find('span', {'class': re.compile(r'hp_address_subtitle')})
        address = address_tag.get_text(strip=True) if address_tag else "Adresse nicht verfügbar"
        address_parts = re.split(',', address)

        # Straße
        street = address_parts[0].strip() if len(address_parts) > 0 else "Straße nicht verfügbar"

        # Stadt extrahieren, falls mit einer 5-stelligen Zahl (Postleitzahl) beginnt
        city = "Stadt nicht verfügbar"
        if len(address_parts) > 1:
            potential_city = address_parts[1].strip()
            # Prüfen, ob die Stadt mit einer fünfstelligen Zahl beginnt
            if re.match(r'^\d{5}', potential_city):
                city = potential_city
            elif len(address_parts) > 2:  # Fallback auf den nächsten Teil, falls keine fünfstellige Zahl vorhanden ist
                city = address_parts[2].strip()

        # Land (letzter Teil)
        country = address_parts[-1].strip() if len(address_parts) > 2 else "Land nicht verfügbar"

        # Check-in-Zeit scrapen
        checkin_time_tag = soup.find('div', {'class': re.compile(r'f565581f7e')})
        checkin_time = checkin_time_tag.get_text(strip=True) if checkin_time_tag else "Check-in-Zeit nicht verfügbar"
        new_checkin_time = re.split('Gäste |Bitte', checkin_time)[0]

        # Check-out-Zeit scrapen
        checkout_time_tag = soup.find_all('div', {'class': re.compile(r'f565581f7e')})
        if len(checkout_time_tag) > 1:
            checkout_time = checkout_time_tag[1].get_text(strip=True)
        else:
            checkout_time = "Check-out-Zeit nicht verfügbar"

        # Suche nach den Geodaten
        geo_tag = soup.find('a', id="hotel_header")
        latlng = geo_tag['data-atlas-latlng'] if geo_tag and 'data-atlas-latlng' in geo_tag.attrs else "Geodata nicht verfügbar"

        return [name, new_price, street, city, country, new_checkin_time, checkout_time, latlng]

    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der URL: {e}")
        return None

# Funktion zum Verarbeiten einer einzelnen Zeile
def process_row(row, lock, progress, total):
    url = row[2]  # Annahme: Der Link ist in der zweiten Spalte
    scraped_data = scrape_hotel_data(url)

    if scraped_data:
        with lock:
            batch_data.append(scraped_data)
            # Fortschrittsbalken nur gelegentlich aktualisieren
            if progress[0] % 10 == 0 or progress[0] == total:  # Alle 10 Schritte
                progressBar = getProgressBar(progress[0], total)
                print(f'\r{progressBar}', end='', flush=True)

        # Zufällige Pause zwischen 1 und 2 Sekunden
        time.sleep(random.uniform(1, 2))
    else:
        with lock:
            if progress[0] % 10 == 0 or progress[0] == total:  # Alle 10 Schritte
                progressBar = getProgressBar(progress[0], total)
                print(f'\r{progressBar}', end='', flush=True)

    with lock:
        progress[0] += 1  # Fortschritt erhöhen

# Alte DB-Datei löschen, falls vorhanden
db_file = 'hotels5.db'
# if os.path.exists(db_file):
#     os.remove(db_file)

# SQLite-Datenbank einrichten
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Drop the table if it exists
cursor.execute('DROP TABLE IF EXISTS hotels5')

# Create the table with a new column for the timestamp
cursor.execute('''
    CREATE TABLE hotels5(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INT,
        street TEXT,
        city TEXT,
        country TEXT,
        checkin_time TEXT,
        checkout_time TEXT,
        geodata REAL,
        last_scraped_at TEXT
    )
''')
conn.commit()

# Datei mit den Links einlesen
with open('hotels2.csv', mode='r', newline='', encoding='utf-8') as infile:
    csv_reader = csv.reader(infile)
    headers = next(csv_reader)  # Überspringen der Headerzeile

    rows = list(csv_reader)  # Alle Zeilen in eine Liste lesen
    total_rows = len(rows)  # Gesamtanzahl der Zeilen (Hotels)

    # Fortschrittsanzeige initialisieren
    print(f"Starte das Scraping von {total_rows} Hotels...")

    # Lock für Thread-sichere Operationen
    lock = Lock()

    # Batch-Daten initialisieren
    batch_data = []
    batch_size = 50  # Größere Batches zum Einfügen in die Datenbank

    # Fortschrittszähler
    progress = [0]

    # Aktueller Timestamp für den Scraping-Durchlauf
    current_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # ThreadPoolExecutor für paralleles Scraping
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [
            executor.submit(process_row, row, lock, progress, total_rows)
            for row in rows
        ]

        # Warten, bis alle Futures abgeschlossen sind
        concurrent.futures.wait(futures)

    # Nach dem Scraping alle verbleibenden Daten in die Datenbank einfügen
    if batch_data:
        cursor.executemany('''
            INSERT OR REPLACE INTO hotels5(name, price, street, city, country, checkin_time, checkout_time, geodata, last_scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [data + [current_timestamp] for data in batch_data])  # Timestamp hinzufügen
        conn.commit()

    # Finales Commit sicherstellen
    conn.commit()

# Verbindung zur Datenbank schließen
conn.close()

print("\nScraping abgeschlossen!")
