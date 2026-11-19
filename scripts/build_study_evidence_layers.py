#!/usr/bin/env python3
"""Build Piemonte study evidence layers from the curated literature catalog.

Geometries come from the ISTAT 2026 boundaries of this edition, from a named
facility geocoded on OpenStreetMap Nominatim (1 req/s, 2026-11-19, raw
responses in raw/nominatim/). The script does not geocode farms, kennels or shelters and does not
invent a site the catalog does not name.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = "Il segnaposto indica dove è stato condotto lo studio, non una prevalenza."
SECTOR = {
    "healthcare_amr": "AMR clinica",
    "human_antimicrobial_use": "Consumo di antimicrobici",
    "antimicrobial_stewardship": "Stewardship antimicrobica",
    "veterinary_amr": "AMR veterinaria",
    "companion_animal_amr": "AMR negli animali d'affezione",
    "environmental_amr": "AMR ambientale",
    "foodborne_amr": "AMR alimentare",
    "wildlife_amr": "AMR nella fauna selvatica",
}
# Nominatim results checked on 2026-11-19 (raw/nominatim/results_2026-11-19.json).
# Coordinates are the facility returned for the named institution, not a sample.
POINTS = {
    "cds": (7.6744085, 45.0394675, "AOU Città della Salute e della Scienza di Torino (Presidio Molinette)",
            "OpenStreetMap Nominatim: Ospedale Molinette, Corso Bramante 88/90, Torino (amenity=hospital)."),
    "rm": (7.6749011, 45.0346655, "Ospedale Infantile Regina Margherita, Torino",
           "OpenStreetMap Nominatim: Ospedale Infantile Regina Margherita, Piazza Polonia, Torino (amenity=hospital)."),
    "oft": (7.6706178, 45.0741641, "Ospedale Oftalmico, Torino",
            "OpenStreetMap Nominatim: Ospedale Oftalmico Sperino, Via Bertola, Torino (amenity=hospital)."),
    "sl": (7.5571032, 45.0285933, "AOU San Luigi Gonzaga, Orbassano",
           "OpenStreetMap Nominatim: Ospedale San Luigi Gonzaga, Via San Luigi, Orbassano (amenity=hospital)."),
    "scc": (7.5370542, 44.3853167, "AO S. Croce e Carle, Cuneo",
            "OpenStreetMap Nominatim: Ospedale Santa Croce, Via Michele Coppino 26, Cuneo (amenity=hospital)."),
    "al": (8.6221526, 44.9161580, "AOU SS. Antonio e Biagio e Cesare Arrigo, Alessandria",
           "OpenStreetMap Nominatim: Ospedale Civile Santi Antonio e Biagio e Cesare Arrigo, Via San Pio V, Alessandria (amenity=hospital)."),
    "arr": (8.6259715, 44.9162274, "Ospedale Infantile Cesare Arrigo, Alessandria",
            "OpenStreetMap Nominatim: Ospedale Infantile Cesare Arrigo, Spalto Marengo 46, Alessandria (amenity=hospital)."),
    "ovu": (7.5910723, 45.0679786, "Ospedale Veterinario Universitario, Università di Torino (Grugliasco)",
            "OpenStreetMap Nominatim: Ospedale Veterinario Universitario, Largo Paolo Braccini 2, Grugliasco (amenity=veterinary)."),
}
ORGANISM = {
    "pubmed_41137582": "Campylobacter spp. (animali da compagnia, da reddito e selvatici)",
    "pubmed_41963697": "infezioni multiresistenti pediatriche (fosfomicina)",
    "pubmed_42075683": "Staphylococcus spp. condivisi tra cani e proprietari",
    "pubmed_42197353": "geni di resistenza nel microbiota delle api",
    "pubmed_42643404": "Actinobacillus pleuropneumoniae (suini)",
    "pubmed_39779737": "colonizzazione da Enterobacterales ESBL (trapianto)",
    "pubmed_39860416": "batteri multiresistenti in terapia intensiva COVID-19",
    "pubmed_40113017": "uso di antimicrobici e ICA (PPS-3 regionale)",
    "pubmed_40239439": "patogeni suini in sorveglianza AMR",
    "pubmed_40635096": "attuazione del PNCAR (SPiNCAR-1)",
    "pubmed_40804996": "Escherichia coli (ricci)",
    "pubmed_40851865": "batteri da batteriemia dopo trapianto allogenico",
    "pubmed_40869516": "Enterobacterales produttori di NDM",
    "pubmed_37985552": "K. pneumoniae KPC resistente a ceftazidime/avibactam",
    "pubmed_38018764": "enterococchi resistenti alla vancomicina (VRE)",
    "pubmed_38398779": "infezioni nosocomiali in portatori di LVAD",
    "pubmed_38543478": "Campylobacter spp. da isolati umani",
    "pubmed_38637766": "patogeni multiresistenti nella VAP",
    "pubmed_38674669": "uso di ceftobiprole (stewardship)",
    "pubmed_38725026": "attività di stewardship durante COVID-19",
    "pubmed_38820893": "indicatori dei programmi di stewardship",
    "pubmed_38866074": "batteri da piometra canina",
    "pubmed_39200039": "Streptococcus pneumoniae invasivo",
    "pubmed_39252070": "stafilococchi meticillino-resistenti (cavalli e addetti)",
    "pubmed_39597563": "Escherichia coli uropatogeno (cani e gatti)",
    "pubmed_35709971": "indicatori dei programmi di stewardship 2017-2019",
    "pubmed_36621272": "Escherichia coli (uccelli selvatici)",
    "pubmed_36678437": "Salmonella spp. da isolati umani",
    "pubmed_36801627": "A. baumannii, K. pneumoniae, P. aeruginosa (sepsi)",
    "pubmed_36902196": "K. pneumoniae KPC resistente a ceftazidime/avibactam",
    "pubmed_36908871": "profilassi con levofloxacina in leucemia",
    "pubmed_36985315": "batteri da batteriemia dopo trapianto allogenico",
    "pubmed_38186699": "Enterobacterales resistenti ai carbapenemi (colonizzazione)",
    "pubmed_38334490": "consumo territoriale di antibiotici",
    "pubmed_35061145": "Enterobacterales produttori di carbapenemasi",
    "pubmed_35504616": "batteriemie multiresistenti in medicina interna",
    "pubmed_35625339": "infezioni ospedaliere MDR e uso di antibiotici",
    "pubmed_35693730": "uso di antimicrobici e trend MDR (manuale di terapia)",
    "pubmed_35889963": "patogeni resistenti ai carbapenemi in terapia intensiva",
    "pubmed_36140036": "programmi di stewardship e contesto culturale",
    "pubmed_36288159": "antimicrobici perioperatori nella chirurgia delle coliche (cavalli)",
    "pubmed_36293992": "prescrizione di antimicrobici nelle RSA",
    "pubmed_36534066": "Escherichia coli resistente ad amoxicillina/clavulanato",
    "pubmed_36551431": "Escherichia coli ESBL (suini e ambiente)",
    "pubmed_31875683": "batteri da infezioni oculari",
    "pubmed_33570474": "MRSA associato al bestiame (vitelli)",
    "pubmed_34064943": "infezioni urinarie di cani e gatti (stewardship)",
    "pubmed_34198805": "MRCoNS e MRSA (suini e addetti)",
    "pubmed_34203490": "uso di antimicrobici negli allevamenti bovini da ingrasso",
    "pubmed_34571699": "batteri resistenti nei pazienti COVID-19",
    "pubmed_34835398": "K. pneumoniae produttrice di carbapenemasi (trapianti)",
    "pubmed_31848106": "programma di stewardship ospedaliero",
    "pubmed_32118283": "K. pneumoniae OXA-48 e NDM-1 (ST101)",
    "pubmed_32961926": "geni di resistenza nella saliva",
    "pubmed_32971788": "patogeni ospedalieri resistenti",
    "pubmed_29096992": "K. pneumoniae KPC, Enterobacterales ESBL, Candida, C. difficile",
    "pubmed_27438306": "batteri da infezioni oculari gravi",
    "pubmed_28368074": "K. pneumoniae resistente ai carbapenemi (trapianto)",
    "pubmed_28011968": "Enterobacterales ESBL in pediatria",
    "pubmed_26110291": "batteriemie pediatriche correlate all'assistenza",
    "pubmed_25759352": "uso di antimicrobici e ICA nelle residenze (HALT-2)",
    "pubmed_22507991": "infezioni nelle RSA",
    "pubmed_21353947": "Staphylococcus aureus meticillino-resistente (MRSA)",
    "pubmed_22106909": "batteri da congiuntivite, antibiotici topici",
}

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def feature(geometry, place, level, basis, studies, extra_note=""):
    note = NOTE + (" " + extra_note if extra_note else "")
    return {"type": "Feature", "geometry": geometry, "properties": {
        "place": place, "geography_level": level, "geography_basis": basis,
        "study_count": len(studies), "study_ids": "; ".join(s["id"] for s in studies),
        "authors": " | ".join(s["authors"] for s in studies), "year": " | ".join(s["year"] for s in studies),
        "title": " | ".join(s["title"] for s in studies), "sector": " | ".join(s["sector"] for s in studies),
        "organism": " | ".join(s["organism"] for s in studies), "doi": " | ".join(s["doi"] for s in studies),
        "geography_note": note}}

def point(key):
    lon, lat, _l, _s = POINTS[key]
    return {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]}

def place_basis(key, text):
    return f"{text} {POINTS[key][3]}"

def merge(geoms):
    if len(geoms) == 1:
        return geoms[0]
    polys = []
    for g in geoms:
        polys.extend([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"])
    return {"type": "MultiPolygon", "coordinates": polys}

def main():
    catalog = load_json(ROOT / "public/data/literature-catalog.json")
    by_id = {r["id"]: r for r in catalog["records"]}
    miss = set(by_id) - set(ORGANISM)
    if miss:
        raise SystemExit("Organismo mancante: " + ", ".join(sorted(miss)))

    def card(sid):
        r = by_id[sid]; doi = r.get("doi") or ""
        return {"id": sid, "authors": r["authors"], "year": str(r["year"]), "title": r["title"].rstrip("."),
                "sector": SECTOR[r["scope"]], "organism": ORGANISM[sid],
                "doi": f"https://doi.org/{doi}" if doi else r["source_url"]}

    mun = {f["properties"]["name"]: f["geometry"] for f in load_json(ROOT / "public/geography/atlas_municipalities.geojson")["features"]}
    prov = {f["properties"]["name"]: f["geometry"] for f in load_json(ROOT / "public/geography/atlas_provinces.geojson")["features"]}
    region = load_json(ROOT / "public/geography/atlas_region.geojson")["features"][0]["geometry"]

    layers = {k: [] for k in ["human", "veterinary", "food", "environment", "wildlife", "regional"]}
    placed = {}

    def add(layer, ids, geometry, place, level, basis, extra=""):
        for sid in ids:
            placed[sid] = placed.get(sid, "") + f"{level}: {place}; "
        layers[layer].append(feature(geometry, place, level, basis, [card(s) for s in ids], extra))

    P = lambda *ids: [f"pubmed_{i}" for i in ids]
    def at(layer, key, ids, text):
        add(layer, P(*ids), point(key), POINTS[key][2], "struttura", place_basis(key, text))
    at("human", "cds", ("29096992", "35625339", "36902196", "38186699", "38637766", "39779737", "40851865", "40869516",
                        "39860416", "38674669", "37985552", "36908871", "35889963", "35693730", "34835398"),
       "Città della Salute e della Scienza / Molinette nominata nell'abstract o nel testo integrale (per lo studio multicentrico, quota torinese separata).")
    at("human", "oft", ("22106909", "27438306", "31875683"), "Ospedale Oftalmico di Torino nominato nell'abstract o nel testo integrale.")
    at("human", "scc", ("35504616",), "AO S. Croce e Carle di Cuneo nominata nell'abstract o nel testo integrale.")
    at("human", "arr", ("36534066",), "Ospedale Infantile Cesare Arrigo di Alessandria nominato nell'abstract o nel testo integrale.")
    at("human", "al", ("36801627",), "AOU SS. Antonio e Biagio e Cesare Arrigo di Alessandria nominata nell'abstract o nel testo integrale.")
    at("human", "rm", ("41963697",), "Ospedale Infantile Regina Margherita nominato nell'abstract o nel testo integrale.")
    at("human", "sl", ("34571699",), "AOU San Luigi Gonzaga di Orbassano nominata nel testo integrale.")
    at("veterinary", "ovu", ("38866074", "39597563", "36288159"), "Ospedale veterinario universitario dell'Università di Torino nominato nell'abstract o nel testo integrale.")
    add("human", P("26110291", "28011968", "28368074", "32961926", "36985315", "38018764", "38398779"), mun["Torino"], "Torino", "comune",
        "Gli autori dichiarano ospedali, reparti o partecipanti di Torino senza nominare la struttura: poligono ISTAT del comune.")
    add("human", P("32118283"), mun["Cuneo"], "Cuneo", "comune",
        "Caso clinico in un reparto di Cuneo, struttura non nominata: poligono ISTAT del comune.")
    add("human", P("21353947", "32971788"), prov["Torino"], "Città metropolitana di Torino", "provincia",
        "Ospedale universitario 'near Torino' o 'on the outskirts of Turin', non nominato: poligono ISTAT della Città metropolitana.")
    add("human", P("22507991", "38334490"), prov["Vercelli"], "Provincia di Vercelli", "provincia",
        "RSA e consumo territoriale dell'ASL VC: poligono ISTAT della provincia.")
    add("human", P("36293992"), prov["Novara"], "Provincia di Novara", "provincia",
        "25 RSA dell'ASL NO, non nominate: poligono ISTAT della provincia.")
    add("human", P("31848106"), prov["Alessandria"], "Provincia di Alessandria", "provincia",
        "Ospedali di Casale Monferrato e Tortona (ASL AL): poligono ISTAT della provincia.")
    add("veterinary", P("42075683", "39252070", "34064943"), prov["Torino"], "Città metropolitana di Torino", "provincia",
        "Clinica veterinaria privata, scuderie o quota torinese dell'ospedale veterinario universitario, non localizzate: poligono ISTAT della Città metropolitana.")
    add("veterinary", P("42197353", "34198805"), prov["Cuneo"], "Provincia di Cuneo", "provincia",
        "Apiari e allevamenti suini non localizzati: poligono ISTAT della provincia.")
    add("wildlife", P("36621272", "40804996"), prov["Torino"], "Città metropolitana di Torino", "provincia",
        "Centri di recupero della fauna selvatica non localizzati: poligono ISTAT della Città metropolitana.")
    add("regional", P("25759352", "33570474", "35709971", "36140036", "36678437", "38543478", "38725026", "38820893", "39200039",
                      "40113017", "40239439", "40635096", "42643404", "41137582", "36551431", "35061145", "34203490"),
        region, "Piemonte", "regione",
        "Gli autori dichiarano il Piemonte, ospedali, RSA o allevamenti non nominati, o isolati raccolti in regione senza scala più fine. Il contorno regionale non è un punto di misura.")

    if set(placed) != set(by_id):
        raise SystemExit(f"Copertura incompleta. Mancanti: {sorted(set(by_id)-set(placed))}. Extra: {sorted(set(placed)-set(by_id))}")
    names = {"human": "human_amr_evidence.geojson", "veterinary": "veterinary_amr_evidence.geojson",
             "food": "food_chain_amr_evidence.geojson", "environment": "environmental_amr_evidence.geojson",
             "wildlife": "wildlife_amr_evidence.geojson", "regional": "regional_study_outline.geojson"}
    for k, fn in names.items():
        (ROOT / "public/data" / fn).write_text(json.dumps({"type": "FeatureCollection", "features": layers[k]}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(fn, len(layers[k]), sum(f["properties"]["study_count"] for f in layers[k]))
    print("studi collocati:", len(placed))

if __name__ == "__main__":
    main()
