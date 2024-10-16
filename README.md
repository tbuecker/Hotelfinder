# Hotelfinder

## Projektübersicht
Das Projekt wurde im Rahmen einer Kooperation mit der HSL-Logistik GmbH, einem Eisenbahnverkehrsunternehmen, durchgeführt. Ziel des Projekts war die systematische Erfassung von Hotelpreisen in relevanten Städten und Regionen Deutschlands, um Triebfahrzeugführern nach einem langen Arbeitstag geeignete und aktuelle Übernachtungsmöglichkeiten anzubieten. Das Projektteam bestand aus drei Mitgliedern: 
Thomas Bücker, Demian In den Birken und Okan Çolak

•	Projektleitung und Präsentation: Thomas Bücker, Okan Çolak
o	Verantwortlich für die Organisation des Projekts und die Präsentation der finalen Ergebnisse. Beide übernehmen gemeinsam die Vorstellung des Gesamtprojekts, der erreichten Meilensteine und der Schlussfolgerungen.
•	Entwickler für Datenextraktion und Präsentation: Thomas Bücker, Okan Çolak
o	Entwickelten die Webscraping-Skripte und leiteten den technischen Teil des Projekts. Bei der Präsentation werden sie die technischen Details zu den verwendeten Tools und Technologien (Selenium, SQLite, Dash) sowie die Herausforderungen und Lösungen während der Datenextraktion erläutern.
•	Dokumentation, Berichterstellung und Präsentation: Thomas Bücker, Demian In den Birken, Okan Çolak
o	Sie waren für die Erstellung der Projektdokumentation und die Zusammenstellung des Abschlussberichts verantwortlich. In der Präsentation wird ein Fokus auf die Projektdokumentation, die verwendeten Methoden und die Ergebnisse der Datenanalyse gelegt.
•	Visualisierungsexperte : Thomas Bücker
o	Verantwortlich für die Entwicklung des interaktiven Dashboards, das die Daten visualisiert. Bei der Präsentation wird er das Dashboard vorstellen, die Datenvisualisierung erläutern und die Vorteile der interaktiven Elemente hervorheben.



##Projektziele
•	Webscraping:  Automatisierte Erfassung von Hotelpreisen von Booking.com. Andere Plattformen wie Trivago wurden zunächst in Betracht gezogen, jedoch aufgrund von Instabilität und inkonsistenter Datenstrukturen nicht verwendet.
•	Datenbank:  Speicherung der gesammelten Daten in einer strukturierten SQLite-Datenbank.
•	Visualisierung:  Erstellung eines Dashboards zur Darstellung der gesammelten Hotelpreisdaten. Das Dashboard ermöglicht es dem Nutzer, aktuelle Hotelpreise einzusehen und nach verschiedenen Kriterien wie Stadt, Preis und Verfügbarkeit zu filtern. Es bietet eine übersichtliche und interaktive Oberfläche, um die erfassten Daten effizient zu präsentieren, ohne dabei tiefere Datenanalysen durchzuführen.
•	Manuelle Datenerfassung:  In der aktuellen Version des Projekts wurde die Hotelpreisdatenbank einmalig erstellt, ohne Mechanismen zur kontinuierlichen Aktualisierung. Eine regelmäßige Aktualisierung der Hotelpreise kann in Zukunft durch manuelle Ausführung des Scraping-Skripts oder durch Erweiterung der Automatisierung erfolgen.


##Vorgehensweise
1.	Anforderungsanalyse:  Zu Beginn des Projekts wurden die Anforderungen in Zusammenarbeit mit HSL-Logistik definiert. Wichtig war es, eine flexible Datenbankstruktur zu entwickeln, die zukünftige Erweiterungen ermöglicht.
2.	Technologieauswahl und Setup:  Die Technologie wurde auf Basis der Projektanforderungen ausgewählt und eingerichtet. Der Fokus lag auf der Stabilität und Erweiterbarkeit des Webscraping-Skripts, sowie einer effizienten Datenverarbeitung.
3.	Datenextraktion:  Das Webscraping-Skript wurde entwickelt, um auf Booking.com die Hotelpreise, Verfügbarkeiten und Standorte von Hotels zu extrahieren. Zunächst wurde auch mit der Trivago-Seite gearbeitet, jedoch aufgrund der instabilen Datenstruktur nicht weiterverfolgt.
4.	Datenbankdesign und -integration:  Die erfassten Daten wurden in einer SQLite-Datenbank gespeichert, welche strukturiert und leicht zugänglich ist. Die Datenbank ermöglicht eine effiziente Abfrage und Verwaltung der Hotelpreisdaten.
5.	Visualisierung:  Ein interaktives Dashboard wurde entwickelt, das die gesammelten Daten in einer benutzerfreundlichen Oberfläche darstellt. Die Benutzer können Hotelpreise filtern und eine geographische Übersicht der Hotels auf einer Karte anzeigen lassen.
6.	Tests und Qualitätssicherung: Um die Stabilität und Korrektheit des Systems zu gewährleisten, wurden umfassende Tests für die Datenextraktion, die Datenbank und das Dashboard durchgeführt.
7.	Dokumentation und Übergabe:  Eine umfassende Projektdokumentation wurde erstellt, die die wichtigsten Projektschritte und Erkenntnisse zusammenfasst. Das Projekt wurde an HSL-Logistik zur weiteren Nutzung übergeben.


##Herausforderungen und Lösungen
•	Instabilität der Webseitenstruktur:  Trivago wurde aufgrund inkonsistenter Datenstrukturen und mangelnder Stabilität nicht verwendet. Stattdessen wurde ausschließlich Booking.com als verlässliche Datenquelle genutzt.
•	Datenaktualisierung:  Eine automatisierte Datenaktualisierung wurde im aktuellen Projektstand nicht implementiert. Stattdessen erfolgte die Datenerfassung einmalig, um eine Basisdatenbank der Hotelpreise zu erstellen. Für zukünftige Erweiterungen besteht die Möglichkeit, das Scraping-Skript manuell erneut auszuführen oder es, um automatisierte Prozesse zur regelmäßigen Aktualisierung der Datenbank zu ergänzen.
•	Visualisierung:  Die visuelle Darstellung der Daten wurde durch das interaktive Dashboard erleichtert, das geografische und preisliche Informationen übersichtlich darstellt.



##Fazit
Das Projekt ermöglicht es der HSL-Logistik, die Hotelpreise in den relevanten Regionen effizient zu überwachen und Triebfahrzeugführern passende Übernachtungsmöglichkeiten anzubieten. Die Implementierung eines stabilen Webscraping-Tools, die Speicherung in einer strukturierten Datenbank und die Entwicklung eines interaktiven Dashboards stellen sicher, dass die erfassten Daten für zukünftige Auswertungen und Optimierungen nutzbar sind.
Ausblick
Für zukünftige Erweiterungen könnte eine regelmäßige Datenaktualisierung durch Automatisierung des Webscraping-Prozesses in Betracht gezogen werden. Zudem wäre es möglich, weitere Datenquellen einzubinden, um eine breitere Abdeckung der Hotelpreisdaten zu gewährleisten. Auch die Nutzung von APIs könnte untersucht werden, falls sie für die relevanten Plattformen verfügbar sind. 

