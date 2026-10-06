# Automatisierte Video-Pipeline

Für den YouTube-Kanal „The Step File Game“ habe ich eine Pipeline gebaut, die ein Erklärvideo vom Skript bis zur Veröffentlichung weitgehend automatisch erstellt.

## Ablauf

1. Skript gemeinsam mit Claude
2. Vertonung mit einer KI-Stimme (Piper TTS bzw. ElevenLabs)
3. Grafiken und Animationen per Python (Pillow, matplotlib)
4. Schnitt und Export mit ffmpeg
5. Upload über die YouTube Data API v3 (OAuth, eigenes Skript `yt_upload.py`), gekennzeichnet als KI-generierter Inhalt
6. Verteilung auf weitere Kanäle über Metricool

Einzelne Schritte laufen als wiederkehrende geplante Aufgaben.

## Serien

- **Werkbank Welt:** Hauptformat, das erklärt, wie Dinge hergestellt werden. Beispiel: Kapitel 61, „Ein T-Shirt ohne Nähmaschine? Die Schreibtisch-Shirtfabrik“, aktuell der Kanal-Trailer.
- **Platinen-Atlas:** siehe [eigene Projektseite](platinen-atlas.md).

## Was ich dabei gelernt habe

Ein Video lässt sich zu großen Teilen automatisieren, aber Themenwahl, Qualitätskontrolle und Kanalpflege (Beschreibung, Keywords, Trailer) bleiben Handarbeit. Genau dort liegt der Wert.
