import subprocess

# Pfad zur virtuellen Umgebung
venv_path = r"A:\DataCraft\venv\Scripts\activate"

# Part 1 ausführen (Scraping und Speicherung in CSV)
print("Starte Part 1 (Scraping)...")
subprocess.run(f"{venv_path} && python booking_scraper_part1_v3.py", shell=True)

# Part 2 ausführen (Scraping und Speicherung in SQLite DB)
print("Starte Part 2 (Datenverarbeitung und Scraping)...")
subprocess.run(f"{venv_path} && python booking_scraper_part2_v3.py", shell=True)

print("Automatisierung abgeschlossen!")

