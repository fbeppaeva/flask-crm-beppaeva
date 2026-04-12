# Flask CRM System

## Beschreibung

Dieses Projekt ist ein CRM-System (Customer Relationship Management), das mit Flask entwickelt wurde.
Es wurde im Rahmen des Kurses „App-Projekte“ umgesetzt und im Laufe mehrerer Sprints erweitert.

## Funktionen

* Customer Management (Kunden anlegen, bearbeiten, löschen)
* Lead Management
* Benutzer-Login mit Rollen (Admin / User)
* SQLite-Datenbank (persistente Speicherung)
* REST API für Kunden
* Swagger API Dokumentation
* Suchfunktion für Kunden

## Technologien

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* Flasgger (Swagger)
* HTML / CSS
* Jira (SCRUM)
* GitHub

## Projektstruktur

* `app.py` – Hauptlogik und Flask-Routen
* `models.py` – Datenmodelle
* `templates/` – HTML-Seiten
* `static/` – CSS und JavaScript
* `docs/` – UML-Diagramme (Use Case, Aktivität, Sequenz, ERD)

## Projekt starten

```bash
python app.py
```

Danach im Browser öffnen:

http://127.0.0.1:5000

## API-Dokumentation

http://127.0.0.1:5000/apidocs

## Login-Daten

* Admin: admin / admin123
* User: user / user123

## Erweiterungen

Im Projekt wurden folgende Erweiterungen umgesetzt:

* Datenbankintegration (SQLite)
* User Authentication
* REST API
* Swagger API Dokumentation
* Suchfunktion

## Hinweis

Das Projekt basiert auf dem MVC-Prinzip und wurde mit dem SCRUM-Ansatz in Jira organisiert.

