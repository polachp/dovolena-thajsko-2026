"""Sestaví web ze src/verze.json, src/sablona.html a verze/<id>/thajsko-phuket-bangkok.md.

Nová verze:
  1. mkdir verze/vN a uložit tam upravený thajsko-phuket-bangkok.md
  2. přidat záznam vN do src/verze.json (datum, název, změny, hlavička)
  3. python build.py
Starší verze se nemění, kořen webu vždy ukazuje poslední verzi.
"""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).parent
SABLONA = (ROOT / "src/sablona.html").read_text(encoding="utf-8")
VERZE = json.loads((ROOT / "src/verze.json").read_text(encoding="utf-8"))

MISTA = [
    ("Andaman", "Phuket Town"), (None, "Koh Yao Noi"), (None, "Krabi Town"), (None, "Khao Lak"),
    ("Prales", "Khao Sok, Cheow Lan"), (None, None), ("Záliv", "Prachuap, Kui Buri"),
    (None, "Sam Roi Yot"), (None, "Bangkok"),
]


def obsah_js(md: str) -> str:
    for bad in ("`", "${", "\\"):
        if bad in md:
            raise SystemExit(f"Markdown obsahuje {bad!r}, do JS šablony nejde vložit.")
    return "// Generováno z thajsko-phuket-bangkok.md skriptem build.py, needitovat ručně.\nwindow.THAJSKO_MD = `" + md + "`;\n"


def stranka(v: dict, base: str) -> str:
    h = v["hlavicka"]
    facts = "\n".join(f"    <div><span>{k} </span><b>{x}</b></div>" for k, x in h["facts"])
    route = []
    for i, ((side, misto), noci) in enumerate(zip(MISTA, h["route"]), start=1):
        misto = misto or h["faze6"]
        route.append(
            f'    <li><a href="#faze-{i}"><span class="side">{side or "&nbsp;"}</span>'
            f'<span class="dot">{i}</span><span class="pl">{misto}</span><span class="n">{noci}</span></a></li>'
        )
    cfg = json.dumps({"id": v["id"], "base": base}, ensure_ascii=False)
    return (SABLONA.replace("{{EYEBROW}}", h["eyebrow"]).replace("{{FACTS}}", facts)
            .replace("{{ROUTE}}", "\n".join(route)).replace("{{CFG}}", cfg).replace("{{BASE}}", base))


def main():
    verejne = [{k: v.get(k) for k in ("id", "datum", "nazev", "zmeny", "commit")} for v in VERZE]
    (ROOT / "verze.js").write_text(
        "// Generováno skriptem build.py ze src/verze.json.\nwindow.THAJSKO_VERZE = "
        + json.dumps(verejne, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")

    for v in VERZE:
        d = ROOT / "verze" / v["id"]
        md = (d / "thajsko-phuket-bangkok.md").read_text(encoding="utf-8")
        (d / "thajsko-obsah.js").write_text(obsah_js(md), encoding="utf-8")
        (d / "index.html").write_text(stranka(v, "../../"), encoding="utf-8")

    posledni = VERZE[-1]
    d = ROOT / "verze" / posledni["id"]
    shutil.copyfile(d / "thajsko-phuket-bangkok.md", ROOT / "thajsko-phuket-bangkok.md")
    shutil.copyfile(d / "thajsko-obsah.js", ROOT / "thajsko-obsah.js")
    (ROOT / "index.html").write_text(stranka(posledni, "./"), encoding="utf-8")

    radky = ["# Změnový list", "", "Itinerář Thajsko Phuket → Bangkok. Nejnovější verze nahoře.", ""]
    for i in range(len(VERZE) - 1, -1, -1):
        v = VERZE[i]
        radky += [f"## {v['id']}: {v['nazev']} ({v['datum']})", ""]
        odkazy = [f"[web](https://polachp.github.io/dovolena-thajsko-2026/verze/{v['id']}/)",
                  f"[Markdown](verze/{v['id']}/thajsko-phuket-bangkok.md)"]
        if i > 0 and v.get("commit") and VERZE[i-1].get("commit"):
            odkazy.append(f"[rozdíl proti {VERZE[i-1]['id']}](https://github.com/polachp/dovolena-thajsko-2026/compare/{VERZE[i-1]['commit']}...{v['commit']})")
        radky += [" · ".join(odkazy), ""] + [f"- {z}" for z in v["zmeny"]] + [""]
    (ROOT / "ZMENY.md").write_text("\n".join(radky), encoding="utf-8")
    print("Hotovo:", ", ".join(v["id"] for v in VERZE), "| aktuální:", posledni["id"])


if __name__ == "__main__":
    main()
