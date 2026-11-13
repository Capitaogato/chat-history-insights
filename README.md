# chat-history-insights

**How do you actually work with AI?** One file, dropped into ChatGPT, turns your own chat history into a personal report: what you use AI for, how well you brief it, whether you check its answers, and what has changed over time.

No installation, no account anywhere else, no data leaves ChatGPT.

*[Deutsche Version weiter unten](#deutsch)*

---

## Quick start

1. Download [`chat-history-insights.py`](chat-history-insights.py) (on the file page: *Download raw file*).
2. Open a new chat in ChatGPT, drag the file in and write: **"Create my AI usage report with the attached file."**
3. Send. ChatGPT guides you through exporting your chats and uploading them, then builds the report.

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
python3 tests/test_insights.py   # 39 scenario tests with synthetic exports
```

The tests simulate incomplete exports, dominant leftover topics, conflicting metadata, careless classification and unstable fields, and check that each is caught.

## License

MIT, © 2026 Philipp Günther ([ai-spark.de](https://ai-spark.de)). Not affiliated with OpenAI. ChatGPT is a trademark of OpenAI.

---

<a id="deutsch"></a>
## Deutsch

**Wie arbeitest du eigentlich mit KI?** Eine Datei, in ChatGPT gezogen, macht aus deinem eigenen Chatverlauf einen persönlichen Bericht, wahlweise auf Deutsch oder Englisch. Er zeigt, wofür du KI nutzt, wie gut du sie instruierst, ob du Antworten prüfst und was sich über die Zeit verändert hat.

### Schnellstart
1. [`chat-history-insights.py`](chat-history-insights.py) herunterladen (auf der Dateiseite: *Download raw file*).
2. In ChatGPT einen neuen Chat öffnen, die Datei hineinziehen und schreiben: **„Erstelle meinen KI-Bericht mit der angehängten Datei.“**
3. Abschicken. ChatGPT führt dich durch den Export und das Hochladen deiner Chats und erstellt dann den Bericht.

Ausführliche Anleitung: [Deutsch](docs/anleitung.de.md)

### Datenschutz
Deine Chats liegen bereits bei OpenAI, der Export ist nur eine Kopie davon. Lade ihn im selben Konto hoch, aus dem er stammt. Im Bericht stehen keine Chat-Texte. Dieses Projekt sammelt keine Daten.

### Grenzen
Der Bericht ist eine strukturierte Selbsteinschätzung und keine Bewertung einer Person. Was die eingebauten Qualitätsprüfungen nicht besteht, wird als nicht belastbar gekennzeichnet oder weggelassen. Methodik: [Methodik und Teststrategie](docs/methodik-und-tests.de.md)
