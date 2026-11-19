# Piemonte One Health AMR Atlas

Edizione regionale `pie_amr_atlas`, pubblicata da Codex Vitae ETS sulla stessa
base delle edizioni Lombardia, Veneto e Liguria.

## Stato

Letteratura scientifica del 19 novembre 2026: 64 studi con collegamento
territoriale esplicito al Piemonte, in sei layer (AMR umana, veterinaria,
alimentare, ambientale, fauna selvatica, studi a scala regionale).

- AMR umana: 13 elementi, 37 studi (sette strutture nominate, comuni di Torino
  e Cuneo, Città metropolitana di Torino, province di Vercelli, Novara e
  Alessandria);
- AMR veterinaria: 3 elementi, 8 studi (Ospedale Veterinario Universitario di
  Grugliasco, Città metropolitana di Torino, provincia di Cuneo);
- AMR alimentare: nessun elemento;
- AMR ambientale: nessun elemento (lo studio sui depuratori 36527555 resta
  dubbio e non è incluso);
- AMR nella fauna selvatica: 1 elemento, 2 studi (centri di recupero non
  localizzati, Città metropolitana di Torino);
- studi a scala regionale: 1 elemento, 17 studi.

I layer vuoti e le aree senza segnaposto sono nessuna evidenza pubblicata,
non resistenza zero. Ogni popup cita lo studio e il DOI (o il record PubMed
se il DOI non è assegnato) e ricorda che il segnaposto è il luogo dello
studio, non una prevalenza.

Fonti istituzionali pubbliche: AR-ISS 2024 (CC BY 4.0) e AIFA Open Data 2024,
antibatterici J01 (CC BY 4.0). Copertura AR-ISS 2024 del Piemonte: 39,0%,
senza rete regionale propria; i sei indicatori non rappresentano tutta la
regione. Confini ISTAT 2026 (1.180 comuni, 7 province e la Città metropolitana
di Torino, regione), letti in UTF-8. Otto strutture nominate © OpenStreetMap
contributors, ODbL. Regione Piemonte, SeREMI e il PDF OsMed sono esclusi:
vedi `metadata/EXCLUDED_SOURCES.md`.

Il conteggio in homepage e in pubblicazioni legge
`public/data/literature-catalog.json` (64).

## Pagine

Sorgente su `main`. Il sito statico è pubblicato dal branch `gh-pages`
(GitHub Pages, cartella `/`). Nessun file `CNAME`. Analitica: GoatCounter
`https://atlanteamr.goatcounter.com/count`, come le edizioni Lombardia, Veneto
e Liguria.

## Build locale

```bash
python3 -m http.server 8000
```

Aprire `http://localhost:8000/`.

Per rigenerare i dati pubblici servono gli input in `raw/` e, per i confini,
l'archivio ISTAT indicato in `metadata/SNAPSHOTS.tsv`:

```bash
pip install -r requirements-geodata.txt
python3 scripts/build_istat_geography.py --source-root <Limiti01012026_g> --output-root public/geography
python3 scripts/build_literature_catalog.py
python3 scripts/build_study_evidence_layers.py
```

## Directory

- `public/`: dati e asset approvati per il sito;
- `metadata/`: fonti, snapshot, ambito pubblico e fonti escluse;
- `raw/`: curatela, esummary e risposte Nominatim;
- `scripts/`: ricostruzione del catalogo e dei layer;
- `private/`: nessun dato riservato in questa edizione.
