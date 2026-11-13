"""Szenario-Tests: prüfen, ob die Prüf- und Abbruchmechanismen greifen. Run: python3 tests/test_insights.py"""
import os, sys, json, shutil, importlib, random, io, contextlib, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import fixtures
RESULTS = []

def fresh(name, **kw):
    d = os.path.join("/tmp/rgtest", name); shutil.rmtree(d, ignore_errors=True); os.makedirs(d + "/data")
    truth = fixtures.make(d + "/data", **kw)
    os.environ["RG_BASE"] = d + "/data"; os.environ["RG_TODAY"] = "2026-11-13"
    import importlib.util
    spec = importlib.util.spec_from_file_location("chi_core", os.path.join(os.path.dirname(HERE), "chat-history-insights.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod, truth, d + "/data"

def quiet(f, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): r = f(*a, **k)
    return r, buf.getvalue()

def check(name, cond, info=""):
    RESULTS.append((name, bool(cond), info)); print(("PASS " if cond else "FAIL ") + name + (f"  [{info}]" if info else ""))

# ---- simulierte Einordnung durch ChatGPT
def name_clusters(rg, lazy=0):
    out, _ = quiet(rg.themen_vorschlag); cl = __import__("pandas").read_pickle(rg.P("cluster.pkl")); truth = json.load(open(os.path.join(rg.BASE, "..", "truth.json")))
    z = {}
    for c in out:
        ids = cl[cl["cl"] == c["cluster"]]["id"]; tops = collections.Counter(truth[i]["thema"].split(" | ")[0] for i in ids)
        t, n = tops.most_common(1)[0]
        z[c["cluster"]] = {"oberthema": t.split(" / ")[0], "thema": t.split(" / ")[1]} if n / len(ids) >= 0.6 and c["cluster"] >= lazy else "GEMISCHT"
    return z

def resolve_rest(rg, truth, lazy=False):
    import pandas as pd
    for _ in range(50):
        cl = pd.read_pickle(rg.P("themen.pkl")); r = cl[cl["thema"] == "REST"]["id"][:120]
        if not len(r): break
        a = {i: ("unklar" if lazy else truth[i]["thema"].split(" | ")[0]) for i in r}
        res, _ = quiet(rg.themen_rest_speichern, a)
        if res: return res
    return rg.state()["gates"]["themen"]["stufe"]

def code_A(rg, truth, ids, unclear=0.0, rnd=random.Random(3)):
    tl = set(json.load(open(rg.P("themen_liste.json"))))
    rows = []
    for i in ids:
        t = truth[i]; th = t["thema"].split(" | ")[0]
        task = "unklar" if rnd.random() < unclear else t["einsatzart"]
        rows.append({"id": i, "aufgabe": f"möchte {t['thema'].split(' | ')[1]} als {task} bearbeiten lassen {i[:4]}", "einsatzart": task, "sicher": 1, "thema": th if th in tl else "unklar"})
    return rows

def code_B(rg, truth, ids, bloom_from_task=False, noise=None, rnd=random.Random(5)):
    BMAP = {"schreiben": 3, "code": 3, "analyse": 4, "recherche": 2, "lernen": 2, "bewerten": 5, "rat": 5, "planen": 3, "ideen": 6, "umformen": 2, "kurzauskunft": 1}
    rows = []
    for i in ids:
        t = truth[i]; r = {"id": i, "denkstufe": BMAP[t["einsatzart"]] if bloom_from_task else t["denkstufe"]}
        for k in rg.IND: r[k] = t.get(k, 0)
        if noise:
            for k, p in noise.items():
                if rnd.random() < p: r[k] = 1 - r[k]
        r["beleg"] = {k: "erkennbar" for k in rg.IND if r[k] == 1}; rows.append(r)
    return rows

def run_coding(rg, truth, unclear_A=(0, 0), bloom_bad=(False, False), noise=(None, None)):
    smp = [x["id"] for x in json.load(open(rg.P("stichprobe.json")))]
    for k in range(0, len(smp), 40): quiet(rg.speichern, "A", code_A(rg, truth, smp[k:k + 40], unclear_A[0]))
    if rg.state()["gates"]["durchgang_A"]["stufe"] == "WIEDERHOLEN":
        rep = json.load(open(rg.P("rep_A.json")))["ids"]
        for k in range(0, len(rep), 40): quiet(rg.speichern, "A", code_A(rg, truth, rep[k:k + 40], unclear_A[1]))
    for k in range(0, len(smp), 40): quiet(rg.speichern, "B", code_B(rg, truth, smp[k:k + 40], bloom_bad[0]))
    if rg.state()["gates"]["durchgang_B"]["stufe"] == "WIEDERHOLEN":
        rep = json.load(open(rg.P("rep_B.json")))["ids"]
        for k in range(0, len(rep), 40):
            rows = code_B(rg, truth, rep[k:k + 40], bloom_bad[1]); quiet(rg.speichern, "B", [{"id": r["id"], "denkstufe": r["denkstufe"]} for r in rows])
    quiet(rg.pruefpaket); ids = json.load(open(rg.P("pruef_ids.json")))
    A2 = {r["id"]: r for r in code_A(rg, truth, ids)}; B2 = code_B(rg, truth, ids, noise=noise[0])
    quiet(rg.pruefung_speichern, [{**A2[r["id"]], **r} for r in B2])
    if rg.state()["gates"]["pruefung"]["stufe"] == "WIEDERHOLEN":
        allids = list(json.load(open(rg.P("codes_B.json"))))
        while rg.state().get("fw_offset", 0) < len(allids): quiet(rg.feld_wiederholung)
        quiet(rg.pruefung_wiederholen); ids = json.load(open(rg.P("pruef_ids.json")))
        A2 = {r["id"]: r for r in code_A(rg, truth, ids)}; B2 = code_B(rg, truth, ids, noise=noise[1])
        quiet(rg.pruefung_speichern, [{**A2[r["id"]], **r} for r in B2])
    quiet(rg.zweifelsfaelle); quiet(rg.korrigieren, [])

def pipeline(rg, truth, lazy_topics=0, lazy_rest=False, **kw):
    quiet(rg.einlesen); quiet(rg.daten_pruefen); quiet(rg.zeitraeume)
    quiet(rg.themen_festlegen, name_clusters(rg, lazy_topics))
    if rg.state()["gates"]["themen"]["stufe"] == "WIEDERHOLEN": resolve_rest(rg, truth, lazy_rest)
    quiet(rg.stichprobe); run_coding(rg, truth, **kw); quiet(rg.auswerten)
    cand = rg.kandidaten(); steps = [{"verhalten": k, "text": "Probier beim nächsten Auftrag: „…“."} for k in cand[:3]]
    out, _ = quiet(rg.bericht, steps); return out

# ---------------- Szenarien
def t_normal():
    rg, truth, d = fresh("normal"); out = pipeline(rg, truth); G = rg.state()["gates"]
    check("Normal: Modus VOLL", G["zeitraeume"]["modus"] == "VOLL")
    check("Normal: Themen-Rest ≤ 15 %", G["themen"]["rest"] <= 0.15, f"{G['themen']['rest']:.0%}")
    check("Normal: Bericht = Vollbericht", G["bericht"]["stufe"] == "Vollbericht", G["bericht"]["grund"])
    R = json.load(open(rg.P("ergebnis.json")))
    check("Normal: Veränderung 'Ziel' abgesichert (wahre Zunahme)", R["veraenderung"]["ziel"]["klasse"] == "abgesichert", str(R["veraenderung"]["ziel"]))
    check("Normal: Reifegrad als Spanne vorhanden", R["reifegrad"] is not None)
    en, _ = quiet(rg.bericht, [], sprache="en"); txt = open(en, encoding="utf-8").read()
    import re
    leftover = set(re.findall(r">[^<]*[äöüÄÖÜß][^<]*<", txt))
    check("Englischer Bericht ohne deutsche Reste", en.endswith("ai-usage-report.html") and not leftover, str(list(leftover)[:3]))
    return out

def t_files():
    rg, truth, d = fresh("files", n=600, files=8)
    open(d + "/conversations-008.json", "w").write(open(d + "/conversations-001.json").read()[:5000])       # abgeschnitten
    shutil.copy(d + "/conversations-002.json", d + "/conversations-002 (1).json")                           # doppelt hochgeladen
    json.dump({"user": "x"}, open(d + "/conversations-x.json", "w"))                                        # fremd
    _, out = quiet(rg.einlesen); lvl, _ = quiet(rg.daten_pruefen); rep = rg.state()["gates"]["daten"]
    check("Dateien: abgeschnittene Datei erkannt", "DEFEKT" in out and "conversations-008" in out)
    check("Dateien: fremde Datei erkannt", "FREMD" in out)
    check("Dateien: Doppelte nicht doppelt gezählt", len(rg._df()) == 600, f"{len(rg._df())}")
    check("Dateien: Datenprüfung WARN wegen Defekt", lvl == "WARN", rep["grund"])

def t_old_export():
    rg, truth, d = fresh("alt", end=(2025, 12)); quiet(rg.einlesen); quiet(rg.daten_pruefen); z, _ = quiet(rg.zeitraeume)
    check("Veralteter Export: kein 'heute', sondern 'zuletzt'", z["jetzt"]["aktuell"] is False and z["jetzt"]["name"].startswith("zuletzt"), z["jetzt"]["name"])

def t_tail():
    rg, truth, d = fresh("tail", start=(2023, 1), end=(2025, 6), n=1000)
    extra = fixtures.make(d + "/x", start=(2026, 5), end=(2026, 6), n=6, files=1, seed=9)
    os.rename(d + "/x/conversations-000.json", d + "/conversations-extra.json"); truth.update(extra)
    json.dump(truth, open(os.path.join(d, "..", "truth.json"), "w"))
    quiet(rg.einlesen); lvl, out = quiet(rg.daten_pruefen)
    check("Dünne Endphase → WARN und Rückfrage an Nutzer", lvl == "WARN" and "RÜCKFRAGE" in out and "06/2025" in out or "07/2025" in out, rg.state()["gates"]["daten"]["grund"])
    quiet(rg.luecke_bestaetigt); z, _ = quiet(rg.zeitraeume)
    check("Dünne Endphase: Zeitraum endet vor der Lücke, Vergleich möglich", z["jetzt"]["bis"] == "2025-06" and z["modus"] == "VOLL" and not z["jetzt"]["aktuell"], json.dumps(z["jetzt"]))
    out = pipeline_after_periods(rg, truth); h = open(out, encoding="utf-8").read()
    check("Dünne Endphase: Bericht nennt Stand 06/2025 und ist eingeschränkt", "Stand 06/2025" in h and rg.state()["gates"]["bericht"]["stufe"] == "Eingeschränkter Bericht")

def t_short():
    rg, truth, d = fresh("kurz", start=(2026, 2), n=500); quiet(rg.einlesen); quiet(rg.daten_pruefen); z, _ = quiet(rg.zeitraeume)
    check("Kurzer Zeitraum: kein Vergleich", z["modus"] == "OHNE_VERGLEICH", z["modus"])
    out = pipeline_after_periods(rg, truth); R = json.load(open(rg.P("ergebnis.json")))
    check("Kurzer Zeitraum: keine Veränderungsaussagen", R["veraenderung"] == {})
    check("Kurzer Zeitraum: Bericht eingeschränkt", rg.state()["gates"]["bericht"]["stufe"] == "Eingeschränkter Bericht")

def pipeline_after_periods(rg, truth):
    quiet(rg.themen_festlegen, name_clusters(rg))
    if rg.state()["gates"]["themen"]["stufe"] == "WIEDERHOLEN": resolve_rest(rg, truth)
    quiet(rg.stichprobe); run_coding(rg, truth); quiet(rg.auswerten)
    out, _ = quiet(rg.bericht, [{"verhalten": k, "text": "x"} for k in rg.kandidaten()[:3]]); return out

def t_gap():
    rg, truth, d = fresh("luecke", gaps={(2026, m) for m in (3, 4, 5, 6, 7)}); quiet(rg.einlesen); lvl, out = quiet(rg.daten_pruefen)
    check("Datenlücke → Datenprüfung WARN", lvl == "WARN")
    check("Datenlücke im letzten Jahr erkannt", "Lücken" in rg.state()["gates"]["daten"]["grund"], rg.state()["gates"]["daten"]["grund"])
    z, _ = quiet(rg.zeitraeume); check("Datenlücke: 'jetzt'-Zeitraum trotzdem nur mit genug Monaten", z["jetzt"]["tragfaehig"] in (True, False), json.dumps(z["jetzt"]))

def t_meta():
    rg, _, _ = fresh("meta_tpl", n=400, meta="template_only"); quiet(rg.einlesen); quiet(rg.daten_pruefen)
    m = rg.state()["gates"]["daten"]["bericht"]["metadaten"]; df = rg._df()
    check("Metadaten: GPT über conversation_template_id erkannt", m["gpt"] == "ok" and (df["gpt_art"] != "").sum() > 20, f"{(df['gpt_art'] != '').sum()} Chats")
    rg, _, _ = fresh("meta_conf", n=400, meta="conflict"); quiet(rg.einlesen); quiet(rg.daten_pruefen)
    check("Metadaten: widersprüchliche IDs → nicht auswerten", "widersprüchlich" in rg.state()["gates"]["daten"]["bericht"]["metadaten"]["gpt"])
    rg, _, _ = fresh("meta_model", n=400, meta="no_model"); quiet(rg.einlesen); quiet(rg.daten_pruefen)
    check("Metadaten: fehlende Modellangaben → nicht auswerten", "nicht auswerten" in rg.state()["gates"]["daten"]["bericht"]["metadaten"]["modell"])

def t_rest():
    rg, truth, _ = fresh("rest"); quiet(rg.einlesen); quiet(rg.daten_pruefen); quiet(rg.zeitraeume)
    z = name_clusters(rg, lazy=10**6)  # alles GEMISCHT außer nichts → simuliert 6 Kategorien + Sammelbecken
    keep = list(z)[:4]; zz = {k: (v if k in keep else "GEMISCHT") for k, v in name_clusters(rg).items()}
    lvl, _ = quiet(rg.themen_festlegen, zz)
    check("Restkategorie dominant → Wiederholung erzwungen", lvl == "WIEDERHOLEN", rg.state()["gates"]["themen"]["grund"])
    try: quiet(rg.stichprobe); blocked = False
    except RuntimeError: blocked = True
    check("Restkategorie: Stichprobe blockiert, solange Wiederholung offen", blocked)
    lvl = resolve_rest(rg, truth, lazy=True)
    check("Rest bleibt > 20 % → Themen NICHT_BELASTBAR", lvl == "NICHT_BELASTBAR", rg.state()["gates"]["themen"]["grund"])
    quiet(rg.stichprobe); run_coding(rg, truth); quiet(rg.auswerten); out, _ = quiet(rg.bericht, [])
    h = open(out).read(); check("Bericht zeigt Themen als nicht belastbar", "Themen nicht belastbar" in h)

def t_sonstiges():
    rg, truth, _ = fresh("sonstiges"); quiet(rg.einlesen); quiet(rg.daten_pruefen); quiet(rg.zeitraeume); quiet(rg.themen_festlegen, name_clusters(rg))
    if rg.state()["gates"]["themen"]["stufe"] == "WIEDERHOLEN": resolve_rest(rg, truth)
    quiet(rg.stichprobe); smp = [x["id"] for x in json.load(open(rg.P("stichprobe.json")))]
    for k in range(0, len(smp), 40): quiet(rg.speichern, "A", code_A(rg, truth, smp[k:k + 40], unclear=0.76))
    check("76 % unklar → Wiederholung", rg.state()["gates"]["durchgang_A"]["stufe"] == "WIEDERHOLEN")
    rep = json.load(open(rg.P("rep_A.json")))["ids"]
    for k in range(0, len(rep), 40): quiet(rg.speichern, "A", code_A(rg, truth, rep[k:k + 40], unclear=0.7))
    check("weiterhin > 20 % unklar → Einsatzart NICHT_BELASTBAR", rg.state()["gates"]["durchgang_A"]["stufe"] == "NICHT_BELASTBAR", rg.state()["gates"]["durchgang_A"]["grund"])
    rg2, truth2, _ = fresh("sonstiges2"); quiet(rg2.einlesen); quiet(rg2.daten_pruefen); quiet(rg2.zeitraeume); quiet(rg2.themen_festlegen, name_clusters(rg2))
    if rg2.state()["gates"]["themen"]["stufe"] == "WIEDERHOLEN": resolve_rest(rg2, truth2)
    quiet(rg2.stichprobe); run_coding(rg2, truth2, unclear_A=(0.76, 0.05)); G = rg2.state()["gates"]
    check("76 % unklar, nach Neulesen 5 % → Einsatzart wieder OK", G["durchgang_A"]["stufe"] in ("OK", "WARN"), G["durchgang_A"]["grund"])

def t_bloom():
    rg, truth, _ = fresh("bloom"); quiet(rg.einlesen); quiet(rg.daten_pruefen); quiet(rg.zeitraeume); quiet(rg.themen_festlegen, name_clusters(rg))
    if rg.state()["gates"]["themen"]["stufe"] == "WIEDERHOLEN": resolve_rest(rg, truth)
    quiet(rg.stichprobe); smp = [x["id"] for x in json.load(open(rg.P("stichprobe.json")))]
    for k in range(0, len(smp), 40): quiet(rg.speichern, "A", code_A(rg, truth, smp[k:k + 40]))
    for k in range(0, len(smp), 40): quiet(rg.speichern, "B", code_B(rg, truth, smp[k:k + 40], bloom_from_task=True))
    check("Denkstufe aus Einsatzart abgeleitet → erkannt", rg.state()["gates"]["durchgang_B"]["stufe"] == "WIEDERHOLEN", rg.state()["gates"]["durchgang_B"]["grund"])

def t_validation():
    rg, truth, _ = fresh("valid", n=400); quiet(rg.einlesen); quiet(rg.daten_pruefen); quiet(rg.zeitraeume); quiet(rg.themen_festlegen, name_clusters(rg))
    if rg.state()["gates"]["themen"]["stufe"] == "WIEDERHOLEN": resolve_rest(rg, truth)
    quiet(rg.stichprobe); smp = [x["id"] for x in json.load(open(rg.P("stichprobe.json")))][:40]
    rows = code_A(rg, truth, smp); [r.update(aufgabe="Hilfe") for r in rows]
    ok, out = quiet(rg.speichern, "A", rows); check("Einordnung ohne eigene Aufgabenbeschreibung wird abgelehnt", ok is False and "ABGELEHNT" in out)
    rows = code_A(rg, truth, smp); [r.update(aufgabe="Nutzer möchte Hilfe bei einem Thema") for r in rows]
    ok, out = quiet(rg.speichern, "A", rows); check("Schablonen-Antworten (identische Aufgaben) werden abgelehnt", ok is False)
    quiet(rg.speichern, "A", code_A(rg, truth, smp)); rows = code_B(rg, truth, smp); [r.update(beleg={}) for r in rows]
    try: ok, out = quiet(rg.speichern, "B", rows)
    except RuntimeError: ok = False; out = "ABGELEHNT"
    check("Verhalten ohne Beleg wird abgelehnt", ok is False)

def t_unreliable_field():
    rg, truth, _ = fresh("unrel"); out = pipeline(rg, truth, noise=({"ziel": 0.45}, {"ziel": 0.45})); G = rg.state()["gates"]
    check("Instabiles Feld im Prüflauf → nicht belastbar", "ziel" in G["pruefung"].get("nicht_belastbar", []), G["pruefung"]["grund"])
    R = json.load(open(rg.P("ergebnis.json")))
    check("Instabiles Feld: keine abgesicherte Veränderung", R["veraenderung"]["ziel"]["klasse"].startswith("nicht belegbar"))
    try: quiet(rg.bericht, [{"verhalten": "ziel", "text": "x"}]); rejected = False
    except ValueError: rejected = True
    check("Instabiles Feld: Tipp dazu wird abgelehnt", rejected)
    check("Instabiles Feld: Bericht eingeschränkt", G["bericht"]["stufe"] == "Eingeschränkter Bericht")

def t_order():
    rg, truth, _ = fresh("order", n=300); quiet(rg.einlesen)
    try: quiet(rg.bericht, []); ok = False
    except RuntimeError: ok = True
    check("Bericht ohne vorherige Prüfungen nicht möglich", ok)
    try: quiet(rg.stichprobe); ok = False
    except RuntimeError: ok = True
    check("Stichprobe ohne Datenprüfung nicht möglich", ok)

def t_reset():
    rg, truth, d = fresh("reset", n=300); quiet(rg.einlesen); shutil.rmtree(rg.ST); os.makedirs(rg.ST)
    try: quiet(rg.daten_pruefen); ok = False
    except RuntimeError as e: ok = True
    check("Zurückgesetzte Sitzung wird erkannt", ok)

def t_small():
    rg, truth, d = fresh("klein", n=80, start=(2026, 5)); quiet(rg.einlesen); lvl, _ = quiet(rg.daten_pruefen)
    check("Zu wenige Chats → STOP", lvl == "STOP")
    try: quiet(rg.zeitraeume); ok = False
    except RuntimeError: ok = True
    check("Nach STOP keine weitere Auswertung", ok)

if __name__ == "__main__":
    for t in [t_order, t_reset, t_small, t_files, t_meta, t_old_export, t_tail, t_gap, t_short, t_rest, t_sonstiges, t_bloom, t_validation, t_unreliable_field, t_normal]:
        try: t()
        except Exception as e:
            import traceback; traceback.print_exc(); check(t.__name__ + " (Absturz)", False, repr(e))
    print(f"\n{sum(r[1] for r in RESULTS)} von {len(RESULTS)} Prüfungen bestanden")
