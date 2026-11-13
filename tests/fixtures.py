"""Erzeugt künstliche ChatGPT-Exporte mit bekannter Wahrheit (truth.json) für Tests."""
import json, random, uuid, os, datetime as dt
TOPICS = {"Finanzen / Steuern": ["Steuererklärung", "Werbungskosten", "Pendlerpauschale"], "Finanzen / Geldanlage": ["ETF Sparplan", "Tagesgeld", "Depot"],
 "Haus / Energie": ["Wärmepumpe", "Photovoltaik", "Stromtarif"], "Familie / Kinder": ["Kindergeburtstag", "Hausaufgaben Mathe", "Elternabend"],
 "Beruf / Bewerbung": ["Anschreiben", "Lebenslauf", "Vorstellungsgespräch"], "Beruf / Führung": ["Teammeeting", "Mitarbeitergespräch", "Feedback"],
 "Freizeit / Kochen": ["Sauerteigbrot", "Pasta Rezept", "Grillen"], "Freizeit / Reisen": ["Reise Portugal", "Städtetrip Rom", "Camping"],
 "Technik / Excel": ["Pivot Tabelle", "SVERWEIS", "Excel Makro"], "Technik / Programmieren": ["Python Skript", "SQL Abfrage", "Fehlermeldung Docker"],
 "Gesundheit / Sport": ["Laufplan", "Rückentraining", "Ernährung Marathon"], "Kommunikation / Social Media": ["LinkedIn Beitrag", "Instagram Post", "Newsletter"]}
TASKS = ["schreiben", "code", "analyse", "recherche", "lernen", "bewerten", "rat", "planen", "ideen", "umformen", "kurzauskunft"]
TEMPL = {"schreiben": ("Schreib eine Mail zum Thema {t}", 3), "code": ("Ich bekomme bei {t} einen Fehler, kannst du das lösen?", 3),
 "analyse": ("Hier sind meine Zahlen zu {t}: 12, 15, 9, 22. Woran liegt der Einbruch im dritten Monat?", 4), "recherche": ("Finde aktuelle Angebote und Quellen zu {t}", 2),
 "lernen": ("Erklär mir, wie {t} funktioniert", 2), "bewerten": ("Ich habe zwei Angebote zu {t}: A für 300 €, B für 420 € mit Service. Welches ist besser?", 5),
 "rat": ("Soll ich mich mit {t} jetzt beschäftigen oder später? Was würdest du in meiner Lage tun?", 5), "planen": ("Mach mir einen Plan für {t}", 3),
 "ideen": ("Gib mir Ideen für {t}", 6), "umformen": ("Übersetze ins Englische: Unser Projekt zu {t} startet nächste Woche.", 2), "kurzauskunft": ("Wann ist die Frist für {t}?", 1)}
ADD = {"ziel": " Ich brauche das, um morgen im Meeting zu entscheiden.", "format": " Bitte als Tabelle mit drei Spalten.", "adressat": " Leser sind Einsteiger, Ton locker.",
 "kontext": " Hintergrund: wir sind ein Team von drei Leuten, Budget 5.000 €.", "beispiel": " Zum Beispiel so: 'Liebe Kolleginnen, …'.",
 "arbeitsweise": " Stell mir zuerst drei Rückfragen, bevor du loslegst.", "eigenansatz": " Mein eigener Entwurf: erst Kosten senken, dann Umsatz. Prüf das."}
FOL = {"nachbessern": "Kürzer bitte und ändere die Überschrift.", "pruefen": "Woher stammt die Zahl? Nenn mir die Quelle."}

def make(out, start=(2023, 1), end=(2026, 10), n=1200, files=10, seed=1, gaps=(), meta="normal", weak_titles=0.0, growth=True, scale=None):
    rnd = random.Random(seed); os.makedirs(out, exist_ok=True); truth = {}; convs = []
    t0, t1 = dt.datetime(*start, 1).timestamp(), dt.datetime(*end, 28).timestamp()
    while len(convs) < n:
        ts = rnd.uniform(t0, t1); d = dt.datetime.fromtimestamp(ts)
        if (d.year, d.month) in gaps: continue
        w = (ts - t0) / (t1 - t0) if growth else 0.3
        top = rnd.choice(list(TOPICS)); sub = rnd.choice(TOPICS[top]); task = rnd.choice(TASKS)
        txt, bloom = TEMPL[task]; txt = txt.format(t=sub); beh = {k: 0 for k in list(ADD) + list(FOL)}
        for k in ADD:
            p = (0.05 + 0.6 * w * w) * (scale or {}).get(k, 1)
            if k == "adressat" and task not in ("schreiben", "ideen", "umformen"): p = 0
            if rnd.random() < p: beh[k] = 1; txt += ADD[k]
        bloom = max(1, min(6, bloom + rnd.choice([-2, -1, -1, 0, 0, 1, 1, 2])))
        follow = []
        for k in FOL:
            if rnd.random() < (0.15 + 0.35 * w) * (scale or {}).get(k, 1): beh[k] = 1; follow.append(FOL[k])
        if rnd.random() < 0.3: follow.append("danke")
        cid = str(uuid.uuid4()); truth[cid] = {"einsatzart": task, "denkstufe": bloom, "thema": top + " | " + sub, **beh, "n_follow": len([f for f in follow if f != 'danke'])}
        msgs = [("user", txt)]
        for f in follow: msgs += [("assistant", "Antwort zu " + sub), ("user", f)]
        msgs.append(("assistant", "Antwort zu " + sub))
        mp, prev = {}, "root"; mp["root"] = {"id": "root", "message": None, "parent": None, "children": []}
        model = "gpt-4o" if ts < 1.75e9 else "gpt-5"
        for i, (r, x) in enumerate(msgs):
            nid = str(uuid.uuid4()); md = {"model_slug": model} if r == "assistant" and meta != "no_model" else {}
            mp[nid] = {"id": nid, "parent": prev, "children": [], "message": {"id": nid, "author": {"role": r}, "create_time": ts + 30 * i,
                       "content": {"content_type": "text", "parts": [x]}, "metadata": md}}
            mp[prev]["children"].append(nid); prev = nid
        title = sub + " " + rnd.choice(["Frage", "Hilfe", "Idee", "Plan", "Vergleich"]) if rnd.random() >= weak_titles else "New chat"
        c = {"title": title, "create_time": ts, "update_time": ts + 400, "mapping": mp, "current_node": prev, "conversation_id": cid}
        if rnd.random() < 0.1:
            gid = "g-p-" + uuid.uuid4().hex[:8] if rnd.random() < .5 else "g-" + uuid.uuid4().hex[:8]
            if meta == "template_only": c["conversation_template_id"] = gid; c["gizmo_id"] = None
            elif meta == "conflict": c["conversation_template_id"] = gid; c["gizmo_id"] = "g-" + uuid.uuid4().hex[:8]
            else: c["gizmo_id"] = gid; c["conversation_template_id"] = gid
        convs.append(c)
    convs.sort(key=lambda c: c["create_time"])
    for i in range(files): json.dump(convs[i::files], open(f"{out}/conversations-{i:03d}.json", "w"), ensure_ascii=False)
    json.dump(truth, open(f"{out}/../truth.json", "w"))
    return truth
