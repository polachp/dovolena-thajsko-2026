"""Sestaví web ze src/verze.json, src/sablona.html a Markdownu každé verze (verze/<id>/<md>).

Nová verze:
  1. mkdir verze/vN a uložit tam upravený Markdown (název souboru je v poli "md")
  2. přidat záznam vN do src/verze.json (datum, název, změny, hlavička)
  3. python build.py
Starší verze se nemění, kořen webu vždy ukazuje poslední verzi.
"""
import json, shutil
from pathlib import Path

ROOT = Path(__file__).parent
SABLONA = (ROOT / "src/sablona.html").read_text(encoding="utf-8")
VERZE = json.loads((ROOT / "src/verze.json").read_text(encoding="utf-8"))

MD_VYCHOZI = "thajsko-phuket-bangkok.md"
SMER_VYCHOZI = ["Phuket", "Bangkok"]
LEDE_VYCHOZI = "Anežčin manuál s itinerářem otočeným pro přílet na Phuket a odlet z Bangkoku. Osnova, ne rozvrh: počty nocí jsou rozpětí, škrtat se dá."
MISTA_VYCHOZI = [
    ["Andaman", "Phuket Town"], [None, "Koh Yao Noi"], [None, "Krabi Town"], [None, "Khao Lak"],
    ["Prales", "Khao Sok, Cheow Lan"], [None, None], ["Záliv", "Prachuap, Kui Buri"],
    [None, "Sam Roi Yot"], [None, "Bangkok"],
]


def obsah_js(md: str) -> str:
    for bad in ("`", "${", "\\"):
        if bad in md:
            raise SystemExit(f"Markdown obsahuje {bad!r}, do JS šablony nejde vložit.")
    return "// Generováno z Markdownu verze skriptem build.py, needitovat ručně.\nwindow.THAJSKO_MD = `" + md + "`;\n"


def md_soubor(v: dict) -> str:
    return v.get("md", MD_VYCHOZI)


def stranka(v: dict, base: str) -> str:
    h = v["hlavicka"]
    facts = "\n".join(f"    <div><span>{k} </span><b>{x}</b></div>" for k, x in h["facts"])
    route = []
    for i, ((side, misto), noci) in enumerate(zip(h.get("mista", MISTA_VYCHOZI), h["route"]), start=1):
        misto = misto or h["faze6"]
        route.append(
            f'    <li><a href="#faze-{i}"><span class="side">{side or "&nbsp;"}</span>'
            f'<span class="dot">{i}</span><span class="pl">{misto}</span><span class="n">{noci}</span></a></li>'
        )
    cfg = json.dumps({"id": v["id"], "base": base}, ensure_ascii=False)
    a, z = v.get("smer", SMER_VYCHOZI)
    return (SABLONA.replace("{{TITLE}}", f"Thajsko {a}–{z}").replace("{{H1}}", f'{a} <span class="arrow">→</span> {z}')
            .replace("{{LEDE}}", v.get("lede", LEDE_VYCHOZI)).replace("{{MD}}", md_soubor(v))
            .replace("{{EYEBROW}}", h["eyebrow"]).replace("{{FACTS}}", facts)
            .replace("{{ROUTE}}", "\n".join(route)).replace("{{CFG}}", cfg).replace("{{BASE}}", base))


def main():
    verejne = [{**{k: v.get(k) for k in ("id", "datum", "nazev", "zmeny", "commit")}, "md": md_soubor(v)} for v in VERZE]
    (ROOT / "verze.js").write_text(
        "// Generováno skriptem build.py ze src/verze.json.\nwindow.THAJSKO_VERZE = "
        + json.dumps(verejne, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")

    for v in VERZE:
        d = ROOT / "verze" / v["id"]
        md = (d / md_soubor(v)).read_text(encoding="utf-8")
        (d / "thajsko-obsah.js").write_text(obsah_js(md), encoding="utf-8")
        (d / "index.html").write_text(stranka(v, "../../"), encoding="utf-8")

    posledni = VERZE[-1]
    d = ROOT / "verze" / posledni["id"]
    for stary in {md_soubor(x) for x in VERZE} - {md_soubor(posledni)}:
        (ROOT / stary).unlink(missing_ok=True)
    shutil.copyfile(d / md_soubor(posledni), ROOT / md_soubor(posledni))
    shutil.copyfile(d / "thajsko-obsah.js", ROOT / "thajsko-obsah.js")
    (ROOT / "index.html").write_text(stranka(posledni, "./"), encoding="utf-8")

    a, z = posledni.get("smer", SMER_VYCHOZI)
    radky = ["# Změnový list", "", f"Itinerář Thajsko, aktuálně směr {a} → {z}. Nejnovější verze nahoře.", ""]
    for i in range(len(VERZE) - 1, -1, -1):
        v = VERZE[i]
        radky += [f"## {v['id']}: {v['nazev']} ({v['datum']})", ""]
        odkazy = [f"[web](https://polachp.github.io/dovolena-thajsko-2026/verze/{v['id']}/)",
                  f"[Markdown](verze/{v['id']}/{md_soubor(v)})"]
        if i > 0 and v.get("commit") and VERZE[i-1].get("commit"):
            odkazy.append(f"[rozdíl proti {VERZE[i-1]['id']}](https://github.com/polachp/dovolena-thajsko-2026/compare/{VERZE[i-1]['commit']}...{v['commit']})")
        radky += [" · ".join(odkazy), ""] + [f"- {z}" for z in v["zmeny"]] + [""]
    (ROOT / "ZMENY.md").write_text("\n".join(radky), encoding="utf-8")
    print("Hotovo:", ", ".join(v["id"] for v in VERZE), "| aktuální:", posledni["id"])


if __name__ == "__main__":
    main()
