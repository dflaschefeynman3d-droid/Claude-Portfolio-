# Platinen-Atlas

Eine Erklärvideo-Serie, die alltägliche Produktfunktionen auf die passende Platine zurückführt: Was steckt elektronisch hinter „Heizen“, „Daten speichern“ und Co.?

## Veröffentlicht

- Folge F01: [Was steckt in jedem Heizgerät? Die Platine dahinter](https://youtu.be/idlLb3qx06M), mit Thumbnail und Kapitelmarken
- Short: [Diese Platine steckt in jedem Heizgerät](https://youtube.com/shorts/KCcx_EzmOT0)

## Wie es gemacht ist

- Die Platine entsteht als Konzeptgrafik in einem eigenen Python-Skript: Bauteile, Pads, Leiterbahnen und Vias mit Koordinaten in Millimetern, gezeichnet mit Pillow.
- Dasselbe Datenmodell treibt die Animationen im Video an, Bild und Erklärung passen dadurch immer zusammen.
- Skript mit Claude, Vertonung per KI-Stimme, Schnitt und Export mit ffmpeg, Upload über die YouTube-API.

## Grenzen

Die Bauteiltypen sind real, das Layout ist aber Konzeptgrafik: kein geprüfter Schaltplan, keine Design-Rule-Prüfung, keine Gerber-Dateien. Für die Erklärung reicht das, für die Fertigung nicht.

**Werkzeuge:** Python, Pillow, ffmpeg, Text-to-Speech, YouTube Data API v3
