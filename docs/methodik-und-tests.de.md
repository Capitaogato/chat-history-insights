# Methodik und Teststrategie (Version 2)

## 1. Ursachenanalyse des ersten Tests

| Befund | Ursache im Prompt | Ursache in der Ausführung | Gegenmaßnahme in V2 |
|---|---|---|---|
| 83,5 % der Chats unter „Weitere Themen“ | Methode war freigegeben („deiner Wahl“). Es gab keine Regel für den Restanteil und keinen Prüfschritt. | ChatGPT hat einige Kategorien festgelegt und den Rest in ein Sammelbecken gekippt. | Cluster aus Titel und erster Nachricht. ChatGPT benennt sie oder markiert sie als GEMISCHT. Bei Rest > 15 % werden die Restchats einzeln zugeordnet. Bei > 20 % gelten die Themen als nicht belastbar. Zusätzlich wird die Zuordnung an der Stichprobe gegengeprüft. |
| 76 % „Sonstiges“ bei den Einsatzarten | Es gab keine Definitionen und keine Abgrenzungsregeln. „Sonstiges“ war als normale Kategorie erlaubt. | Einordnung über Suchwörter statt über das Lesen der Chats. | 13 definierte Einsatzarten mit Abgrenzungsregeln. Neu sind „Kurzauskunft“ und „Umformen“; „unklar“ ist kein Sammelbecken. Bei > 15 % unklar folgt eine Wiederholung, bei > 20 % ist die Einsatzart nicht belastbar. |
| Einordnung per Suchwörter | Das Verbot fehlte, und nichts hat es kontrolliert. | Abkürzung durch ChatGPT. | Pflichtfeld „Aufgabe in eigenen Worten“ (mindestens 4 Wörter), Beleg für jedes erkannte Verhalten und eine Sperre gegen Schablonen-Antworten. Die Datei lehnt Pakete ab, die das nicht erfüllen. |
| Denkstufe aus der Einsatzart abgeleitet | Es gab keine Unabhängigkeitsregel. | Abkürzung durch ChatGPT. | Getrennte Durchgänge: A für die Aufgabe, B für Denkstufe und Verhalten. Hängt die Denkstufe zu stark an der Einsatzart (Cramérs V > 0,8, starre Gruppen oder eine Stufe > 80 %), wird sie neu bewertet. Danach gilt sie notfalls als nicht belastbar. |
| Lückenhafte Daten haben den Bericht nicht verhindert | Es gab kein Abbruchkriterium. | – | Pflichtprüfung `daten_pruefen()` mit STOP. Kalenderzeiträume mit Mindestanforderungen. Die Berichtsart wird automatisch heruntergestuft. |
| GPT-Erkennung über `gizmo_id` | **Fehler im Einleseskript:** Es wurde nur ein Feld angenommen. | – | `gizmo_id` und `conversation_template_id` werden beide gelesen. Bei Widersprüchen, unplausibler Abdeckung oder fehlenden Modellangaben weist der Bericht diese Kennzahl nicht aus. |

**Fazit:** Die meisten Fehler sind durch den Prompt entstanden. V1 hat ChatGPT methodische Freiheit gegeben, ohne zu prüfen, wie es sie nutzt. Die Ausführung hat diese Lücken erwartungsgemäß mit Abkürzungen gefüllt. In V2 liegt die Methodik deshalb in der Datei, und jeder Schritt hat ein maschinell geprüftes Bestehenskriterium.

## 2. Prüfstufen und Abbruchkriterien

| Stufe | Prüfung | OK | Wiederholen | Einschränken / Abbrechen |
|---|---|---|---|---|
| G1 Daten | Dateien, Doppelte, Widersprüche, Datum, Lücken, Metadaten | alles plausibel | – | WARN: defekte Dateien oder > 5 % ohne Datum. **STOP:** < 100 auswertbare Chats |
| G2 Zeiträume | Mindestens 60 Chats und mindestens 4 Monate mit je ≥ 3 Chats pro Zeitraum; letzter Chat ≤ 60 Tage alt | VOLL | – | OHNE_VERGLEICH: kein Vergleichszeitraum trägt. BESTAND: Daten nicht aktuell oder kein Zeitraum trägt |
| G3 Themen | Restanteil | ≤ 15 % | > 15 %: Restchats einzeln zuordnen | 15–20 %: WARN. > 20 %: NICHT_BELASTBAR. Übereinstimmung mit der Stichprobe < 70 % → WARN, < 50 % → NICHT_BELASTBAR |
| G4 Durchgang A | Anteil unklar bei Einsatzart und Thema, Schablonen-Sperre | ≤ 15 % | > 15 %: unklare und unsichere Chats neu lesen | nach Wiederholung > 20 % → Merkmal nicht belastbar |
| G5 Durchgang B | Unabhängigkeit der Denkstufe, Belege | V ≤ 0,8 | Denkstufe komplett neu bewerten | danach weiterhin abhängig → nicht belastbar |
| G6 Prüflauf | 40 Chats blind neu eingeordnet: Übereinstimmung ≥ 80 % (Verhalten, κ ≥ 0,6 ab 6 Treffern), ≥ 75 % (Einsatzart, Thema), Denkstufe ± 1 | alle Felder | Felder unter der Schwelle für alle Chats neu, danach neuer Prüflauf | Felder weiterhin unter der Schwelle → nicht belastbar, keine Tipps dazu |
| G7 Auswertung | Monatssumme = Chatzahl, Stichprobe vollständig, Anteile zwischen 0 und 1, gültige Werte | bestanden | – | **STOP:** kein Bericht |
| Veränderung | Merkmal stabil UND n ≥ 40 je Zeitraum UND p < 0,05 UND Differenz ≥ 10 Punkte UND Differenz größer als die Fehlerrate im Prüflauf | „abgesichert“ | – | sonst „Tendenz“ oder „nicht belegbar“, im Bericht blass |
| Reifegrad | nur bei aktuellem Zeitraum; Promptkompetenz aus ≥ 4 stabilen Merkmalen, kritische Kompetenz aus ≥ 2 | Ausgabe als Spanne (Bootstrap) | – | sonst: „Für eine Gesamteinschätzung reichen die Daten nicht.“ |

Gesprächslänge, Themen und genutzte Modelle gehen nicht in den Reifegrad ein. Der Bericht sagt das ausdrücklich.

## 3. Automatisierte Szenario-Tests

`python3 tests/test_insights.py` erzeugt künstliche Exporte mit bekannter Wahrheit und simuliert die Einordnung durch ChatGPT, auch absichtlich fehlerhaft. Aktueller Stand: **38 von 38 Prüfungen bestanden.**

| Szenario | Was geprüft wird |
|---|---|
| Reihenfolge, Reset, zu wenige Chats | Bericht ohne Prüfungen unmöglich; zurückgesetzte Sitzung wird erkannt; STOP blockiert alle weiteren Schritte |
| Unvollständiger Export | abgeschnittene Datei → DEFEKT und WARN; doppelt hochgeladene Datei wird nicht doppelt gezählt; fremde Datei wird übersprungen |
| Widersprüchliche Metadaten | GPT nur in `conversation_template_id` → wird erkannt; abweichende IDs in beiden Feldern → nicht ausgewiesen; fehlende Modellangaben → nicht ausgewiesen |
| Veralteter Export | letzter Chat > 60 Tage → kein „heute“, nur Bestandsaufnahme |
| Datenlücke | fünf leere Monate im letzten Jahr → wird gemeldet |
| Kurzer Zeitraum | nur 9 Monate Daten → kein Vergleich, keine Entwicklungsaussagen, eingeschränkter Bericht |
| Dominante Restkategorie | 4 benannte Cluster, Rest 97 % → Wiederholung erzwungen, Stichprobe blockiert; bleibt der Rest → Themen nicht belastbar, Bericht sagt das |
| 76 % „unklar“ | Wiederholung; bleibt es → Einsatzart nicht belastbar; nach sorgfältigem Neulesen → wieder OK |
| Denkstufe aus der Einsatzart | wird erkannt (V = 1,00), Neubewertung erzwungen |
| Abkürzungen beim Einordnen | fehlende Aufgabenbeschreibung, Schablonen-Text, fehlende Belege → Paket abgelehnt |
| Instabiles Merkmal | „Ziel“ zu 45 % zufällig → Prüflauf scheitert zweimal → nicht belastbar, keine Veränderungsaussage, Tipp dazu abgelehnt |
| Normalfall | VOLL, Rest ≤ 15 %, wahre Zunahme (+26 Punkte) als „abgesichert“ erkannt, Vollbericht |

## 4. Live-Tests in ChatGPT (nicht automatisierbar)

Ob ChatGPT die Regeln beim Einordnen befolgt, lässt sich nur im echten Lauf prüfen. Die Datei erzwingt die Form, nicht die Sorgfalt.

1. **Dein eigener Export, zweimal in getrennten Chats.** Akzeptanz: Einsatzarten und Verhaltensanteile weichen zwischen den Läufen höchstens im Rahmen der ausgewiesenen Spannen ab. Die Berichtsart ist identisch.
2. **Abgleich mit deinem Dashboard.** Zeigen die als abgesichert markierten Veränderungen in dieselbe Richtung? Abweichungen notieren: Wo liegt der Fehler, in V2 oder im Dashboard?
3. **Echte Fehlerfälle provozieren:**
   - nur die Hälfte der Dateien hochladen → Erwartung: Lücke erkannt, eingeschränkter Bericht
   - eine Datei vorher abschneiden → Erwartung: Meldung „nicht vollständig angekommen“
   - einen alten Export verwenden → Erwartung: Bestandsaufnahme ohne „heute“
   - Sitzung zwischen zwei Paketen 30 Minuten liegen lassen → Erwartung: Reset wird erkannt
4. **Unabhängigkeit des Prüflaufs.** Im selben Chat sieht ChatGPT seine früheren Antworten. Gib deshalb einmal die Ausgabe von `rg.pruefpaket()` in einen **neuen** Chat und vergleiche: Die Übereinstimmung darf nicht deutlich sinken. Sinkt sie, ist der Prüflauf im selben Chat zu optimistisch.
5. **Laientest mit zwei bis drei Personen ohne Technikbezug.** Kommen sie ohne Rückfrage bis zum Bericht? Wo stocken sie?
6. **Protokollieren:** Dauer, Zahl der Wiederholungsrunden, Abbrüche, Berichtsart und alle Stellen, an denen ChatGPT Fachbegriffe oder Code gezeigt hat.
