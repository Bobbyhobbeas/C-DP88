# DP8 – Dagtakenlijst (Attractiepark)

## Wat zit hier in
- `schema.sql` – DB + seed
- `dp8_run.py` – FR2/FR3/FR4/FR6 logica
- `acceptatie_output.json` – output voor acceptatie (NFR4)
- `testrapport.pdf` – ingevuld testrapport met screenshots

## Hoe runnen
1. MySQL: `SOURCE schema.sql` of de statements in Workbench uitvoeren.
2. Python: `pip install mysql-connector-python` (of PyMySQL)  
   `python dp8_run.py` → schrijft `acceptatie_output.json`.
3. Upload `acceptatie_output.json` in de acceptatieomgeving.

## Korte uitleg
- **FR2**: SELECT op `Personeelslid` en `Onderhoudstaak` (parameterized in code).  
- **FR4**: max_fysieke_belasting = min(leeftijdsgrens, verlaagde waarde).  
- **FR6**: filter taken op beroep + bevoegdheid + ≤ max_belasting.  
- **FR3/NFR4**: schrijf JSON in het vereiste format en laad het in de acceptatie.
