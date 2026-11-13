# Your AI usage report – how it works

The simplest version, with a copy button: **https://capitaogato.github.io/chat-history-insights/**

You need a computer and your ChatGPT account. Plan for two stages.

## Part A – Preparation: request your chats from OpenAI
1. **Open chatgpt.com in your browser**, signed in to the account you want to analyse.
2. **Request the export:** click your name or profile picture at the bottom left → **Settings** → **Data controls** → next to "Export data" click **Export** → **Confirm export**.
   - No such option? Use privacy.openai.com → "Make a Privacy Request" → "I have a consumer ChatGPT account" → "Download my data".
   - Company account (Business/Enterprise)? There is no self-service export – only your IT department can help.
3. **Wait for OpenAI's email.** Usually minutes to hours, occasionally a few days. Check your spam folder too. **The download link is only valid for 24 hours.**
4. **Unzip** (Mac: double-click, Windows: right-click → "Extract all"). You **only need the files whose names start with "conversations"**. Ignore everything else. **Count how many there are.**

## Part B – Analysis (about 30 minutes)
5. **Download the analysis file** `chat-history-insights_2.2.py` (download button on the start page). You don't need to open it.
6. **Open a new chat in ChatGPT**, in the same account.
7. **Drag the file in** and write: **"Create my AI usage report with the attached file."** Then send, without the conversations files for now.
8. **ChatGPT asks how many conversations files you have.** Just type the number.
9. **Upload the files in batches of at most 10.** After each batch ChatGPT tells you how many are left.
10. **Wait (15–25 minutes) and open your report:** click the link and double-click the file.
