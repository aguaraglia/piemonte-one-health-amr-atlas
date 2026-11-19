# Fonti escluse o non disponibili per l'atlante Piemonte (verifica riuso 2026-11-19, grok-05dev)

Regola di Alex: senza un permesso di riuso chiaro, la fonte non entra nell'atlante. Nessuna email inviata, nessuna richiesta di autorizzazione.

## Regione Piemonte: pagina AMR, Report consumo antibiotici 2019-2022, cruscotto TS — ESCLUSO
- Pagina AMR per operatori: https://www.regione.piemonte.it/web/temi/sanita/prevenzione/antibiotico-resistenza-indicazioni-per-operatori-sanitari (HTTP 200). Elenca le sorveglianze attive (AR-ISS, ICA, C. auris, CRE, PNCAR, SPiNCAR), un cruscotto sull'uso di antibiotici da dati Tessera Sanitaria e il «Report consumo antibiotici in Piemonte 2019-2022 - edizione 2023» (https://www.regione.piemonte.it/web/media/44757/download, HTTP 200, non scaricato nel pacchetto).
- Note legali (https://www.regione.piemonte.it/web/note-legali-privacy): «Essi possono essere utilizzati previa autorizzazione di Regione Piemonte»; citazione ammessa solo «a titolo di cronaca o recensione».
- Esito: serve un'autorizzazione esplicita. ESCLUSO.

## SeREMI (ASL AL, Servizio di riferimento regionale di epidemiologia) — ESCLUSO
- Pubblicazioni: https://www.seremi.it/pubblicazioni. Report AMR 2015-2016, 2015-2018, 2015-2020; «Isolamenti di laboratorio da sangue e liquor di alcuni microrganismi alert. Report 2021 ed. 2023»; Report CRE 2014-2020 e 2020-2021; consumo antibiotici territorio 2013-2016 e regionale 2017-2018 (ed. 2020). Dati raccolti con la piattaforma web regionale «Gemini» da tutti i laboratori pubblici del SSR e da alcune strutture convenzionate.
- Il sito non riporta alcuna licenza, copyright o condizione di riproduzione (c'è solo l'informativa privacy; la pagina note legali risponde 404). Il report 2021 è stato scaricato solo per consultazione (sha256 in SNAPSHOTS.tsv).
- Esito: nessun permesso di riuso. ESCLUSO.

## AIFA, Rapporto OsMed regionale 2024 (PDF) — ESCLUSO, sostituito
- Come per la Liguria: il PDF è coperto dal copyright del sito AIFA (https://www.aifa.gov.it/copyright). Usato al suo posto l'aggregato J01 degli Open Data AIFA 2024 (CC BY 4.0).

## IZS Piemonte, Liguria e Valle d'Aosta (IZSPLV) — nessun dato da usare
- Note legali (https://www.izsplv.it/it/note-legali.html): testi e tabelle in CC BY-NC 4.0. Nessun dato AMR veterinario pubblico per provincia o regione (stessa verifica dell'edizione Liguria). Gli articoli IZSPLV restano nel catalogo come letteratura.

## Arpa Piemonte — nessun dato da usare (licenza aperta, dati non ancora pubblicati)
- Note legali (https://www.arpa.piemonte.it/note-legali): contenuti e open data in CC BY 4.0, con fonte «Arpa Piemonte - www.arpa.piemonte.it».
- AMR nei reflui: D.G.R. 30 luglio 2026, n. 3-2907 (https://www.regione.piemonte.it/governo/bollettino/abbonati/2026/31/suppo2/00000014.htm), attuazione della D.G.R. 30-1317 del 30/06/2025 (PNCAR): fondi a IZSPLV, ARPA Piemonte e UniTo per il monitoraggio delle resistenze nei reflui urbani fino al 31/12/2028 (max 505.680 euro). Gare ARPA 2026 per reagenti e sonde del CRBAS di La Loggia. Nessun dato pubblicato al 2026-11-19.
- Esito: nessun layer ambientale istituzionale. Quando ARPA pubblicherà i dati, la licenza CC BY 4.0 ne consente l'uso.

## Open data regionali e nazionali
- dati.piemonte.it: l'API CKAN non risponde (404). dati.gov.it (CKAN): 0 dataset per «antibiotici», «antibiotico», «antimicrobica»; «antibiotico-resistenza» restituisce solo dataset sulla Resistenza storica.
- IGR Piemonte e portali aria.ambiente: CC BY 4.0, ma senza dati AMR.

## ISS, sorveglianza CRE (RIS-4/2025) — non estratto
- Come per la Liguria: il valore regionale è solo nella mappa, non in tabella; non estratto.
