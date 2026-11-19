# Geografia pubblica

La cartografia pubblica dell'edizione Piemonte comprende:

- `atlas_region.geojson`: confine regionale ISTAT 2026;
- `atlas_provinces.geojson`: 8 unità (Città metropolitana di Torino, Vercelli, Novara, Cuneo, Asti, Alessandria, Biella, Verbano-Cusio-Ossola) ISTAT 2026;
- `atlas_municipalities.geojson`: 1.180 comuni ISTAT al 1/1/2026.

I file sono letti in UTF-8 dal DBF ISTAT («Città metropolitana» corretto).

Gli studi della letteratura curata sono in layer distinti sotto `public/data/`,
non in questi confini di base. Un punto è una struttura nominata. Un poligono
è un comune o una provincia/città metropolitana. Il contorno regionale è
riservato agli studi che non dichiarano una scala più fine. Nessuna azienda,
allevamento, canile o rifugio è localizzato.
