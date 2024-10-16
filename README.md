# HSL-Logistik Hotelpreiserfassung

Dieses Projekt wurde in Zusammenarbeit mit der **HSL-Logistik GmbH** durchgeführt, einem Eisenbahnverkehrsunternehmen in Deutschland. Ziel war es, eine systematische Erfassung von Hotelpreisen in relevanten Städten und Regionen durchzuführen, um Triebfahrzeugführern nach einem langen Arbeitstag passende Übernachtungsmöglichkeiten anbieten zu können.

## Projektübersicht

Das Projektteam bestand aus:

- **[Thomas Bücker](https://github.com/tbuecker)** – Projektleitung, Entwickler, Dokumentation, Visualisierung
- **[Demian In den Birken](https://github.com/demmdata1990)** – Dokumentation
- **[Okan Çolak](https://github.com/Okan-Colak)** – Projektleitung, Entwickler, Dokumentation

### Verantwortlichkeiten

- **Projektleitung und Präsentation**: Thomas Bücker, Okan Çolak
  - Organisation des Projekts, Vorstellung der finalen Ergebnisse.
  
- **Datenextraktion und Präsentation**: Thomas Bücker, Okan Çolak
  - Entwicklung der Webscraping-Skripte (Selenium) und Datenbank (SQLite).
  
- **Dokumentation und Bericht**: Thomas Bücker, Demian In den Birken, Okan Çolak
  - Erstellung der Projektdokumentation und des Abschlussberichts.
  
- **Visualisierung**: Thomas Bücker
  - Entwicklung des Dashboards mit Dash zur interaktiven Visualisierung der Daten.

## Projektziele

1. **Webscraping**: Automatisierte Erfassung von Hotelpreisen auf **Booking.com**.
2. **Datenbank**: Speicherung der gesammelten Daten in einer **SQLite**-Datenbank.
3. **Visualisierung**: Entwicklung eines interaktiven Dashboards zur Darstellung der Hotelpreise.
4. **Manuelle Datenerfassung**: Einmalige Erfassung der Hotelpreise, ohne automatische Aktualisierung.

## Vorgehensweise

1. **Anforderungsanalyse**: In Zusammenarbeit mit HSL-Logistik wurden die Anforderungen definiert.
2. **Technologieauswahl und Setup**: Auswahl von Selenium für Webscraping, SQLite für die Datenbank und Dash für die Visualisierung.
3. **Datenextraktion**: Entwicklung eines Webscraping-Skripts, das Hotelpreise von Booking.com sammelt.
4. **Datenbankdesign**: Strukturierte Speicherung der Daten in einer SQLite-Datenbank.
5. **Visualisierung**: Erstellung eines interaktiven Dashboards zur Filterung und Anzeige der gesammelten Daten.
6. **Tests und Qualitätssicherung**: Durchführung umfassender Tests zur Sicherstellung der Datenqualität.
7. **Dokumentation und Übergabe**: Erstellung einer Projektdokumentation und Übergabe an HSL-Logistik.

## Herausforderungen und Lösungen

- **Instabilität der Webseitenstruktur**: Trivago wurde aufgrund inkonsistenter Datenstrukturen nicht verwendet. Booking.com erwies sich als stabiler.
- **Datenaktualisierung**: Die Datenaktualisierung erfolgt nicht automatisch. Eine manuelle Ausführung des Webscraping-Skripts ermöglicht eine zukünftige Aktualisierung der Hotelpreise.
- **Visualisierung**: Das interaktive Dashboard erleichtert die Visualisierung von geografischen und preislichen Informationen.

## Technologien

- **Web Scraping**: [Python](https://www.python.org/)
- **Datenbank**: [SQLite](https://www.sqlite.org/index.html)
- **Visualisierung**: [Dash](https://plotly.com/dash/)

## Installationsanleitung

1. Klone das Repository:
```
   git clone https://github.com/tbuecker/Hotelfinder.git
```

2. Installiere die benötigten Abhängigkeiten:
```
- pip install -r requirements.txt
```

3. Führe das Webscraping-Skript aus:
```
- python run_all.py
```

4. Starte das Dashboard:
```
- python dashboard.py
```
