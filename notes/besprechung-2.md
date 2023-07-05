# Zweite Besprechung

## Wissenschaftliche Frage

Diese Studienarbeit soll die Frage beantworten, ob eine Benutzerauthentifizierung anhand Stimmanalyse sicher, effektiv und praktikabel ist.
Dafür werden zunächst Versuche mit verschiedenen Analyse-Methoden durchgeführt und auf dessen Basis eine Applikation entwickelt, die eine Stimm-Authentifizierung demonstriert.

## Gliederung
- *Abstract*
- Einleitung **Lukas**
  - Projektumfeld
  - Wissenschaftliche Frage und Ziel der Arbeit
- Theoretische Grundlagen **Henry**
  - Menschliche Stimme
  - Authentifizierung
  - Audioanalyse und -verarbeitung
    - Fourier-Transformation
    - Dynamic Time Warping
    - Neuronale Netze
    - ...
- Stand der Technik **Johannes**
- Konzeption
  - Anforderungsanalyse **Johannes**
    - Keine neuen Sprecher während der Laufzeit -> Fest definierte Sprecher
  - Konzept Versuchsystem
    - Systemidee
      - Literaturrecherche &rarr; Viele Features &rarr; Evaluierung dieser
      - Erstellen von Parametern &rarr; Begründen warum diese
      - Datensatz &rarr; Bearbeitung des DS
      - Es entsteht ein System, das basierend auf den Input Konfigurationen einen Input Vektor und Test daten berechnet (beschreiben), zur Klassifikation wird ein NN genutzt.
      Abschließend folgt eine Evaluation der ermittelten Daten &rarr; schließen auf richtige Daten
      <!-- TODO Muss Evalution hier schon näher ausgeführt werden, also wie das gemacht wird -->
    - Analyse-Pipeline
      - Feature-Extraktion
        - Fourier-Transformation
        - Dynamic Time Warping
      - Klassifikation
        - Neuronales Netz
      - ...
  - Konzept Demosystem **Henry**
    - Erweitern des Versuchsystems
- Umsetzung der Applikation
  - Technisches Projektumfeld
  - ...
- Evaluation
  - Versuche
    - Durchführung der Versuche
    - Auswertung der Diagramme
    - ...
  - DemoSystem
- Fazit
- Ausblick

## Fragen an Herr Schneider
