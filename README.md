# chat-history-insights

**How do you actually work with AI?** One file, dropped into ChatGPT, turns your entire ChatGPT history – every chat you have ever had – into a personal report: what you use AI for, how well you brief it, whether you check its answers, and what has changed over time.

**Why it's worth it:** most people judge their use of AI by gut feeling. Your own history shows how you really work – where you are already strong, where you can improve (e.g. briefing tasks clearly or checking answers) and which concrete steps help next.

No installation, no account anywhere else, no data leaves ChatGPT.

*[Deutsche Version weiter unten](#deutsch)*

---

## Quick start

The analysis works on your own ChatGPT data export. **Request it first** – it arrives by email and can take a while.

### Part A – Preparation: request your entire ChatGPT history from OpenAI

Under data protection law (in the EU: GDPR, Art. 15 and 20) you are entitled to a copy of all data OpenAI stores about you. The export therefore gives you all your chats, not just recent ones.

1. Open **chatgpt.com** in a browser on your computer, signed in to the account you want to analyse.
2. Click your name or profile picture at the bottom left → **Settings** → **Data controls** → next to "Export data" click **Export** → **Confirm export**.
   - No such option? Use [privacy.openai.com](https://privacy.openai.com) → "Make a Privacy Request" → "I have a consumer ChatGPT account" → "Download my data".
   - Company accounts (ChatGPT Business/Enterprise) have no self-service export – only your IT department can help.
3. Wait for OpenAI's email (usually minutes to hours, occasionally a few days; check your spam folder). **The download link is valid for 24 hours only.**
4. Unzip the download. You only need the files whose names start with **conversations** (e.g. `conversations-000.json`). Count how many there are.

### Part B – Analysis (about 30 minutes)
5. **[Download chat-history-insights.py](https://github.com/Capitaogato/chat-history-insights/releases/latest/download/chat-history-insights.py)** – a plain text file for ChatGPT, nothing to install.
6. Open a new chat in ChatGPT (same account), drag the file in and write: **"Create my AI usage report with the attached file."** Send – without the conversations files for now.
7. Tell ChatGPT how many conversations files you have, then upload them in batches of at most 10. ChatGPT analyses them and gives you your report.

**For non-technical users:** share the simple start page **https://capitaogato.github.io/chat-history-insights/** (download button, the sentence to copy, privacy note, DE/EN).

Step-by-step guide: [English](docs/how-to.en.md) · [Deutsch](docs/anleitung.de.md)

## What you get

An HTML report in **English or German** (your choice) that you open in your browser, with:

- **Your profile today:** strengths, blind spots and one concrete next step
- **What has changed:** last six months compared with the same months a year earlier, showing only changes that hold up statistically
- **How you use AI:** task types, cognitive level of your requests, topics over time
- **Basic facts:** number of chats, active months, length of your requests
- **How the report was made:** sample size, quality checks and limits

Every statement is labelled as *measured*, *classified*, *statistically supported* or *not supported*.

## How it works

The file contains both the instructions for ChatGPT and the analysis logic. ChatGPT runs it in its built-in code environment.

1. **Read and check the data:** files, duplicates, dates, gaps and metadata. If too few chats or outdated data come in, the analysis stops or is downgraded.
2. **Set the time periods:** calendar periods with minimum requirements. If the data is not current, the report makes no claims about "today".
3. **Topics:** derived from your chat titles. If more than 15 % stay unassigned, they are reviewed individually. Above 20 %, topics are not presented as reliable.
4. **Classification:** ChatGPT reads a random sample of 160 chats in two independent passes. Pass A covers the task type, pass B the cognitive level and nine prompting and checking behaviours. Each classification needs a task description in ChatGPT's own words and evidence, otherwise it is rejected.
5. **Quality check:** 40 chats are classified a second time, blind. Fields below 80 % agreement are redone. If they still fail, they are marked as unreliable and no tips are given on them.
6. **Report:** a full report, a limited report or an inventory only, depending on which checks passed.

Details (German): [Methodik und Teststrategie](docs/methodik-und-tests.de.md)

## Privacy

- Your chats are already stored at OpenAI. The export is only a copy, so nothing new goes to any new provider.
- Upload the export only into the **same account** it came from. Never use a company export in a private account or vice versa.
- The report contains no chat texts or titles. You can delete the analysis chat afterwards.
- This project collects nothing. There is no server, no tracking and no telemetry.

## Limits

- The report is a structured self-assessment, not an evaluation of a person. It measures how you write to ChatGPT, not how good the results were.
- Memory, custom instructions and project knowledge are not part of the export, so context may be missing.
- Behaviour is classified by ChatGPT itself and checked against a second pass in the same chat, so the check is likely somewhat optimistic.
- Requires a ChatGPT plan with file uploads and data analysis. Free accounts may hit usage limits.

## For developers

```bash
python3 tests/test_insights.py   # 43 scenario tests with synthetic exports
```

The tests simulate incomplete exports, dominant leftover topics, conflicting metadata, careless classification and unstable fields, and check that each is caught.

## License

MIT, © 2026 Philipp Günther ([ai-spark.de](https://ai-spark.de)). Not affiliated with OpenAI. ChatGPT is a trademark of OpenAI.

---

<a id="deutsch"></a>
## Deutsch

**Wie arbeitest du eigentlich mit KI?** Eine Datei, in ChatGPT gezogen, macht aus deiner gesamten ChatGPT-Historie – allen Chats, die du je geführt hast – einen persönlichen Bericht, wahlweise auf Deutsch oder Englisch. Er zeigt, wofür du KI nutzt, wie gut du sie instruierst, ob du Antworten prüfst und was sich über die Zeit verändert hat.

**Warum sich das lohnt:** Die meisten schätzen ihren Umgang mit KI aus dem Bauch heraus. Deine eigene Historie zeigt, wie du wirklich arbeitest – wo du schon stark bist, wo du besser werden kannst (z. B. Aufgaben klar beschreiben oder Antworten prüfen) und welche konkreten Schritte dir als Nächstes helfen.

### Schnellstart
Die Auswertung arbeitet mit deinem eigenen ChatGPT-Datenexport. **Fordere ihn zuerst an** – er kommt per E-Mail und kann etwas dauern.

**Teil A – Vorbereitung: deine gesamte ChatGPT-Historie bei OpenAI anfordern**

Nach der DSGVO hast du das Recht auf Auskunft über alle bei OpenAI gespeicherten Daten (Art. 15) und auf eine maschinenlesbare Kopie (Art. 20). Der Export liefert dir deshalb alle deine Chats, nicht nur die letzten.

1. **chatgpt.com** am Computer im Browser öffnen, angemeldet mit dem Konto, das du auswerten willst.
2. Unten links auf deinen Namen bzw. dein Profilbild → **Einstellungen** → **Datenkontrollen** → bei „Daten exportieren“ auf **Exportieren** → **Export bestätigen**.
   - Kein Menüpunkt? Dann über [privacy.openai.com](https://privacy.openai.com) → „Make a Privacy Request“ → „I have a consumer ChatGPT account“ → „Download my data“.
   - Firmenkonten (ChatGPT Business/Enterprise) bieten keinen eigenen Export, nur die IT-Abteilung kann helfen.
3. Auf die E-Mail von OpenAI warten (meist Minuten bis Stunden, selten einige Tage; auch im Spam-Ordner nachsehen). **Der Download-Link gilt nur 24 Stunden.**
4. Die ZIP-Datei entpacken. Du brauchst nur die Dateien, deren Name mit **conversations** beginnt (z. B. `conversations-000.json`). Zähle, wie viele es sind.

**Teil B – Auswertung (etwa 30 Minuten)**
5. **[chat-history-insights.py herunterladen](https://github.com/Capitaogato/chat-history-insights/releases/latest/download/chat-history-insights.py)** – eine normale Textdatei für ChatGPT, nichts zu installieren.
6. In ChatGPT einen neuen Chat öffnen (selbes Konto), die Datei hineinziehen und schreiben: **„Erstelle meinen KI-Bericht mit der angehängten Datei.“** Abschicken, noch ohne die conversations-Dateien.
7. ChatGPT die Zahl deiner conversations-Dateien nennen und sie dann in Paketen mit höchstens 10 Stück hochladen. ChatGPT wertet aus und gibt dir deinen Bericht.

Einfache Startseite zum Weitergeben: **https://capitaogato.github.io/chat-history-insights/** · Ausführliche Anleitung: [Deutsch](docs/anleitung.de.md)

### Datenschutz
Deine Chats liegen bereits bei OpenAI, der Export ist nur eine Kopie davon. Lade ihn im selben Konto hoch, aus dem er stammt. Im Bericht stehen keine Chat-Texte. Dieses Projekt sammelt keine Daten.

### Grenzen
Der Bericht ist eine strukturierte Selbsteinschätzung und keine Bewertung einer Person. Was die eingebauten Qualitätsprüfungen nicht besteht, wird als nicht belastbar gekennzeichnet oder weggelassen. Methodik: [Methodik und Teststrategie](docs/methodik-und-tests.de.md)
