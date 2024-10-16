import requests
from bs4 import BeautifulSoup
import csv
import time
import concurrent.futures
from datetime import datetime, timedelta

BAR = chr(9608)  # Character 9608 is '█'


def search_booking(city, checkin, checkout):
    url = "https://www.booking.com/searchresults.de.html"
    params = {
        "ss": city,
        "group_adults": 1,
        "no_rooms": 1,
        "group_children": 0,
        "checkin": checkin,
        "checkout": checkout,
        "distance": 5000
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        hotels = soup.find_all('div', {'data-testid': 'property-card'})
        hotel_data = []

        for hotel in hotels:
            title_tag = hotel.find('div', {'data-testid': 'title'})
            title = title_tag.get_text(strip=True) if title_tag else "Title not available"

            link_tag = hotel.find('a', {'data-testid': "title-link"})
            link = link_tag['href'] if link_tag else "Link not available"

            hotel_data.append((title, link))

        return city, hotel_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return city, []


def read_cities_from_csv(filename):
    cities = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row:  # Only consider non-empty rows
                    cities.append(row[0])  # City name is in the first column
    except FileNotFoundError:
        print(f"File {filename} not found!")
    return cities


# CSV file creation
with open('hotels2.csv', mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['City', 'Hotel Name', 'Link'])

    cities = read_cities_from_csv('orts_liste.csv')
    # Aktuelles Datum und nächster Tag ermitteln
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    # Check-in und Check-out Datum im richtigen Format
    checkin = today.strftime('%Y-%m-%d')
    checkout = tomorrow.strftime('%Y-%m-%d')

    # Using ThreadPoolExecutor for concurrent requests
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_city = {executor.submit(search_booking, city, checkin, checkout): city for city in cities}

        for future in concurrent.futures.as_completed(future_to_city):
            city, hotel_data = future.result()
            for title, link in hotel_data:
                csv_writer.writerow([city, title, link])
            print(f"Data fetched for {city}")

    time.sleep(2)  # Optional pause at the end
