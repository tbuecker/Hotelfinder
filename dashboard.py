import sqlite3
import re
import pandas as pd
import dash
from dash import dcc, html
import dash_leaflet as dl
from dash.dependencies import Input, Output
from datetime import datetime


# Custom REGEXP function for SQLite
def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

# Schritt 1: Verbindung zur SQLite-Datenbank herstellen und REGEXP hinzufügen
def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.create_function("REGEXP", 2, regexp)  # Add custom REGEXP function
    return conn



# Schritt 2: Geodaten und Hotelinformationen aus der Datenbank extrahieren und nach Stadt filtern
def extract_geodata(conn, table_name, geodata_column, city_column=None, city_filter=None, late_checkin=False,
                    early_checkout=False):
    # Basis SQL-Abfrage mit Stadtfilter
    query = f"SELECT {geodata_column}, name, price, checkin_time, checkout_time FROM {table_name} WHERE {city_column} IS NOT NULL AND {country_column} LIKE '%Deutschland%'"

    # Wenn ein Stadtfilter angegeben ist, wird nach der Stadt gefiltert
    if city_filter:
        query += f" AND {city_column} LIKE ?"

    # Filter für Late Check-in und Early Check-out mit REGEXP
    conditions = []
    if late_checkin:
        conditions.append("(checkin_time REGEXP '(18|19|20|21|22|23|00):00')")
    if early_checkout:
        conditions.append("(checkout_time REGEXP '(00|01|02|03|04|05|06|07|08):00')")

    if conditions:
        query += " AND " + " AND ".join(conditions)

    if city_filter:
        df = pd.read_sql(query, conn, params=[f'%{city_filter}%'])
    else:
        df = pd.read_sql(query, conn)

    # Preis in numerische Werte konvertieren, nicht-numerische Werte als NaN behandeln
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # Entferne Einträge mit NaN in der Preis-Spalte
    df = df.dropna(subset=['price'])

    return df


# Schritt 3: Funktion, um den letzten Scraping-Zeitpunkt aus der Datenbank zu holen
def get_last_scraped_at(conn, table_name):
    query = f"SELECT MAX(last_scraped_at) FROM {table_name}"
    result = pd.read_sql(query, conn)
    return result.iloc[0, 0]  # Den ersten (und einzigen) Wert zurückgeben


# Schritt 4: Dash-App erstellen
app = dash.Dash(__name__)

# SQLite Datenbank-Details
db_path = 'hotels5.db'      # Pfad zur SQLite-Datenbank
table_name = 'hotels5'      # Tabellenname in der SQLite-Datenbank
geodata_column = 'geodata'  # Spaltenname mit Geodaten
country_column = 'country'  # Spaltenname der Länder
city_column = 'city'        # Spaltenname der Städte

# CSV-Datei mit Links laden
csv_path = 'hotels2.csv'  # Pfad zur hochgeladenen CSV-Datei
df_links = pd.read_csv(csv_path)  # CSV-Datei laden

# Schritt 5: Initiale Verbindung zur DB herstellen und den letzten Scraping-Zeitpunkt holen
conn = connect_db(db_path)
last_scraped_at = get_last_scraped_at(conn, table_name)
conn.close()

# Schritt 6: Dash Layout erstellen
app.layout = html.Div(style={'backgroundColor': 'black', 'color': 'white', 'padding': '20px'}, children=[
    # Orangener Balken
    html.Div(style={'backgroundColor': '#f58220', 'height': '30px', 'width': '100%'}),

    html.P(),
    html.Img(src='/assets/HSL_Logistic_logo.svg2.png', style={'width': '300px', 'height': 'auto'}),  # Bild hinzufügen
    html.H1("Hotelfinder"),
    html.P([f"Letzte Aktualisierung der Datenbank: {last_scraped_at}"], id='last-scraped-at'),

    # Eingabefeld für den Städtenamen
    html.Label("Geben Sie den Städtenamen ein:"),
    dcc.Input(id="city-input", type="text", placeholder="Stadtname", debounce=True,
              style={'backgroundColor': 'darkgrey', 'color': 'black', 'padding': '10px'}),  # Eingabefeld anpassen
    html.P(),

    # Checkboxen für Late Check-in und Early Check-out
    html.Div([
        dcc.Checklist(
            id="checkin-checkout-filter",
            options=[
                {'label': 'Late Check-in (ab 18:00 Uhr)', 'value': 'late_checkin'},
                {'label': 'Early Check-out (vor 08:00 Uhr)', 'value': 'early_checkout'}
            ],
            value=[],
            labelStyle={'display': 'block', 'color': 'white'}
        )
    ]),

    # Karte und Liste der Hotels in zwei Spalten anzeigen
    html.Div([
        # Leaflet Karte
        html.Div([
            dl.Map(style={'width': '100%', 'height': '600px'}, center=[51.1657, 10.4515], zoom=6, children=[
                dl.TileLayer(),  # Standard-Hintergrundkarte
                dl.LayerGroup(id="layer")
            ])
        ], style={'width': '70%', 'display': 'inline-block'}),

        # Liste der Hotels
        html.Div([

            html.H3("Gefundene Hotels:"),
            html.Ul(id="hotel-list")  # Liste der Hotels
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'})
    ])
])



# Schritt 7: Marker für die Karte und Liste der Hotels aktualisieren, basierend auf der Stadt-Eingabe und Filtern
@app.callback(
    [Output("layer", "children"), Output("hotel-list", "children")],
    [Input("city-input", "value"), Input("checkin-checkout-filter", "value")]
)
def update_markers_and_list(city_filter, checkin_checkout_filter):
    # Leere Liste für Marker und Hotels initialisieren
    markers = []
    hotel_list = []

    # Nur wenn ein Städtefilter gesetzt ist, Hotels und Marker anzeigen
    if city_filter:
        # Verbindung zur SQLite-Datenbank herstellen
        conn = connect_db(db_path)

        # Prüfen, ob Late Check-in und/oder Early Check-out aktiviert sind
        late_checkin = 'late_checkin' in checkin_checkout_filter
        early_checkout = 'early_checkout' in checkin_checkout_filter

        # Geodaten und Hotelinformationen mit Stadtfilter und Check-in/Check-out Filter extrahieren
        df_geodata = extract_geodata(conn, table_name, geodata_column, city_column, city_filter, late_checkin, early_checkout)

        # Sortiere nach Preis (aufsteigend)
        df_geodata = df_geodata.sort_values(by="price", ascending=True)

        # Iteriere über jede Zeile in den Geodaten
        for index, row in df_geodata.iterrows():
            geodata = row[geodata_column]
            hotel_name = row["name"]
            hotel_price = row["price"]

            # Marker zur Karte hinzufügen
            if isinstance(geodata, str):
                try:
                    lat, lon = map(float, geodata.split(','))  # Konvertiere zu Float

                    # Erstelle einen Popup mit dem Hotelnamen und Preis
                    popup = dl.Popup([
                        html.H3(f"{hotel_name}"),
                        html.P(f"Preis: {hotel_price}€")
                    ])

                    # Füge den Marker mit dem Popup zur Karte hinzu
                    markers.append(dl.Marker(position=[lat, lon], children=[popup]))

                except ValueError:
                    continue  # Ignoriere fehlerhafte Daten

            # Suche den Hotelnamen in der CSV-Datei und extrahiere den Link
            hotel_link = df_links[df_links['Hotel Name'] == hotel_name]['Link'].values
            if len(hotel_link) > 0:
                # Wenn der Link gefunden wurde, erstelle einen klickbaren Link
                hotel_list.append(html.Li(html.A(f"{hotel_name}", href=hotel_link[0], target="_blank")))
                hotel_list.append(html.Li(f"Preis: {hotel_price}€"))
                hotel_list.append(html.P())
            else:
                # Wenn kein Link gefunden wurde, einfach den Namen und Preis anzeigen
                hotel_list.append(html.Li(f"{hotel_name} - Preis: {hotel_price}€"))

        conn.close()  # Verbindung zur Datenbank schließen

    return markers, hotel_list



# Schritt 8: App ausführen
if __name__ == "__main__":
    app.run_server(debug=True)
