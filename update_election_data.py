import urllib.request
import json
import os

def fetch_and_save_tse_data():
    base = "https://resultados.tse.jus.br/oficial/ele2026/6259/dados/sp/"
    headers = {"User-Agent": "Mozilla/5.0"}

    for cargo_num, fname in [(7, "raw_estadual_tse.json"), (6, "raw_federal_tse.json")]:
        url = f"{base}sp-c{cargo_num:04d}-e006259-u.json"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                with open(fname, "wb") as f:
                    f.write(data)
                print(f"Baixado {fname} do TSE ({len(data)} bytes)")
        except Exception as e:
            print(f"Aviso ao baixar {url}: {e}. Usando arquivo local existente se disponível.")

def process_tse(raw_file, cargo_nome, cargo_cod):
    with open(raw_file, "r", encoding="utf-8") as f:
        raw = json.load(f)
    
    carg = raw["carg"][0]
    qe = int(carg["qe"])
    vagas_tot = int(carg["nv"])
    
    v_info = raw.get("v", {})
    s_info = raw.get("s", {})
    geral = {
        "total_apurado": int(v_info.get("tv", 0)),
        "validos": int(v_info.get("vv", 0)),
        "brancos": int(v_info.get("vb", 0)),
        "nulos": int(v_info.get("tvn", 0)),
        "secoes_pct": s_info.get("pst", "100,00"),
        "horario": raw.get("ht", "22:58:07"),
        "qe": qe,
        "vagas": vagas_tot
    }
    
    cutoff_10 = qe * 0.1
    cutoff_20 = qe * 0.2
    cutoff_80 = qe * 0.8
    
    partidos_dict = {}
    fed_dict = {}
    all_cands = []
    
    for agr in carg["agr"]:
        agr_nm = agr["nm"]
        is_fed = agr.get("tp") == "f" or "FEDERAÇÃO" in agr_nm
        fed_label = agr_nm if is_fed else "-"
        
        tot_agr_votos = 0
        agr_cands = []
        
        for par in agr["par"]:
            sg = par["sg"]
            nm = par["nm"]
            tvtn = int(par.get("tvtn", 0))
            tvtl = int(par.get("tvtl", 0))
            tot_p = tvtn + tvtl
            tot_agr_votos += tot_p
            
            p_cands = []
            for c in par.get("cand", []):
                c_obj = {
                    "num": str(c["n"]),
                    "nome": str(c["nmu"]),
                    "partido": sg,
                    "agr": agr_nm,
                    "votos": int(c.get("vap", 0)),
                    "e": c.get("e") == "s",
                    "st": c.get("st", "")
                }
                p_cands.append(c_obj)
                agr_cands.append(c_obj)
                all_cands.append(c_obj)
                
            vagas_partido = sum(1 for c in p_cands if c["e"])
            
            partidos_dict[sg] = {
                "sg": sg,
                "nm": nm,
                "fed": fed_label,
                "tvtn": tvtn,
                "tvtl": tvtl,
                "tot": tot_p,
                "vagas": vagas_partido
            }
            
        agr_cands.sort(key=lambda x: x["votos"], reverse=True)
        raw_qp = tot_agr_votos // qe
        cands_10 = [c for c in agr_cands if c["votos"] >= cutoff_10]
        qp = min(raw_qp, len(cands_10))
        
        fed_dict[agr_nm] = {
            "nm": agr_nm,
            "votos": tot_agr_votos,
            "qp": qp,
            "seats": qp,
            "cands": agr_cands,
            "tse_vagas": int(agr.get("vag", 0))
        }

    validos_tot = geral["validos"]
    partidos_list = list(partidos_dict.values())
    partidos_list.sort(key=lambda x: x["tot"], reverse=True)
    for p in partidos_list:
        p["pct"] = round((p["tot"] / validos_tot) * 100, 2)
        
    eleitos = [c for c in all_cands if c["e"]]
    eleitos.sort(key=lambda x: x["votos"], reverse=True)
    eleitos_clean = [
        {
            "num": c["num"],
            "nome": c["nome"],
            "partido": c["partido"],
            "agr": c["agr"],
            "votos": c["votos"]
        }
        for c in eleitos
    ]
    
    qp_total = sum(f["qp"] for f in fed_dict.values())
    sobras_total = vagas_tot - qp_total
    
    historico_sobras = []
    for r in range(1, sobras_total + 1):
        medias = []
        for nm, f in fed_dict.items():
            if f["votos"] >= cutoff_80:
                media = f["votos"] / (f["seats"] + 1)
                cand_idx = f["seats"]
                cand = f["cands"][cand_idx] if cand_idx < len(f["cands"]) else None
                if cand and cand["votos"] >= cutoff_20:
                    medias.append((media, nm, cand))
        medias.sort(key=lambda x: x[0], reverse=True)
        winner_media, winner_nm, winner_cand = medias[0]
        runner_media, runner_nm, runner_cand = medias[1] if len(medias) > 1 else (0, "Nenhum", None)
        
        fed_dict[winner_nm]["seats"] += 1
        historico_sobras.append({
            "rodada": r,
            "partido": winner_nm,
            "media": winner_media,
            "cand": {
                "num": winner_cand["num"],
                "nome": winner_cand["nome"],
                "partido": winner_cand["partido"],
                "votos": winner_cand["votos"]
            },
            "runner": runner_nm,
            "runner_media": runner_media
        })

    proximos_fila = []
    for nm, f in fed_dict.items():
        if f["votos"] >= cutoff_80:
            media = f["votos"] / (f["seats"] + 1)
            cand_idx = f["seats"]
            cand = f["cands"][cand_idx] if cand_idx < len(f["cands"]) else None
            if cand and cand["votos"] >= cutoff_20:
                proximos_fila.append({
                    "partido": nm,
                    "media": media,
                    "cand": {
                        "num": cand["num"],
                        "nome": cand["nome"],
                        "partido": cand["partido"],
                        "votos": cand["votos"]
                    }
                })
    proximos_fila.sort(key=lambda x: x["media"], reverse=True)

    duelos_internos = []
    for nm, f in fed_dict.items():
        vagas = f["seats"]
        if vagas > 0 and len(f["cands"]) > vagas:
            ultimo = f["cands"][vagas - 1]
            suplente = f["cands"][vagas]
            diff = ultimo["votos"] - suplente["votos"]
            duelos_internos.append({
                "partido": nm,
                "vagas": vagas,
                "ultimo": {
                    "num": ultimo["num"],
                    "nome": ultimo["nome"],
                    "partido": ultimo["partido"],
                    "votos": ultimo["votos"]
                },
                "suplente": {
                    "num": suplente["num"],
                    "nome": suplente["nome"],
                    "partido": suplente["partido"],
                    "votos": suplente["votos"]
                },
                "diff": diff
            })
    duelos_internos.sort(key=lambda x: x["diff"])

    return {
        "cargo": cargo_nome,
        "cargo_cod": cargo_cod,
        "geral": geral,
        "partidos": partidos_list,
        "eleitos": eleitos_clean,
        "sobras_tot": sobras_total,
        "historico_sobras": historico_sobras,
        "proximos_fila": proximos_fila,
        "duelos_internos": duelos_internos
    }

if __name__ == "__main__":
    fetch_and_save_tse_data()
    
    data_est = process_tse("raw_estadual_tse.json", "Deputado Estadual", 7)
    data_fed = process_tse("raw_federal_tse.json", "Deputado Federal", 6)

    with open("dados_estadual.json", "w", encoding="utf-8") as f:
        json.dump(data_est, f, ensure_ascii=False, indent=2)

    with open("dados_federal.json", "w", encoding="utf-8") as f:
        json.dump(data_fed, f, ensure_ascii=False, indent=2)

    data_eleicao = {
        "geral": data_fed["geral"],
        "partidos": data_fed["partidos"],
        "eleitos": data_fed["eleitos"]
    }
    with open("dados_eleicao.json", "w", encoding="utf-8") as f:
        json.dump(data_eleicao, f, ensure_ascii=False, indent=2)

    print("Arquivos JSON atualizados com sucesso.")
    
    # Regenerar index.html
    import build_sober_dashboard
    print("Dashboard index.html atualizado.")
