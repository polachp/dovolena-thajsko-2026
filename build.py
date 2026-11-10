"""Sestaví web ze src/verze.json, src/sablona.html a Markdownu každé verze (verze/<id>/<md>).

Nová verze:
  1. mkdir verze/vN a uložit tam upravený Markdown (název souboru je v poli "md")
  2. přidat záznam vN do src/verze.json (datum, název, změny, hlavička)
  3. python build.py
Starší verze se nemění, kořen webu vždy ukazuje poslední verzi.
"""
import hashlib
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
SABLONA = (ROOT / "src/sablona.html").read_text(encoding="utf-8")
VERZE = json.loads((ROOT / "src/verze.json").read_text(encoding="utf-8"))

# Odlet z Prahy pro odpocet v hlavicce (ISO 8601 vcetne posunu, CET = +01:00).
ODLET = "2026-11-26T00:00:00+01:00"

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
    cfg = {"id": v["id"], "base": base}
    if h.get("kam"):
        cfg["kam"] = h["kam"]  # sekce -> zalozka webu (pred, misto, ...): do v50 podle cisla sekce, od v51 podle nazvu
    cfg = json.dumps(cfg, ensure_ascii=False)
    a, z = v.get("smer", SMER_VYCHOZI)
    lede = v.get("lede", LEDE_VYCHOZI)
    sablona = SABLONA if lede else SABLONA.replace('  <p class="lede">{{LEDE}}</p>\n', "")
    return (sablona.replace("{{TITLE}}", f"Thajsko {a}–{z}").replace("{{H1}}", f'{a} <span class="arrow">→</span> {z}')
            .replace("{{LEDE}}", lede).replace("{{MD}}", md_soubor(v))
            .replace("{{EYEBROW}}", h["eyebrow"] + f' · verze {v["id"]} ({v["datum"]})').replace("{{FACTS}}", facts)
            .replace("{{ROUTE}}", "\n".join(route)).replace("{{CFG}}", cfg).replace("{{BASE}}", base).replace("{{ODLET}}", ODLET).replace("{{BUST}}", bust(v)))


def bust(v):
    """Krátký otisk obsahu: připojuje se za názvy skriptů, aby prohlížeč po nové verzi nenačetl starý obsah z mezipaměti."""
    md = (ROOT / "verze" / v["id"] / md_soubor(v)).read_text(encoding="utf-8")
    return hashlib.sha1((json.dumps(VERZE, ensure_ascii=False) + md).encode("utf-8")).hexdigest()[:8]


def zkontroluj_kam(v: dict, md: str) -> None:
    """Od v51 jsou sekce bez čísel a hlavicka.kam je klíčované názvem sekce (část nadpisu ## před dvojtečkou nebo závorkou,
    u sekcí se společným začátkem celý nadpis bez závorky).
    Název, který v kam chybí, by web tiše zařadil do záložky Na místě, proto build v takovém případě spadne."""
    kam = v["hlavicka"].get("kam")
    if not kam or any(k.isdigit() for k in kam):
        return  # starší verze: klíčem je číslo sekce z nadpisu
    nadpisy = []
    for blok in re.split(r"(?m)^(?=## )", md):
        if not blok.startswith("## ") or re.search(r"(?m)^### Fáze \d+:", blok):
            continue  # úvod souboru a itinerář (pozná se podle nadpisů fází) do kam nepatří
        nadpisy.append(blok.split("\n", 1)[0][3:].strip())
    # stejný začátek před dvojtečkou (Místa na trase: Bangkok, Místa na trase: Krabi) = názvem je celý nadpis bez závorky
    zacatky = [re.split(r"[:(]", n)[0].strip() for n in nadpisy]
    nazvy = [n.split("(")[0].strip() if zacatky.count(z) > 1 else z for n, z in zip(nadpisy, zacatky)]
    chybi = [n for n in nazvy if n not in kam]
    navic = [k for k in kam if k not in nazvy]
    if chybi or navic:
        raise SystemExit(f"{v['id']}: hlavicka.kam nesedí na nadpisy sekcí. Chybí v kam: {chybi}. Nemá nadpis: {navic}.")


def souradnice_fazi(md: str):
    """Sloupec "Střed na mapě" v tabulce na úvodu sekce Itinerář po fázích: {číslo fáze: (lat, lon) nebo None}.
    Vrací None, když sekce nebo sloupec chybí (verze do v52 přehledovou mapu nemají)."""
    m = re.search(r"(?m)^## Itinerář po fázích\s*$", md)
    if not m:
        return None
    uvod = re.split(r"(?m)^### ", md[m.end():], maxsplit=1)[0]
    radky = [r for r in uvod.split("\n") if r.startswith("|")]
    if not radky:
        return None
    hlavicka = [c.strip() for c in radky[0].strip().strip("|").split("|")]
    if "Střed na mapě" not in hlavicka:
        return None
    ix = hlavicka.index("Střed na mapě")
    out = {}
    for r in radky[2:]:
        bunky = [c.strip() for c in r.strip().strip("|").split("|")]
        if len(bunky) <= ix or not bunky[0].isdigit():
            continue  # řádek Celkem
        s = re.search(r"(\d{1,2}\.\d+),\s*(\d{2,3}\.\d+)", bunky[ix])
        out[int(bunky[0])] = (float(s.group(1)), float(s.group(2))) if s else None
    return out


def zkontroluj_mapu(v: dict, md: str, povinna: bool) -> None:
    """Přehledová mapa bere středy fází z Markdownu. Poslední verze musí mít souřadnici u každé fáze, jinak by mapa
    tiše chyběla nebo by některý kroužek nestál nikde. Starší verze sloupec mít nemusí, ale když ho mají, musí sedět."""
    body = souradnice_fazi(md)
    if body is None:
        if povinna:
            raise SystemExit(f"{v['id']}: v tabulce na úvodu Itinerář po fázích chybí sloupec Střed na mapě, přehledová mapa by se nezobrazila.")
        return
    fazi = len(re.findall(r"(?m)^### Fáze \d+:", md))
    chybi = [i for i in range(1, fazi + 1) if body.get(i) is None]
    navic = [i for i in body if i < 1 or i > fazi]
    mimo = [i for i, b in body.items() if b and not (5.0 <= b[0] <= 21.0 and 97.0 <= b[1] <= 106.0)]
    if chybi or navic or mimo:
        raise SystemExit(f"{v['id']}: sloupec Střed na mapě nesedí na fáze. Bez souřadnice: {chybi}. Fáze navíc: {navic}. Mimo Thajsko: {mimo}.")


def main():
    verejne =[{**{k: v.get(k) for k in ("id", "datum", "nazev", "zmeny", "commit")}, "md": md_soubor(v)} for v in VERZE]
    (ROOT / "verze.js").write_text(
        "// Generováno skriptem build.py ze src/verze.json.\nwindow.THAJSKO_VERZE = "
        + json.dumps(verejne, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")

    for v in VERZE:
        d = ROOT / "verze" / v["id"]
        md = (d / md_soubor(v)).read_text(encoding="utf-8")
        zkontroluj_kam(v, md)
        zkontroluj_mapu(v, md, v is VERZE[-1])
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
