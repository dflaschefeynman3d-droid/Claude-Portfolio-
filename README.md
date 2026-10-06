# Dirk Flasche – Portfolio

**KI-Praktiker für Content-Produktion und Lerninhalte.** Ich baue mit Claude und weiteren KI-Werkzeugen fertige Ergebnisse: Erklärvideos mit automatisierter Pipeline, Android-Apps, Spiele und Musik. Mein Schwerpunkt ist, Technik so aufzubereiten, dass man ohne Vorwissen folgen kann.

- Werkstudent für Content Development und Website-Administration bei Neoprint3D (seit Mai 2026)
- Gründer und Geschäftsführer der Feynman3D UG, Verkauf von 3D-gedruckten Produkten (2019–2024)
- Über 130 Coursera-Zertifikate seit 2020, darunter vier Spezialisierungen zu KI ([Übersicht](zertifikate.md))

## Lerninhalte und KI-Wissen

Inhalte, mit denen andere lernen, und das Verfolgen der KI-Entwicklung. Details auf der [Projektseite](projekte/lerninhalte.md).

| Inhalt | Was es ist | Format |
| --- | --- | --- |
| [KI-Update: Die Woche der Agenten](inhalte/ki-update-woche-der-agenten.md) | Wochenrückblick zu KI: neue Modelle, Agenten, Regulierung, Lernen mit KI, belegt mit 19 Quellen | Podcast-Skript, 2 Stimmen, ca. 15 min |
| [Epsi lernt Analysis](projekte/lerninhalte.md#epsi-lernt-analysis) | Lern-App mit 222 Karten, Begleiterfigur und Bosskämpfen pro Lektion | [Web-App öffnen](https://raw.githack.com/dflaschefeynman3d-droid/Claude-Portfolio-/main/apps/epsi-lernt-analysis/index.html) |
| [Analysis Formelwerk](projekte/lerninhalte.md#analysis-formelwerk) | 75 Formeln in drei Übungsformen: Leitner-Karteikasten, Zeitspiel, Memory | [Web-App öffnen](https://raw.githack.com/dflaschefeynman3d-droid/Claude-Portfolio-/main/apps/analysis-formelwerk/index.html) |
| [ERW Lernkontor](projekte/lerninhalte.md#erw-lernkontor) | Lernplaner mit Klausur-Countdown, Trefferquote und Klausuranalyse | [Web-App öffnen](https://raw.githack.com/dflaschefeynman3d-droid/Claude-Portfolio-/main/apps/erw-lernkontor/index.html) |
| [AI Weekly Ep. 1: Diffusion Models](inhalte/ai-weekly-ep1-diffusion-models.md) | Erklärvideo-Skript zu Bild-KI mit Lizenzprüfung aller Abbildungen | Video-Skript, 10 min, Englisch |
| [Eigenes Musikstück schreiben](inhalte/eigenes-musikstueck-schreiben.md) | Anleitung in zehn Schritten für Einsteiger ohne Notenkenntnisse | Anleitung |

## Projekte

| Projekt | Was es ist | Ergebnis | Werkzeuge |
| --- | --- | --- | --- |
| [Platinen-Atlas](projekte/platinen-atlas.md) | Erklärvideo-Serie: Welche Platine steckt hinter einer Produktfunktion? | [Folge F01 „Heizen“](https://youtu.be/idlLb3qx06M) und [Short](https://youtube.com/shorts/KCcx_EzmOT0) veröffentlicht | Python, Pillow, ffmpeg, KI-Stimme, YouTube-API |
| [Automatisierte Video-Pipeline](projekte/video-pipeline.md) | Vom Skript bis zum Upload weitgehend automatisiert, Serie „Werkbank Welt“ | Laufender YouTube-Kanal „The Step File Game“ | Claude, Python, ffmpeg, TTS, YouTube Data API v3, Metricool |
| [Haltepunkt-Klavier](projekte/haltepunkt-klavier.md) | Android-App: Töne halten und per Finger stufenlos in der Tonhöhe verschieben | [Im Browser spielen](https://raw.githack.com/dflaschefeynman3d-droid/Claude-Portfolio-/main/apps/haltepunkt-klavier/index.html) · [APK](releases/haltepunkt-klavier-1.0.apk) | HTML/JS-Prototyp (Web Audio), Java, Android-Build ohne Android Studio |
| [Schnipselklavier](projekte/schnipselklavier.md) | Sampler-App: zerlegt eine Audiodatei in Stücke, jedes auf eigener Tastatur spielbar | [Im Browser spielen](https://raw.githack.com/dflaschefeynman3d-droid/Claude-Portfolio-/main/apps/schnipselklavier/index.html) · [APK v1.1](releases/schnipselklavier-1.1.apk) | Web Audio, Java, aapt2, d8, apksigner |
| [Ringwacht](projekte/ringwacht.md) | Eigenes abstraktes Strategiespiel | In der Engine Ludii umgesetzt, KI-gegen-KI-Partien zur Balance, druckfertig bei The Game Crafter | Ludii, The Game Crafter |
| [Punktiert in F](projekte/komposition.md) | Komposition nach eigenem 15-Schritte-Regelwerk, mit synthetischem Saxophon-Growl | MP3 und MIDI | Python (numpy, scipy, mido), CC0-Samples (VCSL) |
| [Erzähl-Prompt](projekte/erzaehl-prompt.md) | Wiederverwendbarer Prompt für Kurzgeschichten auf Basis der Leseforschung | Prompt und Beispielgeschichte (ca. 3.000 Wörter) | Claude, wissenschaftliche Literatur |

## Apps selbst bauen

Haltepunkt-Klavier und Schnipselklavier sind Web-Apps (eine HTML-Datei mit Web Audio), die ein eigenes Skript in eine Android-App verpackt. Das Skript lädt die Schriften lokal herein, erzeugt das App-Symbol, kompiliert die Java-Hülle und signiert die APK, ganz ohne Android Studio:

```
python3 tools/build_apk.py apps/haltepunkt-klavier apps/schnipselklavier
```

Voraussetzungen: Android SDK (Platform 34, Build-Tools 34.0.0), JDK, Python mit Pillow. Zum Installieren die APK auf dem Handy öffnen und die Installation aus dieser Quelle erlauben.

## Arbeitsweise

Ich nutze KI nicht zum Ausprobieren, sondern als Werkzeug mit klarem Ziel. Ich entscheide, was gebaut wird, prüfe die Ergebnisse und weiß aus den Projekten, wo KI zuverlässig ist und wo man nachprüfen muss. Bei jedem Projekt halte ich fest, was es kann und was nicht. Die Platine im Platinen-Atlas ist zum Beispiel Konzeptgrafik, kein fertigungsreifes Layout.

## Kenntnisse

- **KI:** Claude (täglich), Prompt-Gestaltung, KI-Stimmen (ElevenLabs, Piper), Bild- und Musikgenerierung
- **Automatisierung:** Python-Skripte, YouTube Data API, Metricool, wiederkehrende Aufgaben
- **Programmierung:** Python, C# mit Unity, Java für Android, HTML/JavaScript
- **Medien:** Videoproduktion mit Python und ffmpeg, Canva
- **Technik:** 3D-Druck, CAD mit Fusion 360

## Ausbildung

- Wirtschaftsinformatik (ohne Abschluss), FernUniversität in Hagen, seit Oktober 2024
- Abitur, Altes Kurfürstliches Gymnasium Bensheim, 2014
