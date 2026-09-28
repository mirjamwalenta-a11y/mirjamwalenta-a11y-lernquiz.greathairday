# 2D-Tool „Formwirkung“ – Pilotfall: Lange Nase im Profil

**Status:** Konzept / Struktur (noch keine Umsetzung)
**Zielgruppe:** Lehrlinge
**Zweck des Tools:** Sichtbar machen, was eine Schnittform optisch im Gesicht bewirkt.

Dieser Pilotfall legt die Grundstruktur fest, die später für weitere Fälle
(z. B. rundes Gesicht, hohe Stirn, kurzer Hals) wiederverwendet wird.

---

## 0. Lernziel des Pilotfalls

Der Lehrling versteht:

> Die Nase wirkt im Profil nicht für sich allein, sondern im Verhältnis zur
> ganzen Kopfform. Bekommt der Hinterkopf mehr Aufbau, entsteht ein
> Gegengewicht – die Nase wirkt dadurch weniger dominant.

Wichtig für die ganze Darstellung: **Die Nase bleibt in jeder Ansicht gleich.**
Nur die Haarform verändert sich. Genau das soll der Lehrling sehen.

---

## 1. Screen-Aufbau

Jeder Fall folgt denselben fünf Kernschritten. So lernt der Lehrling ein
festes Denkschema, das bei jedem neuen Fall gleich bleibt.

| Nr. | Screen | Frage, die der Screen beantwortet | Lernmodus | Schnell-Modus |
|-----|--------|-----------------------------------|:---------:|:-------------:|
| 0 | Einstieg | Worum geht es? | ✔ | – |
| 1 | Ausgangsform | Was sehe ich? | ✔ | ✔ (kurz) |
| 2 | Zielwirkung | Wie soll es wirken? | ✔ | ✔ (kurz) |
| 3 | Schnittentscheidung | Was schneide ich? | ✔ | ✔ (kurz) |
| 4 | Warum es wirkt | Warum funktioniert das? | ✔ | ✔ (1 Satz) |
| 5 | Darauf achten | Was kann schiefgehen? | ✔ | ✔ (Stichpunkte) |
| 6 | Verständnis-Check | Habe ich es verstanden? | ✔ | – |
| 7 | Merksatz | Was nehme ich mit? | ✔ | ✔ |

### Grundlayout eines Screens (gleich für alle Schritte)

```
┌────────────────────────────────────────────┐
│  Schritt 2 von 7 · Zielwirkung       [ⓘ]   │  ← Fortschritt + Titel
├────────────────────────────────────────────┤
│                                            │
│          [ 2D-Profil-Silhouette ]          │  ← Bildbereich (ca. 60 %)
│                                            │
├────────────────────────────────────────────┤
│  [Hilfslinien] [Gewicht] [Blickpunkt]      │  ← Einblende-Schalter
├────────────────────────────────────────────┤
│  Kurzer Erklärtext (2–4 Sätze)             │  ← Textbereich
├────────────────────────────────────────────┤
│  ← Zurück                      Weiter →    │
└────────────────────────────────────────────┘
```

- Bild oben, Text unten – immer in dieser Reihenfolge.
- Pro Screen nur **eine** neue Idee.
- Am Handy: Bild bleibt oben sichtbar, Text scrollt darunter.

---

## 2. Visuelle Elemente

### Grundfigur

- **Kopf im Profil**, Blick nach rechts, als ruhige 2D-Silhouette
  (Grautöne, keine realistischen Gesichtszüge, kein Make-up, keine Mimik).
- Hals und Schulteransatz angedeutet, damit die Kopfhaltung klar ist.
- **Nase:** deutlich, aber nicht karikiert – eine realistische „lange Nase“.
- **Haar:** als eigene Fläche in einem zweiten Ton, klar vom Kopf abgegrenzt.
  Darunter die Schädelform ganz dezent sichtbar (gestrichelte Linie).

### Zwei Haarformen für den Vergleich

| Form | Beschreibung | Wirkung |
|------|--------------|---------|
| **A – Ausgangsform** | Hinterkopf flach, Haar liegt eng an oder fällt glatt nach unten | Gewicht vorne, Nase wirkt dominant |
| **B – Zielform** | Hinterkopf mit Aufbau (Graduation), Nacken schmal, Vorderpartie weich | Vorne und hinten im Gleichgewicht |

### Farben

- Kopf / Gesicht: helles Grau
- Haar: mittleres Grau
- **Eine** Akzentfarbe für Hilfslinien und Hinweise (z. B. ein ruhiges Blau)
- Warnhinweise (Fehlerbilder): gedämpftes Rot, sparsam

Keine weiteren Farben. Die Aufmerksamkeit soll auf der Form liegen.

---

## 3. Einblendungen und Schaltflächen

Alle Einblendungen sind **Schalter** (an/aus), damit der Lehrling selbst
vergleichen kann. Standard: alle aus, nur die Silhouette ist sichtbar.

| Schalter | Was erscheint | Wozu |
|----------|---------------|------|
| **Hilfslinien** | Senkrechte Linie durch das Ohr. Teilt den Kopf in „vorne“ und „hinten“. | Zeigt, dass es zwei Seiten gibt, die sich ausgleichen müssen. |
| **Gewicht** | Zwei Flächen links und rechts der Ohrlinie, farbig hinterlegt, mit einfacher Waage-Anzeige darunter. | Macht sichtbar, wo mehr „Masse“ ist. |
| **Blickpunkt** | Ein Punkt/Kreis, wohin das Auge zuerst schaut. | Zeigt: Bei Form A springt der Blick zur Nase, bei Form B wird er verteilt. |
| **Schnittzonen** | Farbige Zonen am Haar: Nacken, Hinterkopf, Oberkopf, Vorderpartie. | Verbindet die Wirkung mit der konkreten Schnittentscheidung. |
| **Schädelform** | Gestrichelte Kontur des Kopfes unter dem Haar. | Zeigt, dass der Aufbau durch das Haar entsteht, nicht durch den Kopf. |

### Vergleichs-Regler

- **Schieberegler „Vorher ↔ Nachher“** zwischen Form A und Form B.
  Beim Schieben wächst der Hinterkopf-Aufbau schrittweise.
  Die Nase bleibt dabei sichtbar unverändert.
- Kleine feste Beschriftung neben der Nase: **„Nase unverändert“**.

### Weitere Schaltflächen

- **[ⓘ]** – öffnet eine kurze Begriffserklärung (z. B. „Graduation“,
  „Hinterhauptbein“).
- **„Fehler zeigen“** (nur Screen 5) – blendet nacheinander typische
  Fehlformen ein.

---

## 4. Inhalte der Screens mit Erklärtexten

> Die Texte sind so geschrieben, dass sie direkt übernommen werden können.
> **[L]** = Lernmodus, **[S]** = Kurzfassung für den Schnell-nachschauen-Modus.

### Screen 0 – Einstieg

**Bild:** Form A, ohne Einblendungen.

**[L]**
Manche Kundinnen und Kunden haben eine lange oder markante Nase.
Die Nase können wir nicht verändern. Aber wir können verändern,
wie sie im Verhältnis zum ganzen Kopf wirkt.
In diesem Beispiel siehst du, wie das im Profil funktioniert.

---

### Screen 1 – Ausgangsform

**Bild:** Form A. Schalter „Hilfslinien“ und „Gewicht“ werden angeboten.

**[L]**
Schau dir das Profil an. Der Hinterkopf ist flach, das Haar liegt eng an.
Vor der Ohrlinie ist viel los: Stirn, Nase, Kinn.
Hinter der Ohrlinie ist wenig Form.
Das Gewicht liegt vorne – deshalb fällt die Nase besonders auf.

**[S]**
Hinterkopf flach → Gewicht vorne → Nase wirkt dominant.

---

### Screen 2 – Zielwirkung

**Bild:** Vorher-/Nachher-Regler von Form A zu Form B.

**[L]**
Ziel ist ein Gleichgewicht zwischen vorne und hinten.
Wenn der Hinterkopf mehr Rundung bekommt, entsteht ein Gegengewicht zur Nase.
Die Nase bleibt genau gleich. Sie wirkt aber nicht mehr so stark,
weil der Kopf als Ganzes ausgeglichener aussieht.

**[S]**
Ziel: Vorne und hinten im Gleichgewicht. Die Nase bleibt gleich,
wirkt aber weniger dominant.

---

### Screen 3 – Mögliche Schnittentscheidung

**Bild:** Form B mit Schalter „Schnittzonen“.

**[L]**
Eine mögliche Lösung:

- **Hinterkopf:** mit Graduation Aufbau schaffen. Die meiste Fülle sitzt
  ungefähr am Hinterhauptbein – etwa auf der Höhe, auf der vorne die Nase ist.
- **Nacken:** schmal und nah am Kopf. So wirkt der Aufbau darüber deutlicher.
- **Oberkopf:** leicht mitführen, damit die Form rund bleibt.
- **Vorderpartie:** weich, nicht spitz nach vorne. Ein weicher,
  seitlich fallender Pony oder Längen, die das Gesicht locker umrahmen.

Das ist eine Möglichkeit, nicht die einzige. Entscheidend ist die Wirkung:
hinten Aufbau, vorne Ruhe.

**[S]**
Hinterkopf graduiert aufbauen (Höhe Hinterhauptbein), Nacken schmal,
Vorderpartie weich und nicht spitz nach vorne.

---

### Screen 4 – Warum diese Entscheidung wirkt

**Bild:** Form A und B nebeneinander, Schalter „Blickpunkt“ und „Gewicht“.

**[L]**
Unser Auge vergleicht immer. Es schaut nicht nur auf die Nase,
sondern auf den ganzen Umriss des Kopfes.
Ist hinten wenig Form, bleibt der Blick vorne an der Nase hängen.
Ist hinten ein Gegengewicht, verteilt sich der Blick über den ganzen Kopf.
Die Nase ist dann ein Teil des Gesamtbildes – nicht mehr der Mittelpunkt.

**[S]**
Das Auge vergleicht vorne und hinten. Gegengewicht hinten verteilt den Blick.

---

### Screen 5 – Worauf man achten muss

**Bild:** Schaltfläche „Fehler zeigen“ blendet nacheinander Fehlformen ein.

**[L]**
Aufbau am Hinterkopf hilft nur, wenn er an der richtigen Stelle sitzt.
Achte auf diese Punkte:

| Fehlerbild | Was passiert |
|------------|--------------|
| Aufbau **zu tief** (im Nacken) | Die Form wirkt schwer und hängend. Kein Gegengewicht zur Nase. |
| Aufbau **zu hoch** (nur am Scheitel) | Der Kopf wirkt nach oben verlängert. Die Nase bleibt im Profil dominant. |
| **Spitzer Pony** oder Haar, das nach vorne zeigt | Eine zweite Spitze vorne. Der Blick wird zusätzlich zur Nase gelenkt. |
| Haar **streng nach hinten** und flach | Das Profil liegt ganz frei. Die Nase wirkt noch stärker. |
| **Sehr kurzer, flacher Hinterkopf** (z. B. hoher Undercut) | Hinten fehlt jedes Gegengewicht. |

Außerdem vor dem Schneiden prüfen:

- **Haarstruktur und Haarmenge:** Hält feines Haar den Aufbau?
- **Wirbel am Hinterkopf:** Wo fällt das Haar von selbst hin?
- **Styling zu Hause:** Kann die Kundin oder der Kunde die Form selbst
  nachstylen?
- **Alle Ansichten:** Die Form muss auch von vorne und von hinten stimmig sein.
- **Wunsch der Kundin oder des Kunden:** Nicht jede Person möchte ihre Nase
  „ausgleichen“. Frag nach, bevor du beratend darauf eingehst – und sprich
  respektvoll über das Gesicht.

**[S]**
- Aufbau auf Höhe Hinterhauptbein – nicht im Nacken, nicht nur oben.
- Vorne nichts Spitzes, das nach vorne zeigt.
- Nicht streng und flach zurück.
- Haarstruktur, Wirbel und Styling zu Hause prüfen.
- Wunsch der Kundin/des Kunden klären.

---

## 5. Verständnis-Check

Vier bis fünf kurze Fragen. Nach jeder Antwort erscheint eine kurze
Rückmeldung (richtig/falsch + ein Satz Begründung).

**Frage 1 – Einfachauswahl**
Was passiert, wenn der Hinterkopf mehr Aufbau bekommt?
- a) Die Nase wird kürzer.
- b) **Das Verhältnis zwischen vorne und hinten ändert sich. Die Nase wirkt weniger dominant.** ✔
- c) Es verändert sich nichts, man sieht nur den Hinterkopf besser.

*Rückmeldung:* Die Nase bleibt gleich. Es verändert sich das Verhältnis.

**Frage 2 – Bildauswahl**
Bei welchem Profil wirkt die Nase stärker? *(Form A und Form B nebeneinander)*
- **Profil mit flachem Hinterkopf** ✔
- Profil mit Aufbau am Hinterkopf

*Rückmeldung:* Ohne Gegengewicht hinten bleibt der Blick an der Nase hängen.

**Frage 3 – Einfachauswahl**
Wo sollte der Aufbau am Hinterkopf ungefähr sitzen?
- a) Ganz unten im Nacken
- b) **Etwa am Hinterhauptbein, ungefähr auf Höhe der Nase** ✔
- c) Nur ganz oben am Scheitel

*Rückmeldung:* Zu tief wirkt schwer, zu hoch verlängert den Kopf.
Das Gegengewicht sollte etwa gegenüber der Nase liegen.

**Frage 4 – Richtig oder falsch**
„Ein spitzer, nach vorne gerichteter Pony hilft, die Nase auszugleichen.“
- Richtig
- **Falsch** ✔

*Rückmeldung:* Eine Spitze vorne lenkt den Blick zusätzlich nach vorne.
Besser ist eine weiche Vorderpartie.

**Frage 5 – Situation**
Eine Kundin mit sehr feinem Haar wünscht sich die Form mit Aufbau am
Hinterkopf. Was klärst du zuerst?
- a) Nichts – die Form passt immer.
- b) **Ob das Haar den Aufbau hält und ob sie die Form zu Hause stylen kann.** ✔
- c) Ob sie einen Pony möchte.

*Rückmeldung:* Die beste Form hilft nur, wenn sie im Alltag hält.

---

## 6. Merksatz

> **Die Nase bleibt gleich – das Verhältnis ändert sich.
> Hinten Aufbau, vorne Ruhe.**

---

## 7. Übertragung in die zwei Modi

### Lernmodus

- Alle Screens 0–7 nacheinander.
- Schalter werden Schritt für Schritt eingeführt (erst Hilfslinien,
  dann Gewicht, dann Blickpunkt, dann Schnittzonen).
- Verständnis-Check am Ende, Merksatz als Abschluss.

### Schnell-nachschauen-Modus

Eine einzige Seite, z. B. für den Einsatz direkt vor der Beratung:

```
┌──────────────────────────────────────────┐
│  Lange Nase im Profil                    │
│  [ Vorher ↔ Nachher-Regler ]             │
│                                          │
│  Ausgangsform: Hinterkopf flach →        │
│                Nase wirkt dominant       │
│  Ziel:         Gleichgewicht vorne/hinten│
│  Schnitt:      Hinterkopf graduiert auf- │
│                bauen, Nacken schmal,     │
│                vorne weich               │
│  Warum:        Gegengewicht verteilt den │
│                Blick                     │
│  Achtung:      nicht zu tief, nicht nur  │
│                oben, vorne nichts Spitzes│
│                                          │
│  „Hinten Aufbau, vorne Ruhe.“            │
└──────────────────────────────────────────┘
```

Alle Texte dafür sind oben mit **[S]** markiert.

---

## 8. Wiederverwendbare Struktur für weitere Fälle

Jeder neue Fall füllt dieselben Felder aus. So bleibt das Tool einheitlich:

| Feld | Inhalt beim Pilotfall |
|------|-----------------------|
| Titel | Lange Nase im Profil |
| Ansicht | Profil |
| Lernziel | Nase wirkt im Verhältnis zur Kopfform |
| Ausgangsform (Bild + Text) | Form A, flacher Hinterkopf |
| Zielwirkung (Bild + Text) | Form B, Gleichgewicht vorne/hinten |
| Schnittentscheidung (Zonen + Text) | Graduation Hinterkopf, Nacken schmal, vorne weich |
| Warum es wirkt | Gegengewicht, Blickführung |
| Darauf achten (Fehlerbilder + Checkliste) | zu tief, zu hoch, spitz nach vorne, flach zurück |
| Einblendungen | Hilfslinien, Gewicht, Blickpunkt, Schnittzonen, Schädelform |
| Verständnis-Check | 5 Fragen |
| Merksatz | Hinten Aufbau, vorne Ruhe |

---

## Offene Punkte für den nächsten Schritt

- Wer zeichnet die Silhouetten (Form A, Form B, Fehlerbilder)?
  Wichtig: exakt gleiche Kopf- und Nasenkontur in allen Varianten.
- Soll der Vorher-/Nachher-Regler stufenlos sein oder in 3 festen Stufen?
- Wo im Lernquiz wird das Tool eingebunden (eigener Bereich oder im Themenblock
  „Beratung / Gesichtsformen“)?
- Sollen Ergebnisse des Verständnis-Checks gespeichert werden? Falls ja, gilt
  die Sicherheits-Checkliste aus `CLAUDE.md` (neue Tabelle → RLS von Anfang an).
