import json
import mysql.connector
from typing import Any, Dict, List, Optional

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",   # pas aan als nodig
        user="root",        # pas aan
        password="MindStorm197?1970", # pas aan
        database="park"
    )

def query_personnel(conn, *, id: Optional[int]=None, naam: Optional[str]=None) -> Dict[str, Any]:
    sql = """
    SELECT id, naam, werktijd, beroepstype, bevoegdheid, specialist_in_attracties,
           pauze_opsplitsen, leeftijd, verlaagde_fysieke_belasting
    FROM Personeelslid
    WHERE {col} = %s
    """.format(col="id" if id is not None else "naam")
    param = (id if id is not None else naam,)
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, param)
    row = cur.fetchone()
    cur.close()
    if not row:
        raise ValueError("Personeelslid niet gevonden")
    if isinstance(row.get("specialist_in_attracties"), str):
        row["specialist_in_attracties"] = [s.strip() for s in row["specialist_in_attracties"].split(",") if s.strip()]
    return row

def query_tasks(conn, *, beroepstype: str, bevoegdheid: str, max_belasting: Optional[int]) -> List[Dict[str, Any]]:
    sql = """
    SELECT id, omschrijving, duur, prioriteit, beroepstype, bevoegdheid,
           fysieke_belasting, attractie, is_buitenwerk
    FROM Onderhoudstaak
    WHERE beroepstype = %s
      AND bevoegdheid = %s
      AND (fysieke_belasting IS NULL OR fysieke_belasting <= %s)
      AND (afgerond = 0)
    ORDER BY CASE WHEN prioriteit='Hoog' THEN 1 ELSE 2 END, id
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, (beroepstype, bevoegdheid, max_belasting if max_belasting is not None else 9999))
    rows = cur.fetchall()
    cur.close()
    return rows

def compute_max_belasting(leeftijd: int, verlaagd: Optional[int]) -> int:
    grens = 25 if leeftijd <= 24 else (40 if leeftijd <= 50 else 20)
    if verlaagd not in (None, 0):
        return min(grens, int(verlaagd))
    return grens

def build_output_json(pers: Dict[str, Any], taken: List[Dict[str, Any]], *, weer: Dict[str, Any]) -> Dict[str, Any]:
    personeelsgegevens = {
        "naam": pers["naam"],
        "werktijd": pers["werktijd"],
        "beroepstype": pers["beroepstype"],
        "bevoegdheid": pers["bevoegdheid"],
        "specialist_in_attracties": pers["specialist_in_attracties"],
        "pauze_opsplitsen": bool(pers["pauze_opsplitsen"]),
        "max_fysieke_belasting": pers["max_fysieke_belasting"],
    }
    dagtaken = [{
        "omschrijving": t["omschrijving"],
        "duur": int(t["duur"]),
        "prioriteit": t["prioriteit"],
        "beroepstype": t["beroepstype"],
        "bevoegdheid": t["bevoegdheid"],
        "fysieke_belasting": t["fysieke_belasting"],
        "attractie": t["attractie"],
        "is_buitenwerk": bool(t["is_buitenwerk"]),
    } for t in taken]
    totale_duur = sum(x["duur"] for x in dagtaken)
    return {
        "personeelsgegevens": personeelsgegevens,
        "weergegevens": weer,
        "dagtaken": dagtaken,
        "totale_duur": totale_duur,
    }

def main():
    conn = get_db_connection()
    try:
        pers = query_personnel(conn, naam="Piet de Jong")  # of id=1
        pers["max_fysieke_belasting"] = compute_max_belasting(pers["leeftijd"], pers["verlaagde_fysieke_belasting"])
        taken = query_tasks(conn, beroepstype=pers["beroepstype"], bevoegdheid=pers["bevoegdheid"],
                            max_belasting=pers["max_fysieke_belasting"])
        weer = {"temperatuur": 20, "kans_op_regen": 30}  # DP8: mag statisch
        output = build_output_json(pers, taken, weer=weer)
        with open("acceptatie_output.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print("Klaar → laad 'acceptatie_output.json' in de acceptatieomgeving en maak een screenshot.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
