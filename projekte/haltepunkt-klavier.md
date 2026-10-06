# Haltepunkt-Klavier

Eine Android-App, mit der man einen Ton beliebig lange hält und ihn durch Wischen stufenlos in der Tonhöhe verschiebt, ähnlich einem Bending auf der Gitarre.

## Funktionen

- Ton halten an einem frei gewählten Punkt und per Finger in der Tonhöhe verschieben
- Eigene Klänge laden
- Funktioniert offline, hält den Bildschirm an
- Im Querformat mehr Tasten

## Umsetzung

Zuerst als HTML/JavaScript-Prototyp mit Web Audio, dann als native Android-App in Java. Gebaut ohne Android Studio, direkt mit der Toolchain: aapt2, javac, d8, zipalign, apksigner.

**Ergebnis:** signierte APK für Android 7.0 und neuer (minSdk 24, targetSdk 34)
