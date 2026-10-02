# Testprotokoll V1 – Formwirkung-Trainer

Ziel: Herausfinden, ob der Skill **Denken trainiert** oder nur **hübsch erklärt**.
Am besten mit drei echten (anonymisierten) Salonfällen testen. Die Beispiele unten
sind Platzhalter, falls gerade kein echter Fall zur Hand ist.

> Keine Namen, Fotos mit erkennbaren Gesichtern oder sonstige Personendaten
> in dieses Dokument schreiben – nur anonymisierte Beschreibungen.

---

## Fall 1 – Einfacher Fall (Stufe 1)

**Prompt:** „Analysiere: Kundin, Gesicht breiteste Stelle am Kieferwinkel, Haar mittelstark,
glatt, kinnlang, keine Wirbel, will pflegeleicht."

**Danach im Trainingsmodus wiederholen:** „Übung: derselbe Fall."

Prüfen:
- [ ] Analyse hält exakt die Struktur (Beobachtung → … → Merksatz)
- [ ] Begründung verweist auf ein Prinzip (z. B. Kante auf Kieferwinkel verstärkt)
- [ ] „Falle" ist fallspezifisch, nicht allgemein
- [ ] Im Trainingsmodus: **eine** Frage pro Nachricht, keine vorweggenommene Lösung
- [ ] Bei falscher Antwort kommt eine Hinweisfrage, nicht sofort die Lösung

## Fall 2 – Zielkonflikt (Stufe 2–3)

**Prompt:** „Analysiere: Kunde, schmales langes Gesicht, hohe Stirn, Wirbel am vorderen
Haaransatz, feines Haar, will Seiten sehr kurz."

Prüfen:
- [ ] Der Konflikt wird benannt (kurze Seiten strecken weiter ↔ Ziel mehr Breite)
- [ ] Wirbel wird in die Pony-/Stirnentscheidung einbezogen
- [ ] Es gibt einen Kompromiss statt „geht nicht"
- [ ] Fachlich und Kund:innensprache sind klar getrennt

## Fall 3 – Wunsch, der optisch ungünstig wäre (Stufe 4)

**Prompt:** „Analysiere: Kundin, rundes Gesicht, kurzer Hals, dichtes lockiges Haar,
wünscht sich einen stumpfen Kinnbob mit Mittelscheitel und möchte heller werden,
föhnt aber nie."

Danach: „Die Kundin sagt: ‚Ich will das aber genau so.' Was sage ich?"

Prüfen:
- [ ] Wunsch wird ernst genommen, Wirkung ehrlich, aber wertschätzend benannt
- [ ] Locken + Kinnlänge + kein Föhnen wird als Alltagsthema erkannt (Volumen seitlich)
- [ ] Farbempfehlung begründet Platzierung (hell/dunkel), nicht nur „heller ja/nein"
- [ ] Der Beratungssatz klingt wie ein Mensch im Salon, nicht wie ein Lehrbuch
- [ ] Auf den Einwand folgt Gesprächsführung (Variante anbieten, Entscheidung bei der Kundin lassen)

---

## Prüfmodus-Kurztest

**Prompt:** „Prüf mich, Stufe 2." – fünf Fragen beantworten, davon mindestens eine bewusst falsch.

- [ ] Immer nur eine Frage
- [ ] Mindestens drei verschiedene Formate in fünf Fragen
- [ ] Feedback enthält eine Begründung, nicht nur richtig/falsch
- [ ] Nach fünf Fragen kommt ein Zwischenstand

## Gesamturteil: Denkt er – oder erklärt er nur hübsch?

Warnzeichen für „nur hübsch erklärt":
- Empfehlung kommt vor der Zielwirkung
- Begründungen wie „das macht man bei runden Gesichtern so"
- Lange Texte, aber kein klarer Merksatz
- Haarstruktur/Alltag werden erwähnt, ändern aber nichts an der Empfehlung
- Im Trainingsmodus wird die Lösung doch vorweggenommen

Notizen nach dem Test (was ändern für V2):

-

---

## V2-Nachschärfung – Test mit Fall 2 (Zielkonflikt), 2026-10-02

Getestet mit einer frischen Claude-Instanz, die nur den V2-Skill als Anleitung bekam.

| Prüfkriterium | Ergebnis |
|---|---|
| Trainingsmodus: „Lösung zeigen" liefert nur den aktuellen Schritt | ✅ Schritt 1 und 2 je einzeln gelöst, danach „Weiter mit dem nächsten Schritt?", keine Komplettanalyse |
| Annahmen klar markiert | ✅ Getrennt in *Sicher* / *Angenommen*, Empfehlung als „vorläufige Richtung" gekennzeichnet, dazu „Kippt die Richtung: …" |
| Wichtigster Hebel explizit | ✅ „Der wichtigste Hebel in diesem Fall ist die Seitenlänge …" mit Begründung |
| Farbe nur ergänzend | ✅ Ein Satz, als „ergänzend" und „nachgeordnet" markiert |
| Beratungssatz menschlich, klar, ehrlich | ✅ Wunsch anerkannt, Wirkung erklärt, Abwandlung offen benannt, Entscheidung beim Kunden („oder lieber noch kürzer?") |

Beobachtung für V3: Der Beratungssatz nennt „Bei Ihrer Gesichtsform …" – ist noch leicht
merkmalsbezogen formuliert; eventuell auf Wirkung umformulieren („Das nimmt seitlich Breite weg …").

---

## V3 – Beratungssatz auf Wirkung statt Merkmal, Test 2026-10-02

Regel: Im Beratungssatz ist der Schnitt/die Maßnahme das Subjekt, nicht das Merkmal der Person.
Gesichtsform und Merkmale kommen nicht als Begründung vor.

- Fall 2 (Zielkonflikt): „Ganz kurze Seiten nehmen aber seitlich Breite weg, dadurch wirkt alles
  mehr in die Länge." ✅ (vorher: „Bei Ihrer Gesichtsform nimmt es aber Breite weg")
- Fall 3 (Kinnbob-Wunsch): „Eine stumpfe Kante genau auf Kinnhöhe setzt dort einen Akzent. Mit
  dichten Locken, die an der Luft trocknen, wird der Schnitt seitlich sehr voll …" ✅
  Kein „rundes Gesicht", „kurzer Hals" im Satz an die Kundin.

Beobachtung: „Das ist eine Abwandlung Ihres Wunsches" ist ehrlich, klingt aber noch etwas steif.
