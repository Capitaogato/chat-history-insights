# Dein KI-Bericht – so geht's

Die einfachste Fassung mit Bildern und Kopieren-Knopf: **https://capitaogato.github.io/chat-history-insights/**

Du brauchst einen Computer und deinen ChatGPT-Zugang. Plane zwei Etappen ein.

## Teil A – Vorbereitung: Chats bei OpenAI anfordern
1. **chatgpt.com im Browser öffnen** und mit dem Konto anmelden, das du auswerten willst.
2. **Export anfordern:** unten links auf deinen Namen bzw. dein Profilbild klicken → **Einstellungen** → **Datenkontrollen** → bei „Daten exportieren“ auf **Exportieren** → **Export bestätigen**.
   - Kein Menüpunkt? Dann über privacy.openai.com → „Make a Privacy Request“ → „I have a consumer ChatGPT account“ → „Download my data“.
   - Firmenkonto (Business/Enterprise)? Dort gibt es keinen eigenen Export, nur die IT-Abteilung kann helfen.
3. **Auf die E-Mail von OpenAI warten.** Das dauert meist Minuten bis Stunden, selten einige Tage. Schau auch im Spam-Ordner nach. **Der Download-Link gilt nur 24 Stunden.**
4. **ZIP entpacken** (Mac: Doppelklick, Windows: Rechtsklick → „Alle extrahieren“). Du brauchst **nur die Dateien, deren Name mit „conversations“ beginnt**. Alles andere ignorierst du. **Zähle, wie viele es sind.**

## Teil B – Auswertung (etwa 30 Minuten)
5. **Auswertungsdatei herunterladen:** `chat-history-insights_2.2.py` (Download-Button auf der Startseite). Du musst sie nicht öffnen.
6. **Neuen Chat in ChatGPT öffnen**, im selben Konto.
7. **Die Datei hineinziehen** und schreiben: **„Erstelle meinen KI-Bericht mit der angehängten Datei.“** Dann abschicken, noch ohne die conversations-Dateien.
8. **ChatGPT fragt nach der Zahl der conversations-Dateien.** Schreib einfach die Zahl.
9. **Die Dateien in Paketen mit höchstens 10 Stück hochladen.** ChatGPT sagt dir nach jedem Paket, wie viele noch fehlen.
10. **Warten (15–25 Minuten) und den Bericht öffnen:** auf den Link klicken, Datei mit Doppelklick öffnen.
